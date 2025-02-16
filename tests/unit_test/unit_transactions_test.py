from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from app.crud.auth import add_user, get_user_by_id
from app.crud.transaction import add_transaction, get_sent_transactions_by_user_id, get_received_transactions_by_user_id
from app.services.auth import get_password_hash

pytestmark = pytest.mark.anyio


async def test_send_coins(session: AsyncSession):
    user_1_info = {
        "username": "user1",
        "password": "user1_password",
        "hashed_password": get_password_hash("user1_password"),
    }
    user_2_info = {
        "username": "user2",
        "password": "user2_password",
        "hashed_password": get_password_hash("user2_password"),
    }

    user_1 = await add_user(user_1_info['username'], user_1_info['hashed_password'], session)
    user_2 = await add_user(user_2_info['username'], user_2_info['hashed_password'], session)
    amount_1 = 100
    transaction_1 = await add_transaction(amount=amount_1, sender=user_1.id, receiver=user_2.id, session=session)
    assert transaction_1 is not None
    assert transaction_1.amount == amount_1

    get_send_transactions = await get_sent_transactions_by_user_id(user_1.id, session)
    assert len(get_send_transactions) == 1
    assert get_send_transactions[0].toUser == user_2.username

    get_received_transactions = await get_received_transactions_by_user_id(user_2.id, session)
    assert len(get_received_transactions) == 1
    assert get_received_transactions[0].fromUser == user_1.username




