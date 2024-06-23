from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse

# from fastapi_pagination import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.recipe.router import recipe_router
from webapp.crud.get_recipe import get_user_recipes
from webapp.db.postgres import get_session
from webapp.models.sirius.recipe import Recipe
from webapp.schema.recipe import RecipesResponse
from webapp.crud.crud import get
from webapp.utils.recipe.ingredients_for_recipe import get_ingredients_for_recipe


@recipe_router.get(
    '/read_user_recipes/{user_id}',
    response_model=RecipesResponse,
)
async def read_user_recipes(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:

    user_recipes = await get_user_recipes(session, user_id)

    if user_recipes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No recipes found for this user')

    return ORJSONResponse(
        # paginate(
        [
            {
                'id': recipe.id,
                'title': recipe.title,
                'likes': recipe.likes,
                'user_id': recipe.user_id,
                'ingredients': await get_ingredients_for_recipe(session, recipe),
            }
            for recipe in user_recipes
        ]
        # )
    )
