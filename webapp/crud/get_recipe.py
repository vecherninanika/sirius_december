from typing import Sequence, Any

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.metrics import async_integrations_timer
from webapp.models.sirius.recipe import Recipe
from webapp.schema.recipe import RecipeData
from sqlalchemy import desc


@async_integrations_timer
async def get_recipe(session: AsyncSession, recipe_data: RecipeData) -> Recipe | None:
    return (
        await session.scalars(
            select(Recipe)
            .where(Recipe.title == recipe_data.title))
    ).one_or_none()


@async_integrations_timer
async def get_sorted_recipes(session: AsyncSession, recipe_limit: int) \
        -> Sequence[Row | RowMapping | Any] | None:
    return (
        await session.scalars(
            select(Recipe)
            .order_by(desc(Recipe.Entry.likes))
            .limit(recipe_limit))
    ).all()
