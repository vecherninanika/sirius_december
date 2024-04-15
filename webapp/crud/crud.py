from typing import Sequence
from fastapi_pagination import Page
from sqlalchemy import Row, RowMapping
from typing import Any, List, Type, TypeVar
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from fastapi_pagination.ext.sqlalchemy import paginate

from webapp.metrics import async_integrations_timer

ModelT = TypeVar('ModelT', bound=DeclarativeMeta)


@async_integrations_timer
async def get(session: AsyncSession, model_id: Any, model: Type[ModelT]) -> List[ModelT] | None:
    return (await session.scalars(select(model).where(model.id == model_id))).one_or_none()


@async_integrations_timer
async def get_all(session: AsyncSession, model: Type[ModelT]) -> Page[Row | RowMapping | Any] | None:
    # return (await session.scalars(select(model))).all()  # сделать пагинацию
    return await paginate(session, select(model))   # TODO может быть ошибка


@async_integrations_timer
async def create(session: AsyncSession, data: Any, model: ModelT) -> ModelT:
    async with session.begin_nested():
        async with session.begin_nested():
            data_dict = data.dict()
            instance = model(**data_dict)
            session.add(instance)
            await session.flush()
            await session.commit()
        return instance


@async_integrations_timer
async def delete(session: AsyncSession, id_: int, model: ModelT) -> int:
    deleted_id = (
        await session.execute(delete(model).where(model.id == id_).returning(model.id))
    ).one_or_none()[0]
    await session.commit()
    return deleted_id


@async_integrations_timer
async def update(session: AsyncSession, id_: int, data: Any, model: ModelT) -> Row | None:
    data_dict = data.dict()
    updated = (
        await session.execute(update(model).where(model.id == id_).values(**data_dict))
    ).one_or_none()
    await session.commit()
    return updated
