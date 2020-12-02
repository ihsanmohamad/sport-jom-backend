from fastapi_users import models as fumodels
from tortoise import  models, fields
from typing import Optional, List

from fastapi_users.db import (
    TortoiseBaseOAuthAccountModel,
    TortoiseBaseUserModel,
)

class TimestampMixin():
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

class User(fumodels.BaseUser, fumodels.BaseOAuthAccountMixin):
    is_business : bool = False
    

class UserCreate(fumodels.BaseUserCreate):
    is_business : bool = False

class UserUpdate(User, fumodels.BaseUserUpdate):
    pass

class UserDB(User, fumodels.BaseUserDB):
    pass

class UserModel(TortoiseBaseUserModel):

    is_business: bool = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    class Meta:
        table="user"
    detail: fields.ReverseRelation["UserDetailModel"]
    business_detail: fields.ReverseRelation["BusinessDetailModel"]

class UserDetailModel(models.Model):
    id = fields.IntField(pk=True)
    name: str = fields.CharField(max_length=255, null=True)
    profile_url: str = fields.CharField(max_length=255 ,null=True)
    gender: str = fields.CharField(max_length=50, null=True)
    # age = fields.IntField(null=True)

    booking: fields.ManyToManyRelation["Booking"] 

    class Meta:
        table="user_detail"

    user: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField("models.UserModel", related_name="detail", on_delete=fields.CASCADE)
    
    def __str__(self):
        return self.name

class BusinessDetailModel(models.Model):
    id = fields.IntField(pk=True)
    name: str = fields.CharField(max_length=255, null=True)
    profile_url: str = fields.CharField(max_length=255 ,null=True)
    
    # age = fields.IntField(null=True)

    facilities: fields.ReverseRelation["Facility"]

    class Meta:
        table="business_detail"

    user: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField("models.UserModel", related_name="business_detail", on_delete=fields.CASCADE)

    def __str__(self):
        return self.name

class OAuthAccountModel(TortoiseBaseOAuthAccountModel):
    class Meta:
        table="oauth_account"
    user = fields.ForeignKeyField("models.UserModel", related_name="oauth_accounts")

class Facility(models.Model):
    id = fields.IntField(pk=True)
    name:str = fields.CharField(max_length=255, null=True)
    profile_pic: str = fields.CharField(max_length=255, null=True)
    category: str = fields.CharField(max_length=50, null=True)
    city = fields.CharField(max_length=255)
    street = fields.CharField(max_length=255)
    street2 = fields.CharField(max_length=255)
    postcode = fields.IntField()
    

    class Meta:
        table = 'facilities'

    booking: fields.ReverseRelation["Booking"]

    amenities: fields.ManyToManyRelation['Amenities'] = fields.ManyToManyField("models.Amenities", related_name="facilities", on_delete=fields.CASCADE)

    events: fields.ForeignKeyNullableRelation["Event"]

    user: fields.ForeignKeyRelation[BusinessDetailModel] = fields.ForeignKeyField("models.BusinessDetailModel", related_name="facilities", on_delete=fields.CASCADE)
    
    def __str__(self):
        return self.name

class Amenities(models.Model):
    id = fields.IntField(pk=True)
    name:str = fields.CharField(max_length=255, null=True, unique=True)

    class Meta:
        table = 'amenities'

    def __str__(self):
        return self.name
    

    facilities: fields.ManyToManyRelation[Facility]
    
class Booking(models.Model):
    
    id = fields.IntField(pk=True)
    book_date = fields.DateField()
    book_status = fields.CharField(max_length=50)
    book_duration = fields.DatetimeField()

    payment: fields.ReverseRelation["Payment"]

    class Meta:
        table = 'booking'

    facilities : fields.ForeignKeyRelation[Facility] = fields.ForeignKeyField("models.Facility", related_name="booking")
    user: fields.ManyToManyRelation[UserDetailModel] = fields.ManyToManyField("models.UserDetailModel", related_name="booking", through="user_booking", forward_key="user_id")

    def __str__(self):
        return self.id

class Payment(models.Model):
    id = fields.IntField(pk=True)
    payment_status = fields.CharField(max_length=50)
    paid = fields.BooleanField(default=False)
    booking: fields.ForeignKeyRelation[Booking] = fields.ForeignKeyField("models.Booking", related_name="payment")

class Tournament(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    events:fields.ReverseRelation["Event"]

    def __str__(self):
        return self.name

class Team(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    events: fields.ManyToManyRelation["Event"]

    def __str__(self):
        return self.name


class Event(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    tournament: fields.ForeignKeyRelation[Tournament] = fields.ForeignKeyField(
        "models.Tournament", related_name="events"
    )
    participants: fields.ManyToManyRelation[Team] = fields.ManyToManyField(
        "models.Team", related_name="events", through="event_team"
    )

    facilities: fields.ForeignKeyNullableRelation[Facility] = fields.ForeignKeyField(
        "models.Facility", related_name="events"
    )

    def __str__(self):
        return self.name