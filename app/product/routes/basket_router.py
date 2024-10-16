from datetime import datetime

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.product.repository import BasketRepository
from app.product.schemas import SRBasket, SCBasket
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
    # Возвращаем основные данные корзины
    return SRBasket(
        id=new_basket.id,
        user_id=new_basket.user_id,
        total_price=new_basket.total_price,
        active_status=new_basket.active_status,
        created_at=new_basket.created_at
    )