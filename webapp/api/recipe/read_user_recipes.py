from fastapi import Depends
from fastapi.responses import ORJSONResponse
# from fastapi_pagination import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.user.router import auth_router
from webapp.crud.get_user_recipe import get_user_recipe
from webapp.db.postgres import get_session
from webapp.models.sirius.recipe import Recipe
from webapp.schema.recipe import RecipesResponse
from webapp.crud.crud import get


@auth_router.get(
    '/read_user_recipes/{user_id}',
    response_model=RecipesResponse,
)
async def read_user_recipes(
        user_id: int, session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:

    association_elems = await get_user_recipe(session, user_id)
    recipes = []
    for elem in association_elems:
        recipe = await get(session, elem.recipe_id, Recipe)
        recipes.append(recipe)

    return ORJSONResponse(
        # paginate(
            [{'id': recipe.id,
              'title': recipe.title,
              'likes': recipe.likes}
             for recipe in recipes]
        # )
    )
