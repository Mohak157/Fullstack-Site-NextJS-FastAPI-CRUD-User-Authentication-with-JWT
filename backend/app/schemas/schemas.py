from pydantic import BaseModel
from fastapi_users import schemas 
import uuid

class CreatePost(BaseModel):
    title:str
    description:str

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass


