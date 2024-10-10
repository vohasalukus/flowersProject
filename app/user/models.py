from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):

    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    profile_picture: Mapped[str] = mapped_column(String)

    # One to many
    baskets: Mapped[List["Basket"]] = relationship("Basket", back_populates="user")
