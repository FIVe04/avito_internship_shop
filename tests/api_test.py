from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
import pytest


pytestmark = pytest.mark.anyio


async def test_api_first_auth(client: AsyncClient):
    test_name = "test"
    async with client as ac:
        response = await ac.post(
            "/api/auth/",
            data={"username": "testNew", "password": "passwd"},
        )


        assert response.status_code == 200
        assert response.json().get('access_token') is not None


async def test_api_purchase(client: AsyncClient, session: AsyncSession):
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
            json={"item": test_item},
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












