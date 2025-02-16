from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import pytest


pytestmark = pytest.mark.anyio


async def test_e2e_info(client: AsyncClient, session: AsyncSession):
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

        headers_user1 = {"Authorization": f"Bearer {auth_user1_response.json().get('access_token')}"}
        headers_user2 = {"Authorization": f"Bearer {auth_user2_response.json().get('access_token')}"}

        amount_1 = 100
        amount_2 = 70


        send_coins_response_1 = await ac.post(
            "/api/sendCoin/",
            json={"toUser": user2.get('username'), "amount": amount_1},
            headers=headers_user1,
        )


        send_coins_response_1 = await ac.post(
            "/api/sendCoin/",
            json={"toUser": user1.get('username'), "amount": amount_2},
            headers=headers_user2,
        )

        purchase_response_user_1 = await ac.post(
            f"/api/buy/?item=cup",
            headers=headers_user1,
        )

        info_user_1 = await ac.get(
            "/api/info/",
            headers=headers_user1,
        )

        assert info_user_1.status_code == 200
        assert info_user_1.json().get('coins') == 1000 - amount_1 + amount_2 - 20
        assert len(info_user_1.json().get('inventory')) == 1
        assert info_user_1.json().get('inventory')[0]['type'] == 'cup'

        assert len(info_user_1.json().get('coinHistory').get('received')) == 1
        assert len(info_user_1.json().get('coinHistory').get('sent')) == 1

        assert info_user_1.json().get('coinHistory').get('sent')[0]['toUser'] == user2.get('username')
        assert info_user_1.json().get('coinHistory').get('sent')[0]['amount'] == amount_1

        assert info_user_1.json().get('coinHistory').get('received')[0]['fromUser'] == user2.get('username')
        assert info_user_1.json().get('coinHistory').get('received')[0]['amount'] == amount_2

