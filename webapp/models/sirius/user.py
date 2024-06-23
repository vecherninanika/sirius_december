from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from webapp.models.meta import DEFAULT_SCHEMA, Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    username: Mapped[int] = mapped_column(Integer, unique=True)

    code: Mapped[int] = mapped_column(Integer, unique=True)
