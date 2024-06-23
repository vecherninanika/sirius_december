from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette import status

from webapp.api.auth.router import auth_router
from webapp.crud.crud import create
from webapp.db.postgres import get_session
from webapp.models.sirius.user import User
from webapp.schema.user import UserLogin, UserLoginResponse


@auth_router.post(
    '/register',
    response_model=UserLoginResponse,
)
async def register(body: UserLogin, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:

    try:
        user = await create(session, body, User)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'User with username {body.username} already exists'
        )

    return ORJSONResponse({'id': user.id, 'username': user.username})
