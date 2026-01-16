from fastapi import APIRouter
import redis
import os

router = APIRouter(prefix="/jobs", tags=["Jobs"])

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

QUEUES = {
    "gateway_jobs": "pending",
    "gateway_jobs_dlq": "dlq",
    "gateway_webhooks": "webhooks",
    "gateway_webhooks_dlq": "webhooks_dlq",
    "gateway_refunds": "refunds",
    "gateway_refunds_dlq": "refunds_dlq",
}


@router.get("/health")
def job_queue_health():
    return {
        "status": "ok",
        "queues": {
            queue: redis_client.llen(queue)
            for queue in QUEUES
        },
    }