from db.models import BusinessUserModel, PublicUserModel, User, UserModel
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, HttpUrl
from typing import Optional


PublicUser_Pydantic = pydantic_model_creator(PublicUserModel, name="PublicUser")
UserModel_Pydantic = pydantic_model_creator(UserModel, name="UserModel", exclude_readonly=True)



class PublicUserIn(BaseModel):
    name: str
    profile_url: HttpUrl = "https://google.com"
    gender: str

class PublicUserFull(User):
    detail: Optional[PublicUser_Pydantic]



