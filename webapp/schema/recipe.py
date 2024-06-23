from typing import List, Optional
from pydantic import BaseModel


class RecipeData(BaseModel):
    title: str
    likes: Optional[int] = 0
    ingredients: List[str]
    username: Optional[int] = None


class CreateRecipe(BaseModel):
    title: str
    likes: Optional[int] = 0
    user_id: Optional[int] = None


class RecipeFields(BaseModel):
    title: Optional[str] = None
    likes: Optional[int] = None


class RecipeTitle(BaseModel):
    title: str


class RecipeIngredients(BaseModel):
    ingredients: List[str]


class RecipeIngredient(BaseModel):
    ingredient: str


class RecipeUser(BaseModel):
    username: int


class RecipeId(BaseModel):
    id: int


class RecipeResponse(BaseModel):
    id: int
    title: str
    likes: int
    user_id: int
    ingredients: Optional[List[str]] = None


class RecipesResponse(BaseModel):
    recipes: List[RecipeResponse]
