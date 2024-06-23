from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse

# from fastapi_pagination import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.recipe.router import recipe_router
from webapp.crud.get_recipe import get_sorted_recipes
from webapp.db.postgres import get_session
from webapp.schema.recipe import RecipesResponse
from webapp.utils.recipe.ingredients_for_recipe import get_ingredients_for_recipe


@recipe_router.get(
    '/read_popular',
    response_model=RecipesResponse,
)
async def read_popular(
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:

    recipes = await get_sorted_recipes(session, 10)

    if recipes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No recipes found')

    return ORJSONResponse(
        # paginate(  # TODO
        [
            {
                'id': recipe.id,
                'title': recipe.title,
                'likes': recipe.likes,
                'user_id': recipe.user_id,
                'ingredients': await get_ingredients_for_recipe(session, recipe),
            }
            for recipe in recipes
        ]
        # )
    )
