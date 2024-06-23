from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.auth.router import auth_router
from webapp.crud.crud import get_all
from webapp.db.postgres import get_session
from webapp.schema.user import UsersResponse
from webapp.models.sirius.user import User


@auth_router.get(
    '/read_all',
    response_model=UsersResponse,
)
async def read_users(
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    users = await get_all(session, User)

    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'There are no users')

    return ORJSONResponse(
        # paginate(
        [
            {
                'id': user.id,
                'username': user.username,
            }
            for user in users
        ]
        # )
    )
