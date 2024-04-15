from pydantic import BaseModel


class FeedbackData(BaseModel):
    user_id: int
    recipe_id: int
    status: str
