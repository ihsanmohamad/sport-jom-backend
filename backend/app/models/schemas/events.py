from db.models import Event
from tortoise.contrib.pydantic import pydantic_model_creator
from models.schemas.tournament import Tournament_Pydantic
from pydantic import BaseModel

Event_Pydantic = pydantic_model_creator(Event, name="Event")
EventIn_Pydantic = pydantic_model_creator(Event, name="EventIn", exclude_readonly=True)

class EventResponse(Event_Pydantic):
    tournament_id: int
    facilities_id: int

class EventIn(EventIn_Pydantic):
    tournament_id: int
    facilities_id: int

class FacilitiesEvent(BaseModel):
    id: int
    name: str

class EventFull(Event_Pydantic):
    tournament: Tournament_Pydantic
    facilities: FacilitiesEvent