from starlette import status
from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.user.router import auth_router
from webapp.crud.crud import update
from webapp.db.postgres import get_session
from webapp.models.sirius.user import User
from webapp.schema.user import UserLogin, UserLoginResponse


@auth_router.post(
    '/update_user/{user_id}',
    response_model=UserLoginResponse,
)
async def update_user(user_id: int, body: UserLogin, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    updated = await update(session, user_id, body, User)

    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse({'id': updated.id, 'username': updated.username})
