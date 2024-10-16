from fastapi import FastAPI
from app.user.routers import router as user_router
from app.product.routers import router as mini_router

app = FastAPI()

app.include_router(user_router)
app.include_router(mini_router)