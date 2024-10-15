from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.product.models import Basket


class User(Base):

    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(256))
    profile_picture: Mapped[str] = mapped_column(String, nullable=True)

    # One to many
    baskets: Mapped[List["Basket"]] = relationship(
        "Basket", back_populates="user", cascade="all, delete-orphan"
    )
