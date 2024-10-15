from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.user.auth import get_hashed_password, verify_password, create_access_token
from app.user.dependencies import get_current_user
from app.user.models import User
from app.user.repository import UserRepository
from app.user.schemas import SRUser, SCUser, SAuth

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
)


@router.post("/register", response_model=SRUser, status_code=status.HTTP_201_CREATED)
async def register_user(data: SCUser):
    existing_user = await UserRepository.get_by(email=data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_hashed_password(data.password)
    user = await UserRepository.create(
        name=data.name,
        email=data.email,
        hashed_password=hashed_password,
        profile_picture=data.profile_picture,
    )
    return user


@router.post("/login")
async def login(data: SAuth, response: Response):
    user = await UserRepository.get_by(email=data.email)
    if user is None or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = create_access_token(user.id)
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return {"message": "Successfully logged in"}


@router.get("/current-user", response_model=SRUser)
async def get_current_user_route(current_user: User = Depends(get_current_user)):
    return current_user
