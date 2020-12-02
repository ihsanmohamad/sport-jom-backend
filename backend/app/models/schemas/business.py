from db.models import BusinessUserModel, PublicUserModel, User, UserModel
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, HttpUrl
from typing import Optional

BusinessUser_Pydantic = pydantic_model_creator(BusinessUserModel, name="BusinessUser")
BusinessUserIn_Pydantic = pydantic_model_creator(BusinessUserModel, name="BusinessUserIn", exclude_readonly=True)

class BusinessUserIn(BaseModel):
    name: str
    profile_url: HttpUrl

class BusinessUserFull(User):
    detail: Optional[BusinessUser_Pydantic]