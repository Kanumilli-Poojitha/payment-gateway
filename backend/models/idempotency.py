from sqlalchemy import Column, String, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from database import Base


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    id = Column(String, primary_key=True)
    merchant_id = Column(String, ForeignKey("merchants.id"), nullable=True)

    idem_key = Column(String, nullable=False)

    request_hash = Column(String, nullable=False)
    response_body = Column(Text, nullable=False)
    response_code = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("merchant_id", "idem_key", name="uq_merchant_idem_key"),
    )