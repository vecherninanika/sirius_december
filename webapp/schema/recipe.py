from typing import List, Optional

from pydantic import BaseModel


class RecipeData(BaseModel):
    title: str
    likes: Optional[int] = None
    ingredients: List[str]
    user: Optional[int] = None


class RecipeField(BaseModel):
    title: Optional[str] = None
    likes: Optional[int] = None


class RecipeTitle(BaseModel):
    title: str


class RecipeIngredients(BaseModel):
    ingredients: List[str]


class RecipeIngredient(BaseModel):
    ingredient: str


class RecipeUser(BaseModel):
    username: str


class RecipeId(BaseModel):
    id: int


class RecipeResponse(BaseModel):
    id: int
    title: str
    likes: int


class RecipesResponse(BaseModel):
    recipes: List[RecipeResponse]
