import os
import time
import redis
import json
import random
import signal
from sqlalchemy.orm import Session
from database import SessionLocal
from models.payment import Payment
from models.order import Order

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
QUEUE_NAME = os.getenv("WORKER_QUEUE", "gateway_jobs")
DLQ_QUEUE = os.getenv("DLQ_QUEUE", "gateway_jobs_dlq")
WEBHOOK_QUEUE = os.getenv("WEBHOOK_QUEUE", "gateway_webhooks")

MAX_RETRIES = int(os.getenv("WORKER_MAX_RETRIES", "3"))
TEST_MODE = os.getenv("TEST_MODE", "true").lower() == "true"

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
running = True


def graceful_shutdown(signum, frame):
    global running
    print("🛑 Payment worker shutting down...")
    running = False


signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)


def process_payment(payment_id: str) -> bool:
    db: Session = SessionLocal()
    try:
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            print(f"❌ Payment {payment_id} not found")
            return False

        order = db.query(Order).filter(Order.id == payment.order_id).first()
        if not order:
            print(f"❌ Order {payment.order_id} not found")
            return False

        payment.status = "PROCESSING"
        db.commit()
        print(f"⚙️ Processing payment {payment.id}")

        time.sleep(2)

        success = True if TEST_MODE else random.random() < 0.9

        if success:
            payment.status = "SUCCESS"
            order.status = "PAID"
            print(f"✅ Payment {payment.id} SUCCESS")
        else:
            payment.status = "FAILED"
            payment.error_code = "PAYMENT_FAILED"
            payment.error_description = "Authorization failed"
            order.status = "FAILED"
            print(f"❌ Payment {payment.id} FAILED")

        db.commit()

        # enqueue webhook (FINAL STATE ONLY)
        redis_client.rpush(WEBHOOK_QUEUE, json.dumps({
            "payment_id": payment.id,
            "event_type": f"payment.{payment.status.lower()}",
            "amount": payment.amount,
            "currency": payment.currency,
            "method": payment.method,
            "order_id": payment.order_id,
            "merchant_id": payment.merchant_id,
        }))

        return success
    finally:
        db.close()


def worker_loop():
    print("🟢 Payment worker started")
    while running:
        item = redis_client.blpop(QUEUE_NAME, timeout=5)
        if not item:
            continue

        _, payload = item

        try:
            job = json.loads(payload)
        except json.JSONDecodeError:
            redis_client.rpush(DLQ_QUEUE, payload)
            continue

        payment_id = job.get("payment_id")
        retries = job.get("retries", 0)

        if not payment_id:
            redis_client.rpush(DLQ_QUEUE, payload)
            continue

        success = process_payment(payment_id)

        if not success:
            if retries < MAX_RETRIES:
                job["retries"] = retries + 1
                redis_client.rpush(QUEUE_NAME, json.dumps(job))
                print(f"🔁 Retry {job['retries']} for payment {payment_id}")
            else:
                redis_client.rpush(DLQ_QUEUE, json.dumps(job))
                print(f"⚠️ Payment {payment_id} moved to DLQ")


if __name__ == "__main__":
    worker_loop()