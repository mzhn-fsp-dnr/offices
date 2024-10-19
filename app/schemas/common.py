from pydantic import BaseModel
from typing import List

class CommonList(BaseModel):
    ids: List[str]