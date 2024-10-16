from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.product.repository import ProductRepository
from app.product.schemas import SCProduct, SRProduct, SUProduct
from app.repository.schemas import SBaseListResponse
from app.repository.tools import get_list_data
from app.user.dependencies import get_current_user

router = APIRouter(
    prefix="/product",
    tags=["Product"],
)


@router.post("/", response_model=SRProduct, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: SCProduct,
    current_user: str = Depends(get_current_user)
):
    new_product = await ProductRepository.create(**product_data.dict())
    return new_product


@router.get("/", response_model=SBaseListResponse)
async def get_all_products(
    page: int = 1,
    limit: int = 10
):

    products = await ProductRepository.paginate(page=page, limit=limit)
    total = await ProductRepository.count()

    products_data = [SRProduct.from_orm(product) for product in products]
    return {
        "data": products_data,
        "total": total,
        "page": page,
        "limit": limit
    }


@router.get("/{product_id}", response_model=SRProduct)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(get_session)
):
    product = await ProductRepository.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.put("/{product_id}", response_model=SRProduct)
async def update_product(
    product_id: int,
    product_update: SUProduct,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    updated_product = await ProductRepository.update(product_id, product_update.dict(exclude_unset=True))
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user)
):

    delete_result = await ProductRepository.destroy(product_id, session)

    if delete_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }