from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.ingredient.router import ingredient_router
from webapp.crud.crud import delete
from webapp.crud.get_ingredient_recipe import get_ingredient_recipe
from webapp.db.postgres import get_session
from webapp.models.sirius.ingredient import Ingredient
from webapp.models.sirius.ingredient_to_recipe import IngredientToRecipe
from webapp.schema.ingredient import IngredientData


@ingredient_router.post(
    '/delete/{ingredient_id}',
    response_model=IngredientData,
)
async def delete_ingredient(ingredient_id: int, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:

    association_objects = await get_ingredient_recipe(session, ingredient_id)
    id_ = association_objects[0].id

    if id_:
        await delete(session, id_, IngredientToRecipe)

    deleted_id = await delete(session, ingredient_id, Ingredient)

    if deleted_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Ingredient does not exist')

    return ORJSONResponse({'id': deleted_id})
