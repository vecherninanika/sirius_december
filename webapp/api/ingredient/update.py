from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.ingredient.router import ingredient_router
from webapp.crud.crud import update
from webapp.db.postgres import get_session
from webapp.models.sirius.ingredient import Ingredient
from webapp.schema.ingredient import IngredientData, IngredientResponse


@ingredient_router.post(
    '/update/{ingredient_id}',
    response_model=IngredientResponse,
)
async def update_ingredient(
    ingredient_id: int, body: IngredientData, session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:
    updated = await update(session, ingredient_id, body.dict(), Ingredient)

    if updated.id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Ingredient "{body.title}" does not exist')

    return ORJSONResponse({'id': updated.id, 'title': updated.title})
