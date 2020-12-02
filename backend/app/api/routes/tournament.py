from fastapi import APIRouter, Depends
from api.services import fastapi_users
from db.models import User, Tournament
from models.schemas.common import Message
from models.schemas.tournament import Tournament_Pydantic, TournamentIn_Pydantic

router = APIRouter()

@router.post("",response_model=Tournament_Pydantic, name="create_tournament")
async def create_tournament(
    tournament: TournamentIn_Pydantic,
    user: User = Depends(fastapi_users.get_current_active_user)
    ):
    tournament_obj = await Tournament.create(**tournament.dict())
    return await Tournament_Pydantic.from_tortoise_orm(tournament_obj)

@router.get("", name="get_all_tournament")
async def get_tournament():
    tournament = Tournament.all()
    return await Tournament_Pydantic.from_queryset(tournament)

@router.get("/{tournament_id}", response_model=Tournament_Pydantic, name="get_tournament_by_id")
async def get_tournament_by_id(tournament_id: int):
    tournament = await Tournament.filter(id=tournament_id).get()
    result = {"id": tournament.id, "name": tournament.name}
    return result

@router.patch("/{tournament_id}", response_model=Tournament_Pydantic, name="update tournament")
async def update_tournament(
    tournament_id: int, 
    tournament: TournamentIn_Pydantic,
    user: User = Depends(fastapi_users.get_current_active_user)):
    await Tournament.filter(id=tournament_id).update(**tournament.dict(exclude_unset=True))
    return await Tournament_Pydantic.from_queryset_single(Tournament.get(id=tournament_id))

@router.delete("/{tournament_id}", response_model=Message)
async def delete_tournament(tournament_id: int, user: User = Depends(fastapi_users.get_current_active_user)):
    tournament = await Tournament.filter(id=tournament_id).delete()
    return {"message": "Deleted successfully"}