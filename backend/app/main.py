from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.api import router as api_router
from tortoise.contrib.fastapi import register_tortoise
from core.configs import models, DB_URL, HOST_URL, ORIGINS
import uvicorn

def fastApp() -> FastAPI:
    app = FastAPI(title="SportJom", description="""
    Backend for SportJom. 
    Postgres as database 
    auth/google/authorize scope need profile and email

    scopes = profile , email
    """)
    
    register_tortoise(
            app,
            db_url=DB_URL,
            modules={"models": models
            },
            generate_schemas=True,
            add_exception_handlers=True,
        )  

    app.include_router(api_router)

    # origins = [
    # "http://localhost",
    # "http://localhost:8100",
    # "http://192.168.1.5",
    # "http://192.168.1.5:8100",
    # ]
    
    app.add_middleware(
    CORSMiddleware,
    allow_origins= ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
    return app

app = fastApp()



if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST_URL, port=8000, reload=True)