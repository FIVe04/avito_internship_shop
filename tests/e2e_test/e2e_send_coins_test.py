from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.models.user import User
import pytest


pytestmark = pytest.mark.anyio


async def test_e2e_send_coins(client: AsyncClient, session: AsyncSession):
    user1 = {
        'username': 'user1',
        'password': 'password'
    }
    user2 = {
        'username': 'user2',
        'password': 'password'
    }
    async with client as ac:
        auth_user1_response = await ac.post(
            "/api/auth/",
            data={"username": user1.get('username'), "password": user1.get('password')},
        )
        auth_user2_response = await ac.post(
            "/api/auth/",
            data={"username": user2.get('username'), "password": user2.get('password')},
        )

        assert auth_user1_response.status_code == 200
        assert auth_user2_response.status_code == 200

        amount_small = 100
        amount_large = 20000

        headers_user1 = {"Authorization": f"Bearer {auth_user1_response.json().get('access_token')}"}
        headers_user2 = {"Authorization": f"Bearer {auth_user2_response.json().get('access_token')}"}

        send_coins_response = await ac.post(
            "/api/sendCoin/",
            json={"toUser": user2.get('username'), "amount": amount_small},
            headers=headers_user1,
        )

        send_coins_large_response = await ac.post(
            "/api/sendCoin/",
            json={"toUser": user2.get('username'), "amount": amount_large},
            headers=headers_user1,
        )

        send_coins_unknown_user = await ac.post(
            "/api/sendCoin/",
            json={"toUser": 'none', "amount": amount_large},
            headers=headers_user1,
        )

        assert send_coins_unknown_user.status_code == 400
        assert send_coins_unknown_user.json().get('detail') == 'User not found.'

        assert send_coins_response.status_code == 200

        assert send_coins_large_response.status_code == 400
        assert send_coins_large_response.json().get('detail') == 'Not enough coins.'

