from fastapi import APIRouter, Depends, Body
from api.services import fastapi_users
from db.models import User, Booking, PublicUserModel
from models.schemas.common import Message
from models.schemas.booking import Booking_Pydantic, BookingIn_Pydantic, BookingIn, BookingFull

router = APIRouter()

@router.post("", response_model=BookingFull, name="create_booking")
async def create_booking(
    booking: BookingIn,
    user: User = Depends(fastapi_users.get_current_active_user)
    ):
    booking_obj = await Booking.create(**booking.dict())
    result_obj = await Booking_Pydantic.from_tortoise_orm(booking_obj)
    booking_result = result_obj.dict()
    
    data = await Booking.filter(id=booking_obj.id).prefetch_related('facilities').get()

    booking_result['facilities'] = {
        'id': data.facilities.id,
        'name': data.facilities.name
    }
    
    public_user = await PublicUserModel.filter(user_id=user.id).get()
    insert_related = await booking_obj.public.add(public_user)
    

    public = await PublicUserModel.filter(booking__id=booking_obj.id).get()


    booking_result['book_by'] = {
        'id': public.id,
        'name': public.name
    }
    return booking_result

@router.get("",name="get_all_booking", )
async def get_booking( user: User = Depends(fastapi_users.get_current_active_user)):
    public = await PublicUserModel.filter(user_id=user.id).get()
    booking = await Booking.filter(public__id=public.id).all().prefetch_related('payment', 'facilities', 'public')
    response = []
    for book in booking:
        data = {}
        data['id'] = book.id
        data['book_date'] = book.book_date
        data['book_duration'] = book.book_duration
        data['book_status'] = book.book_status
        data['book_time'] = book.book_time
        
        response.append(data)
    # return await Booking_Pydantic.from_queryset(booking)
    return response

@router.get("/{booking_id}" , response_model=BookingFull, name="get_booking_by_id")
async def get_booking_by_id(booking_id: int):
    booking = await Booking.filter(id=booking_id).prefetch_related('public', 'facilities', 'payment').get()
    data = {}
    data['id'] = booking.id
    data['book_date'] = booking.book_date
    data['book_status'] = booking.book_status
    data['book_time'] = booking.book_time
    data['book_duration'] = booking.book_duration
    data['facilities'] = {
        'id': booking.facilities.id,
        'name': booking.facilities.name,
    }
    public = await PublicUserModel.filter(booking__id=booking_id).get()
    
    
    data['book_by'] = {
        'id': public.id,
        'name': public.name
    }
    
    # return await Booking_Pydantic.from_queryset(booking)
    return data

@router.patch("/{booking_id}", name="update booking")
async def update_booking(
    booking_id: int, 
    booking: BookingIn_Pydantic,
    user: User = Depends(fastapi_users.get_current_active_user)):
    await Booking.filter(id=booking_id).update(**booking.dict(exclude_unset=True))
    return await Booking_Pydantic.from_queryset_single(Booking.get(id=booking_id))

@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: User = Depends(fastapi_users.get_current_active_user)):
    booking = await Booking.filter(id=booking_id).delete()
    return {"message": "Deleted successfully"}