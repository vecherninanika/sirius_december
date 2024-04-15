from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    code: int


class UserLoginResponse(BaseModel):
    id: int
    username: str


class UserTokenResponse(BaseModel):
    access_token: str
