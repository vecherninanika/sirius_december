from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

# from fastapi_pagination import paginate

from webapp.api.recipe.router import recipe_router
from webapp.crud.get_ingredient_recipe import get_ingredient_recipe
from webapp.crud.get_ingredient import get_ingredient
from webapp.db.postgres import get_session
from webapp.models.sirius.recipe import Recipe
from webapp.schema.ingredient import IngredientData
from webapp.schema.recipe import RecipesResponse
from webapp.crud.crud import get
from webapp.utils.recipe.ingredients_for_recipe import get_ingredients_for_recipe


@recipe_router.get(
    '/find_by_ingredient',
    response_model=RecipesResponse,
)
async def find_by_ingredient(
    ingredient_title: IngredientData,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    ingredient = await get_ingredient(session, ingredient_title)

    if ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Ingredient {ingredient_title} not found')

    recipe_to_ingredient = await get_ingredient_recipe(session, ingredient.id)

    if recipe_to_ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No recipes found with this ingredient')

    recipes = []
    for elem in recipe_to_ingredient:
        recipe = await get(session, elem.recipe_id, Recipe)
        recipes.append(recipe)

    ingredients = await get_ingredients_for_recipe(session, recipe)

    return ORJSONResponse(
        # paginate(
        [
            {
                'id': recipe.id,
                'title': recipe.title,
                'likes': recipe.likes,
                'user_id': recipe.user_id,
                'ingredients': ingredients,
            }
            for recipe in recipes
        ]
        # )
    )
