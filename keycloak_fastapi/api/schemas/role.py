from pydantic import BaseModel
from typing import Optional

class RoleRepresentation(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
