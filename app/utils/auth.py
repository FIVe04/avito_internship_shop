from datetime import timedelta, datetime
from typing import Optional

from app.core.config import settings


def get_expiration_timestamp_access_token(expires_delta: Optional[timedelta] = None):
    if expires_delta is None:
        return datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return datetime.utcnow() + expires_delta

