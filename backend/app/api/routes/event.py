from fastapi import APIRouter, Depends, Body
from api.services import fastapi_users
from db.models import User, Event, Team
from models.schemas.common import Message
from models.schemas.events import Event_Pydantic, EventIn_Pydantic, EventResponse, EventIn, EventFull
from typing import List, Optional

router = APIRouter()

@router.post("",response_model=EventResponse, name="create_events")
async def create_events(
    events: EventIn,
    user: User = Depends(fastapi_users.get_current_active_user)
    ):
    events_obj = await Event.create(**events.dict())
    result_obj = await Event_Pydantic.from_tortoise_orm(events_obj)
    events_result = result_obj.dict()
    events_result['tournament_id'] = events.tournament_id
    events_result['facilities_id'] = events.facilities_id
    return events_result

@router.get("",name="get_all_events", )
async def get_events():
    events = await Event.all().prefetch_related('tournament', 'facilities', 'participants')
    response = []
    for event in events:
        data = {}
        data['id'] = event.id
        data['name'] = event.name
        data['tournament'] = {
            'id': event.tournament.id,
            'name': event.tournament.name
         }
        data['facilities'] = {
            'id': event.facilities.id,
            'name': event.facilities.name,
        }
        response.append(data)
    # return await Event_Pydantic.from_queryset(events)
    return response

@router.get("/{events_id}", response_model=EventFull, name="get_events_by_id")
async def get_events_by_id(events_id: int):
    events = await Event.filter(id=events_id).prefetch_related('tournament', 'facilities', 'participants').get()
    
    data = {}
    data['id'] = events.id
    data['name'] = events.name
    data['tournament'] = {
        'id': events.tournament.id,
        'name': events.tournament.name
        }
    data['facilities'] = {
        'id': events.facilities.id,
        'name': events.facilities.name,
    }
    # return await Event_Pydantic.from_queryset(events)
    return data

@router.patch("/{events_id}", response_model=Event_Pydantic, name="update events")
async def update_events(
    events_id: int, 
    events: EventIn_Pydantic,
    user: User = Depends(fastapi_users.get_current_active_user)):
    await Event.filter(id=events_id).update(**events.dict(exclude_unset=True))
    return await Event_Pydantic.from_queryset_single(Event.get(id=events_id))

@router.delete("/{events_id}", response_model=Message)
async def delete_events(events_id: int, user: User = Depends(fastapi_users.get_current_active_user)):
    events = await Event.filter(id=events_id).delete()
    return {"message": "Deleted successfully"}

@router.post("/team" ,tags=['team', 'event'])
async def create_event_team(event:int, teams: List[int], user: User = Depends(fastapi_users.get_current_active_user)):
    event = await Event.filter(id=event).get()
    team_list= []
    for team in teams:
        teams_to_add = await Team.filter(id=team).get()
        insert_related = await event.participants.add(teams_to_add)
        team_list.append(teams_to_add.id) 

    result ={}
    result['id'] = event.id
    result['name'] = event.name
    result['teams'] = team_list
    return result
    


    