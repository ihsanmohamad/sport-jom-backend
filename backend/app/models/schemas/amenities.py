from db.models import Amenities
from tortoise.contrib.pydantic import pydantic_model_creator

Amenities_Pydantic = pydantic_model_creator(Amenities, name="Amenities")
AmenitiesIn_Pydantic = pydantic_model_creator(Amenities, name="AmenitiesIn", exclude_readonly=True)