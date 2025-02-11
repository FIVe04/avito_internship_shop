from pydantic import BaseModel


class ItemSchema(BaseModel):
    user_id: int
    product_id: int
    quantity: int