from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.recipe.router import recipe_router
from webapp.crud.crud import update
from webapp.db.postgres import get_session
from webapp.models.sirius.recipe import Recipe
from webapp.schema.recipe import RecipeResponse, RecipeFields
from webapp.utils.recipe.ingredients_for_recipe import get_ingredients_for_recipe


@recipe_router.post(
    '/update/{recipe_id}',
    response_model=RecipeResponse,
)
async def update_recipe(
    recipe_id: int, body: RecipeFields, session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:

    data = {}
    if body.title:
        data['title'] = body.title
    if body.likes:
        data['likes'] = body.likes

    updated = await update(session, recipe_id, data, Recipe)

    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Recipe does not exist')

    return ORJSONResponse(
        # paginate(
        {
            'id': updated.id,
            'title': updated.title,
            'likes': updated.likes,
            'user_id': updated.user_id,
            'ingredients': await get_ingredients_for_recipe(session, updated),
        }
        # )
    )
