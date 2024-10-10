from datetime import datetime
from typing import List

from sqlalchemy import Integer, String, Float, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Product(Base):

    name: Mapped[str] = mapped_column(String, index=True)
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(Text)
    quantity: Mapped[int] = mapped_column(Integer)
    product_image: Mapped[str] = mapped_column(String)

    # One to many
    basket_items: Mapped[List["BasketItem"]] = relationship("BasketItem", back_populates="product")


class Basket(Base):

    created_at: Mapped[datetime] = mapped_column(DateTime)
    total_price: Mapped[float] = mapped_column(Float)
    active_status: Mapped[bool] = mapped_column(Boolean, default=True)

    # One to many
    user: Mapped["User"] = relationship("User", back_populates="baskets")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    # One to many
    basket_items: Mapped[List["BasketItem"]] = relationship("BasketItem", back_populates="basket")


class BasketItem(Base):

    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer)

    # One to many
    basket: Mapped["Basket"] = relationship("Basket", back_populates="basket_items")
    basket_id: Mapped[int] = mapped_column(Integer, ForeignKey("baskets.id"))

    # One to many
    product: Mapped["Product"] = relationship("Product", back_populates="basket_items")
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
