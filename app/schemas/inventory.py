from pydantic import BaseModel


class InventoryItem(BaseModel):
    type: str
    quantity: int