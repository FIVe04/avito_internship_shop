from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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