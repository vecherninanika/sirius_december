from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from webapp.models.meta import DEFAULT_SCHEMA, Base


class IngredientToRecipe(Base):
    __tablename__ = 'ingredient_to_recipe'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    ingredient_id: Mapped[int] = mapped_column(Integer, ForeignKey(f"{DEFAULT_SCHEMA}.ingredient.id"))

    recipe_id: Mapped[int] = mapped_column(Integer, ForeignKey(f"{DEFAULT_SCHEMA}.recipe.id"))
