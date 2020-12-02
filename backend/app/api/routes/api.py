from fastapi import APIRouter

from api.services import fastapi_users, google_oauth_client, jwt_authentication
from api.dependencies.users import on_after_forgot_password, on_after_register 

from api.routes import users, business, booking, facility, amenities, event, team, tournament, payment

from core.configs import SECRET

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)
router.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

google_oauth_router = fastapi_users.get_oauth_router(
    google_oauth_client, SECRET, after_register=on_after_register
)
router.include_router(google_oauth_router, prefix="/auth/google", tags=["auth"])

router.include_router(users.router, tags=["public user"], prefix="/public")
router.include_router(business.router, tags=["business user"], prefix="/business")
router.include_router(booking.router, tags=["booking"], prefix="/booking")
router.include_router(facility.router, tags=["facility"], prefix="/facility")
router.include_router(amenities.router, tags=["amenities"], prefix="/amenities")
router.include_router(event.router, tags=["event"], prefix="/event")
router.include_router(team.router, tags=["team"], prefix="/team")
router.include_router(tournament.router, tags=["tournament"], prefix="/tournament")
router.include_router(payment.router, tags=["payment"], prefix="/payment")
