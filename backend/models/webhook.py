from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from database import Base

class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(String, primary_key=True, index=True)
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True)
    url = Column(String, nullable=False)
    secret = Column(String, nullable=False)  # HMAC secret
    active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )