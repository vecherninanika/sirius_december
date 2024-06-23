from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette import status

from webapp.api.recipe.add_ingredient import add_ingredient
from webapp.api.recipe.router import recipe_router
from webapp.crud.crud import create
from webapp.db.postgres import get_session
from webapp.models.sirius.recipe import Recipe
from webapp.schema.recipe import RecipeData, RecipeIngredient, RecipeResponse, CreateRecipe
from webapp.schema.user import UserLogin
from webapp.crud.get_user import get_user


@recipe_router.post('/create', response_model=RecipeResponse)
async def create_recipe(body: RecipeData, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:

    data = CreateRecipe(title=body.title, likes=body.likes)

    if body.username is not None:
        user = await get_user(session, body.username)
        # data.user_id=user.id
        data = CreateRecipe(title=body.title, likes=body.likes, user_id=user.id)

    try:
        recipe = await create(session, data, Recipe)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'Recipe with title {body.title} already exists'
        )

    for ingredient_title in body.ingredients:
        ingredient = RecipeIngredient(ingredient=ingredient_title)
        await add_ingredient(recipe.id, ingredient, session)

    return ORJSONResponse(
        {
            'id': recipe.id,
            'title': recipe.title,
            'likes': recipe.likes,
            'user_id': recipe.user_id,
            'ingredients': body.ingredients,
        }
    )
