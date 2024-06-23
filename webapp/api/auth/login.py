from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.auth.router import auth_router
from webapp.cache.redis import redis_set
from webapp.crud.get_user import get_user
from webapp.db.postgres import get_session
from webapp.schema.user import UserLogin, UserTokenResponse
from webapp.utils.auth.jwt import jwt_auth


@auth_router.post(
    '/login',
    response_model=UserTokenResponse,
)
async def login(
    body: UserLogin,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    user = await get_user(session, body.username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User {body.username} does not exist')

    if user.code != body.code:
        raise HTTPException(status_code=status.http_401_unauthorized, detail=f'{user.code} is not the correct code')

    token = jwt_auth.create_token(user.id)
    await redis_set('access_token', token)

    return ORJSONResponse(
        {
            'id': user.id,
            'username': user.username,
            'access_token': token,
        }
    )
