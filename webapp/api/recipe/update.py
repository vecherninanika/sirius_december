from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.recipe.router import recipe_router
from webapp.crud.crud import update
from webapp.db.postgres import get_session
from webapp.models.sirius.recipe import Recipe
from webapp.schema.recipe import RecipeResponse, RecipeField


@recipe_router.post(
    '/update/{recipe_id}',
    response_model=RecipeResponse,
)
async def update_recipe(
    recipe_id: int, body: RecipeField, session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:
    updated = await update(session, recipe_id, body, Recipe)

    if updated.id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse({'id': updated.id, 'title': updated.title, 'likes': updated.likes})
