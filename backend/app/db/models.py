from fastapi_users import models as fumodels
from tortoise import  models, fields
from typing import Optional, List
from slugify import slugify

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
    public: fields.OneToOneNullableRelation["PublicUserModel"]
    business: fields.OneToOneNullableRelation["BusinessUserModel"]

class PublicUserModel(models.Model):
    id = fields.BigIntField(pk=True)
    name: str = fields.CharField(max_length=255, null=True)
    profile_url: str = fields.CharField(max_length=255 ,null=True, default="https://google.com")
    gender: str = fields.CharField(max_length=50, null=True)
    # age = fields.IntField(null=True)

    booking: fields.ManyToManyRelation["Booking"] 
    team: fields.ManyToManyRelation["Team"]

    class Meta:
        table="public"

    user: fields.OneToOneNullableRelation[UserModel] = fields.OneToOneField("models.UserModel", related_name="public", on_delete=fields.CASCADE)
    
    def __str__(self):
        return self.name

class BusinessUserModel(models.Model):
    id = fields.BigIntField(pk=True)
    name: str = fields.CharField(max_length=255, null=True)
    profile_url: str = fields.CharField(max_length=255 ,null=True, default="https://google.com")
    
    # age = fields.IntField(null=True)

    facilities: fields.ReverseRelation["Facility"]

    class Meta:
        table="business"

    user: fields.OneToOneNullableRelation[UserModel] = fields.OneToOneField("models.UserModel", related_name="business", on_delete=fields.CASCADE)

    def __str__(self):
        return {self.name}

class OAuthAccountModel(TortoiseBaseOAuthAccountModel):
    class Meta:
        table="oauth_account"
    user = fields.ForeignKeyField("models.UserModel", related_name="oauth_accounts")

class Facility(models.Model):
    id = fields.BigIntField(pk=True)
    name:str = fields.CharField(max_length=255, null=True, unique=True)
    profile_pic: str = fields.CharField(max_length=255, null=True, default="https://google.com")
    category: str = fields.CharField(max_length=50, null=True)
    city = fields.CharField(max_length=255)
    street = fields.CharField(max_length=255)
    street2 = fields.CharField(max_length=255)
    postcode = fields.CharField(max_length=10)

    class Meta:
        table = 'facilities'

    booking: fields.ReverseRelation["Booking"]

    amenity: fields.ManyToManyRelation['Amenities'] = fields.ManyToManyField("models.Amenities", related_name="facilities", on_delete=fields.CASCADE)

    events: fields.ForeignKeyNullableRelation["Event"]

    business: fields.ForeignKeyRelation[BusinessUserModel] = fields.ForeignKeyField("models.BusinessUserModel", related_name="facilities", on_delete=fields.CASCADE)
    
    def __str__(self):
        return self.name

    def slug(self) -> str:
        """
        Returns slugify name
        """
        slugname = slugify(self.name)
        return slugname

    class PydanticMeta:
        computed = ["slug"]
        

class Amenities(models.Model):
    id = fields.BigIntField(pk=True)
    name:str = fields.CharField(max_length=255, null=True, unique=True)

    class Meta:
        table = 'amenities'

    def __str__(self):
        return self.name
    

    facilities: fields.ManyToManyRelation[Facility]
    
class Booking(models.Model):
    
    id = fields.BigIntField(pk=True)
    book_date = fields.DateField()
    book_status = fields.CharField(max_length=50)
    book_time = fields.DatetimeField()
    book_duration = fields.DatetimeField()

    payment: fields.ReverseRelation["Payment"]

    class Meta:
        table = 'booking'

    facilities : fields.ForeignKeyRelation[Facility] = fields.ForeignKeyField("models.Facility", related_name="booking")
    public: fields.ManyToManyRelation[PublicUserModel] = fields.ManyToManyField("models.PublicUserModel", related_name="booking", through="user_booking", forward_key="public_id")

    def __str__(self):
        return self.id

class Payment(models.Model):
    id = fields.BigIntField(pk=True)
    payment_status = fields.CharField(max_length=50)
    paid = fields.BooleanField(default=False)
    amount = fields.DecimalField(max_digits=7, decimal_places=2)
    booking: fields.ForeignKeyRelation[Booking] = fields.ForeignKeyField("models.Booking", related_name="payment")

class Tournament(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.TextField()

    events:fields.ReverseRelation["Event"]

    def __str__(self):
        return self.name

class Team(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    created_by = fields.BigIntField()
    events: fields.ManyToManyRelation["Event"]
    public: fields.ManyToManyRelation[PublicUserModel] = fields.ManyToManyField("models.PublicUserModel", related_name="team", through="user_team", forward_key="user_id")

    def __str__(self):
        return self.name

    class PydanticMeta:
        exclude=["created_by"]

class Event(models.Model):
    id = fields.BigIntField(pk=True)
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