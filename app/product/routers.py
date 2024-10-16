from fastapi import APIRouter
from app.product.routes.product_router import router as product_router

router = APIRouter(prefix="/app")

router.include_router(product_router)
