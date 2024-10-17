from datetime import datetime

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.product.models import Basket, BasketItem
from app.product.repository import BasketRepository, ProductRepository, BasketItemRepository
from app.product.schemas import SRBasket, SCBasket, SUBasket, SRBasketItem, SCBasketItem
from app.repository.schemas import SBaseListResponse
from app.user.dependencies import get_current_user

router = APIRouter(
    prefix="/basket",
    tags=["Basket"],
)


@router.post("/", response_model=SRBasket, status_code=status.HTTP_201_CREATED)
async def create_basket(
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Создание новой корзины для текущего пользователя.
    """
    new_basket = await BasketRepository.create(
        session=session,
        user_id=current_user.id,
        active_status=True,
        total_price=0.0,
        created_at=datetime.utcnow()
    )

    # Выполняем запрос с предварительной загрузкой связанных объектов
    query = select(Basket).options(
        selectinload(Basket.basket_items),
        selectinload(Basket.user)
    ).filter(Basket.id == new_basket.id)
    result = await session.execute(query)
    basket = result.scalar_one()

    return SRBasket.from_orm(basket)

# Get All Baskets for Current User
@router.get("/", response_model=SBaseListResponse)
async def get_all_baskets(
    page: int = 1,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Получение всех корзин для текущего пользователя с поддержкой пагинации.
    """
    filter_condition = Basket.user_id == current_user.id
    query = select(Basket).options(
        selectinload(Basket.basket_items).selectinload(BasketItem.product),
        selectinload(Basket.user)
    ).filter(filter_condition).limit(limit).offset((page - 1) * limit)
    result = await session.execute(query)
    baskets = result.scalars().all()
    total = await BasketRepository.count(filter=filter_condition)
    baskets_data = [SRBasket.from_orm(basket) for basket in baskets]
    return {
        "data": baskets_data,
        "total": total,
        "page": page,
        "limit": limit
    }


# Get Basket by ID

@router.get("/{basket_id}", response_model=SRBasket)
async def get_basket(
    basket_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Получение корзины по ID для текущего пользователя.
    """
    query = select(Basket).options(
        selectinload(Basket.basket_items).selectinload(BasketItem.product),
        selectinload(Basket.user)
    ).filter(Basket.id == basket_id)
    result = await session.execute(query)
    basket = result.scalar_one_or_none()

    if not basket or basket.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Basket not found"
        )
    return SRBasket.from_orm(basket)

# Update Basket
@router.put("/{basket_id}", response_model=SRBasket)
async def update_basket(
    basket_id: int,
    basket_update: SUBasket,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Обновление корзины по ID для текущего пользователя.
    """
    basket = await BasketRepository.get_by_id(basket_id)
    if not basket or basket.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Basket not found"
        )

    # Обновляем корзину
    await BasketRepository.update(basket_id, basket_update.dict(exclude_unset=True))

    # Выполняем запрос с предварительной загрузкой связанных объектов
    query = select(Basket).options(
        selectinload(Basket.basket_items).selectinload(BasketItem.product),
        selectinload(Basket.user)
    ).filter(Basket.id == basket_id)
    result = await session.execute(query)
    updated_basket = result.scalar_one()

    return SRBasket.from_orm(updated_basket)

# Delete Basket
@router.delete("/{basket_id}", status_code=status.HTTP_200_OK)
async def delete_basket(
    basket_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Удаление корзины по ID для текущего пользователя.
    """
    basket = await BasketRepository.get_by_id(basket_id)
    if not basket or basket.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Basket not found"
        )
    await BasketRepository.destroy(basket_id, session)
    return {
        "message": "Basket deleted successfully"
    }


# Add Item to Basket
@router.post("/{basket_id}/items", response_model=SRBasketItem, status_code=status.HTTP_201_CREATED)
async def add_item_to_basket(
        basket_id: int,
        item_data: SCBasketItem,
        session: AsyncSession = Depends(get_session),
        current_user: str = Depends(get_current_user)
):
    """
    Добавление товара в корзину текущего пользователя.
    """
    # Получаем корзину по ID
    basket = await BasketRepository.get_by_id(basket_id)
    if not basket or basket.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Basket not found"
        )

    # Получаем продукт по ID
    product = await ProductRepository.get_by_id(item_data.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Создаем новый элемент корзины
    new_item = await BasketItemRepository.create(
        session=session,
        basket_id=basket_id,
        product_id=item_data.product_id,
        quantity=item_data.quantity,
        price=product.price  # Добавляем цену продукта
    )

    # Обновляем общую цену корзины
    basket.total_price += product.price * item_data.quantity
    await session.commit()

    # Выполняем запрос с предварительной загрузкой связанных объектов
    query = select(BasketItem).options(selectinload(BasketItem.product)).filter(BasketItem.id == new_item.id)
    result = await session.execute(query)
    new_item_with_product = result.scalar_one()

    return SRBasketItem.from_orm(new_item_with_product)

# Remove Item from Basket
@router.delete("/{basket_id}/items/{item_id}", status_code=status.HTTP_200_OK)
async def remove_item_from_basket(
    basket_id: int,
    item_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Удаление товара из корзины текущего пользователя.
    """
    basket = await BasketRepository.get_by_id(basket_id)
    if not basket or basket.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Basket not found"
        )

    item = await BasketItemRepository.get_by_id(item_id)
    if not item or item.basket_id != basket_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in this basket"
        )

    product = await ProductRepository.get_by_id(item.product_id)
    # Обновляем цену корзины
    basket.total_price -= product.price * item.quantity
    await BasketItemRepository.destroy(item_id)
    await session.commit()
    return {
        "message": "Item removed from basket successfully"
    }


# Update Item Quantity in Basket
@router.put("/{basket_id}/items/{item_id}", response_model=SRBasketItem)
async def update_item_quantity(
    basket_id: int,
    item_id: int,
    item_update: SCBasketItem,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Обновление количества товара в корзине текущего пользователя.
    """
    basket = await BasketRepository.get_by_id(basket_id)
    if not basket or basket.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Basket not found"
        )

    item = await BasketItemRepository.get_by_id(item_id)
    if not item or item.basket_id != basket_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in this basket"
        )

    # Обновляем количество и цену корзины
    product = await ProductRepository.get_by_id(item.product_id)
    basket.total_price = basket.total_price - (product.price * item.quantity) + (product.price * item_update.quantity)
    item.quantity = item_update.quantity
    await session.commit()

    # Перезагружаем элемент корзины с предварительной загрузкой связанного объекта
    query = select(BasketItem).options(selectinload(BasketItem.product)).filter(BasketItem.id == item.id)
    result = await session.execute(query)
    updated_item = result.scalar_one()

    return SRBasketItem.from_orm(updated_item)