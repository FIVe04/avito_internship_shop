from sqlalchemy import Column, Integer, String

from app.core.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)



