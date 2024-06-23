from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from webapp.models.sirius.recipe import Recipe
from webapp.models.sirius.ingredient import Ingredient
from webapp.crud.get_ingredient_recipe import get_ingredient_recipe
from webapp.crud.crud import get


async def get_ingredients_for_recipe(session: AsyncSession, recipe: Recipe) -> List[str]:
    association_objects = await get_ingredient_recipe(session, recipe_id=recipe.id)

    ingredients = []
    for obj in association_objects:
        id_ = obj.ingredient_id
        ingredient = await get(session, id_, Ingredient)
        ingredients.append(ingredient.title)

    return ingredients
