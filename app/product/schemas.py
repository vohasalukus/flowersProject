from datetime import datetime
from typing import List

from pydantic import BaseModel


class SGProduct(BaseModel):
    id: int
    name: str
    price: float
    description: str
    quantity: int
    product_image: str

    basket_items: List


class SCProduct(BaseModel):
    name: str
    price: float
    description: str
    quantity: int
    product_image: str


class SUProduct(BaseModel):
    id: int
    name: str
    price: float
    description: str
    quantity: int
    product_image: str


class SDProduct(BaseModel):
    id: int


class SGBasket(BaseModel):
    id: int
    created_at: datetime
    price: float
    active_status: bool

    user_id: int

    basket_items: List


class SCBasket(BaseModel):
    id: int
    price: float



class SBasket(BaseModel):
    id: int | None
    created_at: datetime
    price: float
    active_status: bool

    user_id: int

    basket_items: List

class SBasket(BaseModel):
    id: int | None
    created_at: datetime
    price: float
    active_status: bool

    user_id: int

    basket_items: List

class SBasketItem(BaseModel):
    id: int
    price: float
    quantity: int

    basket_id: int

    product_id: int
