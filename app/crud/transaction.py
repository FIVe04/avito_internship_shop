from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth import get_user_by_id
from app.models.transaction import Transaction
from app.schemas.transaction import CoinTransaction, CoinTransactionSent, CoinTransactionReceived


async def add_transaction(amount: int, sender: int, receiver: int, session: AsyncSession):
    new_transaction = Transaction(amount=amount, sender_id=sender, receiver_id=receiver)
    session.add(new_transaction)
    await session.commit()
    await session.refresh(new_transaction)
    return new_transaction


async def get_sent_transactions_by_user_id(user_id: int, session: AsyncSession) -> List[CoinTransactionSent]:
    result = await session.execute(select(Transaction).filter(Transaction.sender_id == user_id))
    transactions = result.scalars().all()
    transactions_data = []
    for transaction in transactions:

        receiver = await get_user_by_id(transaction.receiver_id, session)

        transactions_data.append(
            CoinTransactionSent(toUser=receiver.username, amount=transaction.amount)
        )
    return transactions_data


async def get_received_transactions_by_user_id(user_id: int, session: AsyncSession) -> List[CoinTransactionReceived]:
    result = await session.execute(select(Transaction).filter(Transaction.receiver_id == user_id))
    transactions = result.scalars().all()
    transactions_data = []
    for transaction in transactions:

        sender = await get_user_by_id(transaction.sender_id, session)

        transactions_data.append(
            CoinTransactionReceived(fromUser=sender.username, amount=transaction.amount)
        )
    return transactions_data
