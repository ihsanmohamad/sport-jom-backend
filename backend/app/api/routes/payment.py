from fastapi import APIRouter, Depends, Query
from api.services import fastapi_users
from db.models import User
from typing import List, Optional

router = APIRouter()

@router.post("")
async def create_payment(user: User = Depends(fastapi_users.get_current_active_user)):
    return {"otw"}

@router.get("")
async def get_payment(user: User = Depends(fastapi_users.get_current_active_user)):
    return {"otw"}

@router.get("/{payment_id}")
async def get_payment_by_id(q: Optional[List[str]] = Query(None, deprecated=True), user: User = Depends(fastapi_users.get_current_active_user) ):
    query_items = {"q": q}
    return query_items

# @router.patch("{payment_id}")
# async def update_booking(user: User = Depends(fastapi_users.get_current_active_user)):
#     return {"otw"}

# @router.delete("{booking_id}")
# async def delete_booking(user: User = Depends(fastapi_users.get_current_active_user)):
#     return {"otw"}