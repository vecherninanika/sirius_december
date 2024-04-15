from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.recipe.router import recipe_router
from webapp.crud.crud import create, get
from webapp.crud.get_user import get_user
from webapp.db.postgres import get_session
from webapp.models.sirius.user_to_recipe import UserToRecipe
from webapp.models.sirius.recipe import Recipe
from webapp.schema.user_to_recipe import AssociationData
from webapp.schema.recipe import RecipeUser, RecipeResponse


@recipe_router.post(
    '/add_user/{recipe_id}',
    response_model=RecipeResponse,
)
async def add_user(
    recipe_id: int, body: RecipeUser, session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:

    user = await get_user(session, body.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'User {body.user} does not exist'
        )

    recipe = await get(session, recipe_id, Recipe)

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Recipe {recipe_id} does not exist'
        )

    data = AssociationData(user_id=user.id, recipe_id=recipe.id)
    await create(session, data, UserToRecipe)

    return ORJSONResponse({'id': recipe.id, 'title': recipe.title})
