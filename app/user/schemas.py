from typing import List
from pydantic import BaseModel


class SGUser(BaseModel):
    id: int
    name: str
    email: str
    hashed_password: str
    profile_picture: str

    baskets: List


class SCUser(BaseModel):
    name: str
    email: str
    hashed_password: str
    profile_picture: str | None


class SUUser(BaseModel):
    id: int
    name: str
    email: str
    hashed_password: str
    profile_picture: str | None


class SDUser(BaseModel):
    id: int
