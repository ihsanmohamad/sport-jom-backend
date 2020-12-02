from db.models import BusinessUserModel, PublicUserModel, User, UserModel,Facility
from models.schemas.business import BusinessUser_Pydantic
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, HttpUrl
from typing import Optional, List


Facility_Pydantic = pydantic_model_creator(Facility, name="Facility")
FacilityIn_Pydantic = pydantic_model_creator(Facility, name="FacilityIn", exclude_readonly=True)

class FacilityIn(FacilityIn_Pydantic):
    amenities: Optional[List] = None


class FacilityInResponse(Facility_Pydantic):
    slug: str
    

class FacilityResponse(Facility_Pydantic):
    slug: str
    business_id: int

class FacilityUserResponse(Facility_Pydantic):
    slug: str
    owner: BusinessUser_Pydantic
    amenities: Optional[List]



