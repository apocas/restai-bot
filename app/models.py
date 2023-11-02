from pydantic import BaseModel
from typing import Union


class ChallengeModel(BaseModel):
    token: str
    challenge: str
    type: str

class ProjectModel(BaseModel):
    name: str
    embeddings: Union[str, None] = None
    embeddings_model: Union[str, None] = None
    llm: Union[str, None] = None
