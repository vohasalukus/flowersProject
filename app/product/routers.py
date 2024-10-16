from fastapi import APIRouter
from app.product.routes.product_router import router as product_router

router = APIRouter(prefix="/app", tags=["App"])

router.include_router(product_router)
