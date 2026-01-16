from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json
import redis
import os

from database import get_db
from auth import authenticate
from models.webhook_log import WebhookLog
from models.webhook import Webhook
from schemas.webhook_log import WebhookLogResponse
from utils.errors import not_found

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
QUEUE_NAME = os.getenv("WEBHOOK_QUEUE", "gateway_webhooks")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

router = APIRouter(prefix="/webhook-logs", tags=["webhook-logs"])


# -------------------------------------------------
# GET webhook delivery logs (merchant dashboard)
# -------------------------------------------------
@router.get("", response_model=list[WebhookLogResponse])
def list_webhook_logs(
    merchant=Depends(authenticate),
    db: Session = Depends(get_db),
):
    return (
        db.query(WebhookLog)
        .join(Webhook, Webhook.id == WebhookLog.webhook_id)
        .filter(Webhook.merchant_id == merchant.id)
        .order_by(WebhookLog.created_at.desc())
        .all()
    )


# -------------------------------------------------
# POST retry failed webhook
# -------------------------------------------------
@router.post("/{log_id}/retry")
def retry_webhook(
    log_id: str,
    merchant=Depends(authenticate),
    db: Session = Depends(get_db),
):
    log = (
        db.query(WebhookLog)
        .join(Webhook, Webhook.id == WebhookLog.webhook_id)
        .filter(
            WebhookLog.id == log_id,
            Webhook.merchant_id == merchant.id,
        )
        .first()
    )

    if not log:
        not_found("Webhook log not found")

    # Re-enqueue payload
    redis_client.rpush(QUEUE_NAME, json.dumps(log.payload))

    # Reset status for visibility
    log.status = "pending"
    db.commit()

    return {"message": "Webhook retry queued"}