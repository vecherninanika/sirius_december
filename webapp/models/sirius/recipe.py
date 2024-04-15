from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from webapp.models.meta import DEFAULT_SCHEMA, Base


class Recipe(Base):
    __tablename__ = 'recipe'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String, unique=True)

    likes: Mapped[int] = mapped_column(Integer, default=0)

