from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

from fastapi_mail import ConnectionConfig


config = Config(".env")

models = ["db.models", "aerich.models"]

# HOST URL
HOST_URL = config("HOST_URL")

# CORS ORIGIN
ORIGINS = config("CORS_ORIGINS", cast=CommaSeparatedStrings)

# DB
DB_URL = config("DB_CONNECTION")

# main
SECRET = config("SECRET_KEY")

# oauth
CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")

# Email setting
email_conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM = config("MAIL_FROM"),
    MAIL_PORT = config("MAIL_PORT"),
    MAIL_SERVER = config("MAIL_SERVER"),
    MAIL_FROM_NAME = config("MAIL_FROM_NAME"),
    MAIL_TLS = config("MAIL_TLS"),
    MAIL_SSL = config("MAIL_SSL")
)

# aerich config
TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": models,
            "default_connection": "default",
        },
    },
}

    
