from fastapi import APIRouter, Depends
from api.services import fastapi_users
from db.models import User, Team, UserModel, PublicUserModel
from models.schemas.common import Message
from models.schemas.users import PublicUser_Pydantic
from models.schemas.team import Team_Pydantic, TeamIn_Pydantic

router = APIRouter()

@router.post("", response_model=Team_Pydantic, name="create_team")
async def create_team(
    team: TeamIn_Pydantic,
    user: User = Depends(fastapi_users.get_current_active_user)
    ):
    public_user = await PublicUser_Pydantic.from_queryset_single(PublicUserModel.get(user_id=user.id))
    public_data = await PublicUserModel.get(user_id=user.id)
    user_data = public_user.dict()
    team_obj = await Team.create(**team.dict(), created_by=user_data['id'])
    insert_related = await team_obj.public.add(public_data)
    return await Team_Pydantic.from_tortoise_orm(team_obj)

@router.get("", name="get_all_team")
async def get_team():
    team = Team.all()
    return await Team_Pydantic.from_queryset(team)

@router.get("/{team_id}", response_model=Team_Pydantic, name="get_team_by_id")
async def get_team_by_id(team_id: int):
    team = await Team.filter(id=team_id).get()
    result = {"id": team.id, "name": team.name}
    return result

@router.patch("/{team_id}", response_model=Team_Pydantic, name="update team")
async def update_team(
    team_id: int, 
    team: TeamIn_Pydantic,
    user: User = Depends(fastapi_users.get_current_active_user)):
    await Team.filter(id=team_id).update(**team.dict(exclude_unset=True))
    return await Team_Pydantic.from_queryset_single(Team.get(id=team_id))

@router.delete("/{team_id}", response_model=Message)
async def delete_team(team_id: int, user: User = Depends(fastapi_users.get_current_active_user)):
    team = await Team.filter(id=team_id).delete()
    return {"message": "Deleted successfully"}