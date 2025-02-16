from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.models.user import User
import pytest


pytestmark = pytest.mark.anyio



















