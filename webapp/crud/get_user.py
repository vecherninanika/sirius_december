from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from webapp.metrics import async_integrations_timer
from webapp.models.sirius.user import User
from webapp.schema.user import UserLogin


# @async_integrations_timer
async def get_user(session: AsyncSession, username: str = None, user_id: int = None) -> User | None:
    query = None
    if username:
        query = User.username == username
    elif user_id:
        query = User.id == user_id
    return (await session.scalars(select(User).where(query))).one_or_none()
