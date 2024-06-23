from pydantic import BaseModel
from typing import List, Optional


class UserLogin(BaseModel):
    username: int
    code: Optional[int] = None


class UserLoginResponse(BaseModel):
    id: int
    username: int


class UserTokenResponse(BaseModel):
    access_token: str


class UsersResponse(BaseModel):
    recipes: List[UserLoginResponse]
