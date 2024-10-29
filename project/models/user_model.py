from pydantic import BaseModel

# Define the User schema using Pydantic
class User(BaseModel):
    name: str
    email: str
    password: bytes