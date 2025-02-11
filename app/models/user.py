from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.transaction import Transaction


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    coins_balance = Column(Integer, nullable=False)

    inventory = relationship("Inventory", back_populates="user")
    sent_transactions = relationship("Transaction", foreign_keys=[Transaction.sender_id], back_populates="sender")
    received_transactions = relationship("Transaction", foreign_keys=[Transaction.receiver_id],back_populates="receiver")



