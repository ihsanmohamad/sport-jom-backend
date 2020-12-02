from db.models import Booking
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel

Booking_Pydantic = pydantic_model_creator(Booking, name="Booking")
BookingIn_Pydantic = pydantic_model_creator(Booking, name="BookingIn", exclude_readonly=True)

class BookingIn(BookingIn_Pydantic):
    facilities_id: int

class FacilitiesEvent(BaseModel):
    id: int
    name: str

class FacilitiesUser(BaseModel):
    id: int
    name: str

class BookingFull(Booking_Pydantic):
    facilities: FacilitiesEvent
    book_by: FacilitiesUser
