from fastapi import Depends, HTTPException, Query
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

# from fastapi_pagination import paginate

from webapp.api.recipe.router import recipe_router
from webapp.crud.crud import get_all
from webapp.crud.get_recipe import get_recipe
from webapp.db.postgres import get_session
from webapp.models.sirius.recipe import Recipe
from webapp.schema.recipe import RecipeResponse, RecipesResponse, RecipeTitle
from webapp.utils.recipe.ingredients_for_recipe import get_ingredients_for_recipe


@recipe_router.get(
    '/read',
    response_model=RecipeResponse,
)
async def read_recipe(
    body: RecipeTitle,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    recipe = await get_recipe(session, body)

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    ingredients = await get_ingredients_for_recipe(session, recipe)

    return ORJSONResponse(
        # paginate(
        {
            'id': recipe.id,
            'title': recipe.title,
            'likes': recipe.likes,
            'user_id': recipe.user_id,
            'ingredients': ingredients,
        }
        # )
    )


@recipe_router.get(
    '/read_all',
    response_model=RecipesResponse,
)
async def read_recipes(
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:

    recipes = await get_all(session, Recipe)

    if recipes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No recipes found')

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
            for recipe in recipes
        ]
        # )
    )
