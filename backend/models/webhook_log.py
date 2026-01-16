from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from database import Base
import uuid


class WebhookLog(Base):
    __tablename__ = "webhook_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    webhook_id = Column(String, ForeignKey("webhooks.id"), nullable=False)

    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)

    status = Column(String, default="pending")  # pending | success | failed
    response_code = Column(String, nullable=True)
    response_body = Column(String, nullable=True)

    attempts = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )