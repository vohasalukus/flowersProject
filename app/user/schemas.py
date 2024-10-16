from pydantic import BaseModel, EmailStr


class SGUser(BaseModel):
    name: str
    email: EmailStr
    profile_picture: str | None


class SCUser(SGUser):
    password: str


class SUUser(BaseModel):
    name: str | None
    email: EmailStr | None
    profile_picture: str | None
    password: str


class SRUser(SGUser):
    id: int


class SAuth(BaseModel):
    username: str
    password: str
    email: EmailStr
