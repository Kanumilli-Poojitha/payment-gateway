from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid
import secrets

from database import get_db
from models.webhook import Webhook
from auth import authenticate
from utils.errors import bad_request, not_found

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("")
def register_webhook(url: str, merchant=Depends(authenticate), db: Session = Depends(get_db)):
    if not url.startswith("http"):
        return bad_request("Invalid URL")

    webhook = Webhook(
        id=str(uuid.uuid4()),
        merchant_id=merchant.id,
        url=url,
        secret=secrets.token_hex(16)  # HMAC secret
    )
    db.add(webhook)
    db.commit()
    db.refresh(webhook)

    return {"id": webhook.id, "url": webhook.url, "secret": webhook.secret}

@router.get("")
def list_webhooks(merchant=Depends(authenticate), db: Session = Depends(get_db)):
    return db.query(Webhook).filter(Webhook.merchant_id == merchant.id, Webhook.active == True).all()