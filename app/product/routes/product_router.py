from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.product.models import Product
from app.product.schemas import SCProduct, SRProduct
from app.user.dependencies import get_current_user

router = APIRouter(
    prefix="/product",
    tags=["product"],
)


@router.post("/", response_model=SRProduct, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: SCProduct,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user)
):

    new_product = Product(**product_data.dict())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product
