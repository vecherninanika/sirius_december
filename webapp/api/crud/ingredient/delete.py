from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.ingredient.router import ingredient_router
from webapp.crud.crud import delete
from webapp.db.postgres import get_session
from webapp.schema.ingredient import IngredientData
from webapp.models.sirius.ingredient import Ingredient


@ingredient_router.post(
    '/delete/{ingredient_id}',
    response_model=IngredientData,
)
async def delete_ingredient(
    ingredient_id: int,
    session: AsyncSession = Depends(get_session)
    ) -> ORJSONResponse:
    deleted_id = await delete(session, ingredient_id, Ingredient)
    
    if deleted_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
    return ORJSONResponse(
        {
            'id': deleted_id
        }
    )

