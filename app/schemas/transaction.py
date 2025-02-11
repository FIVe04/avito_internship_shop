from pydantic import BaseModel, conint


class TransactionCreate(BaseModel):
    receiver_id: int
    amount: conint(gt=0)


class CoinTransaction(BaseModel):
    amount: int


class CoinTransactionReceived(CoinTransaction):
    fromUser: str


class CoinTransactionSent(CoinTransaction):
    toUser: str


