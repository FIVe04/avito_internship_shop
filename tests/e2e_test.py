from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.models.user import User
import pytest


pytestmark = pytest.mark.anyio


async def test_e2e_purchase(client: AsyncClient, session: AsyncSession):
    test_item = "cup"
    async with client as ac:
        auth_response = await ac.post(
            "/api/auth/",
            data={"username": "testUser", "password": "passwd"},
        )

        result_user = await session.execute(select(User).where(User.username == "testUser"))    # type: ignore
        assert result_user.scalar_one_or_none().username == "testUser"

        assert auth_response.status_code == 200

        token = auth_response.json().get("access_token")
        assert token is not None

        purchase_response_success = await ac.post(
            f"/api/buy/?item=cup",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert purchase_response_success.status_code == 200

        purchase_response_not_found = await ac.post(
            f"/api/buy/?item=fork",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert purchase_response_not_found.status_code == 400
        assert purchase_response_not_found.json().get('detail') == 'Product not found'

        purchase_response_not_authenticated = await ac.post(
            f"/api/buy/?item=cup",
            json={"item": test_item},
            headers={"Authorization": f"Bearer sadssad"}
        )

        assert purchase_response_not_authenticated.status_code == 401
        assert purchase_response_not_authenticated.json().get('detail') == 'Unauthorized.'


        auth_response_2 = await ac.post(
            "/api/auth/",
            data={"username": "testUser2", "password": "passwd"},
        )

        result_user = await session.execute(select(User).where(User.username == "testUser2"))    # type: ignore
        assert result_user.scalar_one_or_none().username == "testUser2"

        token = auth_response_2.json().get("access_token")
        assert token is not None
        purchase_response_fine_2 = await ac.post(
            f"/api/buy/?item=pink-hoody",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert purchase_response_fine_2.status_code == 200

        purchase_response_fine_3 = await ac.post(
            f"/api/buy/?item=pink-hoody",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert purchase_response_fine_3.status_code == 200

        purchase_response_not_enough = await ac.post(
            f"/api/buy/?item=pink-hoody",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert purchase_response_not_enough.status_code == 400
        assert purchase_response_not_enough.json().get('detail') == 'Not enough coins'


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

