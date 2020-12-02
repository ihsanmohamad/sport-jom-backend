from models.schemas.business import (
    BusinessUser_Pydantic, BusinessUserFull, BusinessUserIn_Pydantic, BusinessUserModel, BusinessUserIn
)
from api.services import fastapi_users
from db.models import BusinessUserModel, User


from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post("", response_model=BusinessUser_Pydantic, name="set_business_detail")
async def set_business_detail(
    business_detail: BusinessUserIn,
    business: User = Depends(fastapi_users.get_current_active_user) ,
): 
    if business.is_business:
        business_obj = await BusinessUserModel.create(**business_detail.dict(), user_id=business.id)
        return await BusinessUser_Pydantic.from_tortoise_orm(business_obj)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.get("", response_model=BusinessUserFull,  name="business_detail")
async def get_business_detail(business: User = Depends(fastapi_users.get_current_active_user)):
    if business.is_business:
        detail = await BusinessUser_Pydantic.from_queryset_single(BusinessUserModel.get(user_id=business.id))
        business_obj = business.dict()
        business_obj['detail'] = detail
        
        return business_obj
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.patch("", response_model=BusinessUserIn, name="update_business_detail")
async def update_business_detail( business: BusinessUserIn ,user: User = Depends(fastapi_users.get_current_active_user)):
    await BusinessUserModel.filter(user_id=user.id).update(**business.dict(exclude_unset=True))
    return await BusinessUser_Pydantic.from_queryset_single(BusinessUserModel.get(user_id=user.id))