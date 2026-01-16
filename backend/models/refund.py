from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Refund(Base):
    __tablename__ = "refunds"

    id = Column(String, primary_key=True, index=True)
    payment_id = Column(String, ForeignKey("payments.id"), nullable=False)
    merchant_id = Column(String, nullable=False)

    amount = Column(Integer, nullable=False)
    status = Column(String, default="PENDING")  # PENDING | PROCESSED | FAILED

    reason = Column(String, nullable=True)
    error_code = Column(String, nullable=True)
    error_description = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )