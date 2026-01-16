import os
import json
import redis
import requests
import signal
import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import Webhook, WebhookLog, Payment
from utils.webhooks import generate_signature

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
QUEUE_NAME = os.getenv("WEBHOOK_QUEUE", "gateway_webhooks")
DLQ_QUEUE = os.getenv("WEBHOOK_DLQ_QUEUE", "gateway_webhooks_dlq")
MAX_RETRIES = int(os.getenv("WEBHOOK_MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("WEBHOOK_RETRY_DELAY", "2"))
DATABASE_URL = os.getenv("DATABASE_URL")
TEST_MODE = os.getenv("TEST_MODE", "true").lower() == "true"

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

running = True


def graceful_shutdown(signum, frame):
    global running
    print("🛑 Webhook worker shutting down...")
    running = False


signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

def send_webhook(url, secret, payload):
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    signature = generate_signature(secret, body)

    headers = {
        "Content-Type": "application/json",
        "X-Webhook-Signature": signature
    }

    try:
        resp = requests.post(url, data=body, headers=headers, timeout=5)
        return resp.status_code, resp.text
    except Exception as e:
        return None, str(e)


def process_job(job):
    db = SessionLocal()
    try:
        payment = db.query(Payment).filter_by(id=job["payment_id"]).first()
        if not payment:
            return True  # drop invalid job silently

        webhooks = db.query(Webhook).filter(
            Webhook.merchant_id == payment.merchant_id,
            Webhook.active == True
        ).all()

        for webhook in webhooks:
            log = db.query(WebhookLog).filter_by(
                webhook_id=webhook.id,
                event_type=job["event_type"]
            ).first()

            if not log:
                log = WebhookLog(
                    webhook_id=webhook.id,
                    event_type=job["event_type"],
                    payload=job,
                    attempts=0
                )
                db.add(log)
                db.commit()

            if log.attempts >= MAX_RETRIES:
                redis_client.rpush(DLQ_QUEUE, json.dumps(job))
                continue

            status, response = send_webhook(webhook.url, webhook.secret, job)

            log.attempts += 1
            log.response_code = status
            log.response_body = response

            if status and 200 <= status < 300:
                log.status = "success"
            else:
                log.status = "failed"
                db.commit()
                time.sleep(RETRY_DELAY)
                redis_client.rpush(QUEUE_NAME, json.dumps(job))
                continue

            db.commit()

        return True
    finally:
        db.close()


def worker_loop():
    print("🟢 Webhook worker started")
    while running:
        item = redis_client.blpop(QUEUE_NAME, timeout=5)
        if not item:
            continue

        _, payload = item
        job = json.loads(payload)
        process_job(job)


if __name__ == "__main__":
    worker_loop()