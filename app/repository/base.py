from sqlalchemy import select
from app.database import async_session


class BaseRepository:
    model = None

    @classmethod
    async def get_all(cls):
        async with async_session() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_by_id(cls, id):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_by(cls, **filters):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, **data):
        async with async_session() as session:
            instance = cls.model(**data)
            session.add(instance)
            await session.commit()
            return instance

    @classmethod
    async def update(cls, id, data):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            instance = result.scalar_one_or_none()
            if not instance:
                return {'message': 'Post not found'}
            for key, value in data.dict().items():
                setattr(instance, key, value)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    @classmethod
    async def destroy(cls, id):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            instance = result.scalar()
            session.delete(instance)
            await session.commit()
            return {'message': f'Post {id} deleted'}
