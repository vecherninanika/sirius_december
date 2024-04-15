from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.metrics import async_integrations_timer
from webapp.models.sirius.user_to_recipe import UserToRecipe


@async_integrations_timer
async def get_user_recipe(
    session: AsyncSession, user_id: int = None, recipe_id: int = None
) -> Sequence[UserToRecipe] | None:
    if user_id:
        query = UserToRecipe.user_id == user_id
    elif recipe_id:
        query = UserToRecipe.recipe_id == recipe_id
    return (await session.scalars(select(UserToRecipe).where(query))).all()
