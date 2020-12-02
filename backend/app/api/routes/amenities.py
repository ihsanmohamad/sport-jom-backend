from fastapi import APIRouter, Depends
from api.services import fastapi_users
from db.models import User, Amenities
from models.schemas.common import Message
from models.schemas.amenities import Amenities_Pydantic, AmenitiesIn_Pydantic

router = APIRouter()

@router.post("",response_model=Amenities_Pydantic, name="create_amenity")
async def create_amenities(
    amenity: AmenitiesIn_Pydantic,
    user: User = Depends(fastapi_users.get_current_superuser)
    ):
    amenity_obj = await Amenities.create(**amenity.dict())
    return await Amenities_Pydantic.from_tortoise_orm(amenity_obj)

@router.get("", name="get_all_amenities")
async def get_amenities():
    amenities = Amenities.all()
    return await Amenities_Pydantic.from_queryset(amenities)

@router.get("/{amenity_id}", response_model=Amenities_Pydantic, name="get_amenities_by_id")
async def get_amenities_by_id(amenity_id: int):
    amenity = await Amenities.filter(id=amenity_id).get()
    result = {"id": amenity.id, "name": amenity.name}
    return result

@router.patch("/{amenity_id}", response_model=Amenities_Pydantic, name="update amenities")
async def update_amenities(
    amenity_id: int, 
    amenity: AmenitiesIn_Pydantic,
    user: User = Depends(fastapi_users.get_current_superuser)):
    await Amenities.filter(id=amenity_id).update(**amenity.dict(exclude_unset=True))
    return await Amenities_Pydantic.from_queryset_single(Amenities.get(id=amenity_id))

@router.delete("/{amenity_id}", response_model=Message)
async def delete_amenities(amenity_id: int, user: User = Depends(fastapi_users.get_current_superuser)):
    amenity = await Amenities.filter(id=amenity_id).delete()
    return {"message": "Deleted successfully"}