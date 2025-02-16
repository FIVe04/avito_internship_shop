from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from app.crud.auth import add_user, get_user_by_id, get_user_by_username


from app.services.auth import get_password_hash, verify_password, create_access_token, verify_token

pytestmark = pytest.mark.anyio


async def test_add_user(session: AsyncSession):

    user_1_info = {
        "username": "user1",
        "password": "user1_password",
        "hashed_password": get_password_hash("user1_password"),
    }

    assert verify_password(user_1_info["password"], user_1_info["hashed_password"])

    user_1 = await add_user(user_1_info['username'], user_1_info['hashed_password'], session)
    assert user_1.username == user_1_info['username']


async def test_get_user(session: AsyncSession):
    user_1_info = {
        "username": "user1",
        "password": "user1_password",
        "hashed_password": get_password_hash("user1_password"),
    }

    user_1 = await add_user(user_1_info['username'], user_1_info['hashed_password'], session)
    user_get_by_id = await get_user_by_id(user_1.id, session)

    assert user_get_by_id == user_1

    user_get_by_username = await get_user_by_username(user_1.username, session)
    assert user_get_by_username == user_1


async def test_jwt_token(session: AsyncSession):
    user_1_info = {
        "username": "user1",
        "password": "user1_password",
        "hashed_password": get_password_hash("user1_password"),
    }
    user_1 = await add_user(user_1_info['username'], user_1_info['hashed_password'], session)
    token = create_access_token(data={'sub': str(user_1.id)})
    payload = verify_token(token)
    assert payload is not None
    assert payload['sub'] == str(user_1.id)

























