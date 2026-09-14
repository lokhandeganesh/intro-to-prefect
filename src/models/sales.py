# models/sales.py
from sqlalchemy import Column, DateTime, Integer, Numeric, String

from db.database import Base


class RawTransaction(Base):
    __tablename__ = "raw_transactions"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime)

class ProcessedSummary(Base):
    __tablename__ = "processed_customer_summaries"

    customer_id = Column(Integer, primary_key=True)
    total_spend = Column(Numeric(14, 2), nullable=False)
    transaction_count = Column(Integer, nullable=False)
    customer_tier = Column(String(20), nullable=False)
