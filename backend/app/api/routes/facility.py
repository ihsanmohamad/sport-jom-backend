from fastapi import APIRouter, Depends, HTTPException, status, Body
from api.services import fastapi_users
from db.models import User, Facility, Booking, BusinessUserModel, UserModel, Amenities
from models.schemas.facility import FacilityIn, Facility_Pydantic, FacilityIn_Pydantic, FacilityResponse, FacilityInResponse, FacilityUserResponse
from models.schemas.business import BusinessUser_Pydantic
from typing import Optional

router = APIRouter()

@router.get("/filter", name="get_by_filter")
async def get_facility_by_filter(name: Optional[str] = None, category: Optional[str] = None):
    if (name is None and category is None):
        return []
    elif (name and category is None) :
        facility =  Facility.all().filter(name__icontains=name)
        return await Facility_Pydantic.from_queryset(facility)
    elif (category and name is None) :
        facility =  Facility.all().filter(category__icontains=category)
        return await Facility_Pydantic.from_queryset(facility)
    elif (name and category):
        facility =  Facility.all().filter(category__icontains=category).filter(name__icontains=name)
        return await Facility_Pydantic.from_queryset(facility)
    

# @router.post("", response_model=FacilityInResponse, name="create_facility")
@router.post("", name="create_facility")
async def create_facility(
    facility: FacilityIn ,
    user: User = Depends(fastapi_users.get_current_active_user)):
    business_user = await BusinessUser_Pydantic.from_queryset_single(BusinessUserModel.get(user_id=user.id))
    business_obj = business_user.dict()
    
    facility_obj = await Facility.create(**facility.dict(exclude_unset=True), business_id=business_obj["id"])
    amenities_list = []
    if facility.amenities:
        for i in facility.amenities:
            amenities = await Amenities.get(id=i)
            insert_related = await facility_obj.amenity.add(amenities)
            amenities_list.append(amenities.name)

    result = await Facility_Pydantic.from_tortoise_orm(facility_obj)
    result_obj = result.dict()
    result_obj['amenities'] = amenities_list
    return result_obj

# @router.get("", response_model=FacilityResponse, name="get_facilities")
@router.get("", name="get_facilities")
async def get_facilities():
    facilities = Facility.all()
    
    return await Facility_Pydantic.from_queryset(facilities)
  

@router.get("/{facility_id}", response_model=FacilityUserResponse)
async def get_facility_by_id(facility_id:int):
    # facility = await Facility.filter(id=facility_id).values(business="business__name")
    # business = await Facility.all().prefetch_related('business').filter(business_id=1)
    business = await Facility.filter(id=facility_id).values('business_id')
    facility = await Facility.filter(id=facility_id).get()
    
    amenities = await facility.amenity.all()
    amenity_list = []
    for amenity in amenities:
        amenity_list.append(amenity.name)

    facility_data = await Facility_Pydantic.from_queryset_single(Facility.filter(id=facility_id).get())
    facility_obj = facility_data.dict()
    business_id = business[0]['business_id']
    business_detail = await BusinessUser_Pydantic.from_queryset_single(BusinessUserModel.get(id=business_id))
    business_obj = business_detail.dict()
    facility_obj['owner'] = business_obj
    facility_obj['amenities'] = amenity_list
    return facility_obj

# @router.patch("/{facility_id}", response_model=FacilityInResponse)
@router.patch("/{facility_id}")
async def update_facility(
    facility_id:int, 
    facility: FacilityIn_Pydantic,
    user: User = Depends(fastapi_users.get_current_active_user)
    ):
    await Facility.filter(id=facility_id).update(**facility.dict(exclude_unset=True))
    return await Facility_Pydantic.from_queryset_single(Facility.get(id=facility_id))

@router.delete("/{facility_id}")
async def delete_facility(facility_id: int, user: User = Depends(fastapi_users.get_current_active_user)):
    
    business_id = await get_facility_by_id(facility_id)

    business = await BusinessUserModel.filter(id=business_id['owner']['id']).get()
    
    user = await UserModel.filter(id=user.id).get()
    user_obj = await user.business.filter(user_id=user.id).get()
    if  business.pk == user_obj.pk:
        to_delete = await Facility.filter(id=facility_id, business_id=business.pk).delete()
        if not to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object does not exist")
            
        return {"message": "Deleted successfully"}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


