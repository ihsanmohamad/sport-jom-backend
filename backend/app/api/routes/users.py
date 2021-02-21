from models.schemas.users import (
    PublicUser_Pydantic, PublicUserFull, 
    UserModel_Pydantic, UserModel, PublicUserIn)

from api.services import fastapi_users
from db.models import PublicUserModel, User, Team

from fastapi import APIRouter, Depends

router = APIRouter()

# @router.get("", response_model=PublicUserIn_Pydantic, name="user_detail")
# async def get_user_detail(user: User = Depends(fastapi_users.get_current_active_user) ):
#     return user.id


@router.get("", response_model=PublicUserFull ,  name="user_detail")
async def get_user_detail(user: User = Depends(fastapi_users.get_current_active_user)):
    detail = await PublicUser_Pydantic.from_queryset_single(PublicUserModel.get(user_id=user.id))
    user_obj = user.dict()
    user_obj['detail'] = detail
    # user["detail"] = detail
    return user_obj

@router.post("", response_model=PublicUser_Pydantic, name="set_user_detail")
async def set_user_detail(
    user_detail: PublicUserIn,
    user: User = Depends(fastapi_users.get_current_active_user) ,
): 
    user_obj = await PublicUserModel.create(**user_detail.dict(), user_id=user.id)
    return await PublicUser_Pydantic.from_tortoise_orm(user_obj)

@router.patch("", response_model=PublicUserIn, name="update_user_detail")
async def update_user_detail( public:PublicUserIn, user: User = Depends(fastapi_users.get_current_active_user)):
    await PublicUserModel.filter(user_id=user.id).update(**public.dict(exclude_unset=True))
    return await PublicUser_Pydantic.from_queryset_single(PublicUserModel.get(user_id=user.id))

@router.post("/join-team", name="user team")
async def join_team(team_id: int, user: User = Depends(fastapi_users.get_current_active_user)):
    public_user = await PublicUser_Pydantic.from_queryset_single(PublicUserModel.get(user_id=user.id))
    public_data = await PublicUserModel.get(user_id=user.id)
    team_obj = await Team.filter(id=team_id).get()
    insert_related = await team_obj.public.add(public_data)

    
    members = await team_obj.public.all()
    member_list = []
    for member in members:
        member_data = {"id": member.id, "name": member.name}
        member_list.append(member_data)
    result = {"id": team_obj.id, "name": team_obj.name, "members": member_list}
    return result

@router.delete("/leave-team", name="leave team")
async def delete_team(team_id: int, user: User = Depends(fastapi_users.get_current_active_user)):
    public_user = await PublicUser_Pydantic.from_queryset_single(PublicUserModel.get(user_id=user.id))
    public_data = await PublicUserModel.get(user_id=user.id)
    team_obj = await Team.filter(id=team_id).get()
    delete_related = await team_obj.public.remove(public_data)

    
    members = await team_obj.public.all()
    member_list = []
    for member in members:
        member_data = {"id": member.id, "name": member.name}
        member_list.append(member_data)
    result = {"id": team_obj.id, "name": team_obj.name, "members": member_list}
    return result

@router.get("/team", name="get team")
async def get_team(user: User = Depends(fastapi_users.get_current_active_user)):
    return {"otw"}