from typing import List

from pydantic import BaseModel

from app.schemas.inventory import InventoryItem
from app.schemas.transaction import CoinTransaction, CoinTransactionReceived, CoinTransactionSent


class CoinHistory(BaseModel):
    received: List[CoinTransactionReceived] | None = None
    sent: List[CoinTransactionSent] | None = None


class InfoResponse(BaseModel):
    coins: int
    inventory: List[InventoryItem]
    coinHistory: CoinHistory
