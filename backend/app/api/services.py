from httpx_oauth.clients.google import GoogleOAuth2

from fastapi_users.db import TortoiseUserDatabase

from fastapi_users.authentication import JWTAuthentication
from fastapi_users import FastAPIUsers

from core.configs import SECRET, CLIENT_ID, CLIENT_SECRET

from db.models import User, UserCreate, UserUpdate, UserDB, UserModel, OAuthAccountModel

jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login"
)

google_oauth_client = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)


user_db = TortoiseUserDatabase(UserDB, UserModel, OAuthAccountModel)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB
)