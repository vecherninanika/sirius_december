from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from webapp.models.meta import DEFAULT_SCHEMA, Base


class UserToRecipe(Base):
    __tablename__ = 'user_to_recipe'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(f"{DEFAULT_SCHEMA}.user.id"))

    recipe_id: Mapped[int] = mapped_column(Integer, ForeignKey(f"{DEFAULT_SCHEMA}.recipe.id"))
