from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import paginate

from webapp.api.recipe.router import recipe_router
from webapp.crud.get_ingredient_recipe import get_ingredient_recipe
from webapp.db.postgres import get_session
from webapp.models.sirius.recipe import Recipe
from webapp.schema.ingredient import IngredientData
from webapp.schema.recipe import RecipesResponse
from webapp.api.ingredient.read import read_ingredient
from webapp.crud.crud import get


@recipe_router.get(
    '/find_by_ingredient',
    response_model=RecipesResponse,
)
async def find_by_ingredient(
    ingredient: IngredientData,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    ingredient_id = (await read_ingredient(ingredient))['id']

    recipe_to_ingredient = await get_ingredient_recipe(session, ingredient_id)
    recipes = []
    for elem in recipe_to_ingredient:
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
