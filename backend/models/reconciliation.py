from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base
import uuid

class PaymentLog(Base):
    __tablename__ = "payment_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    payment_id = Column(String, ForeignKey("payments.id"), nullable=False, index=True)
    old_status = Column(String, nullable=False)
    new_status = Column(String, nullable=False)
    worker_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())