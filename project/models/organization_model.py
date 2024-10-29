from pydantic import BaseModel
from typing import List, Dict

# Define the organization schema using Pydantic
class Organization(BaseModel):
    name: str
    description: str
    organization_members: List[Dict[str, str]]