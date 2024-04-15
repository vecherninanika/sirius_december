from fastapi import Depends
from fastapi.responses import ORJSONResponse
# from fastapi_pagination import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.recipe.router import recipe_router
from webapp.crud.get_recipe import get_sorted_recipes
from webapp.db.postgres import get_session
from webapp.schema.recipe import RecipesResponse


@recipe_router.get(
    '/read_popular',
    response_model=RecipesResponse,
)
async def read_popular(
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    recipes = await get_sorted_recipes(session, 10)

    return ORJSONResponse(
        # paginate(  # TODO
            [{'id': recipe.id,
              'title': recipe.title,
              'likes': recipe.likes}
             for recipe in recipes]
        # )
    )
