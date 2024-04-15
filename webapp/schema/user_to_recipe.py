from pydantic import BaseModel


class AssociationData(BaseModel):
    user_id: int
    recipe_id: int
