from pydantic import BaseModel
from typing import Union


class ProjectModel(BaseModel):
    name: str
    embeddings: Union[str, None] = None
    embeddings_model: Union[str, None] = None
    llm: Union[str, None] = None
