from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.recipe.router import recipe_router
from webapp.crud.crud import delete
from webapp.crud.get_ingredient_recipe import get_ingredient_recipe
from webapp.db.postgres import get_session
from webapp.models.sirius.ingredient_to_recipe import IngredientToRecipe
from webapp.models.sirius.recipe import Recipe
from webapp.schema.recipe import RecipeData


@recipe_router.post(
    '/delete/{recipe_id}',
    response_model=RecipeData,
)
async def delete_recipe(recipe_id: int, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:

    association_objects = await get_ingredient_recipe(session, recipe_id)
    id_ = association_objects[0].id

    if id_:
        await delete(session, id_, IngredientToRecipe)

    deleted_id = await delete(session, recipe_id, Recipe)

    if deleted_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Recipe {recipe_id} does not exist')

    return ORJSONResponse({'id': deleted_id})
