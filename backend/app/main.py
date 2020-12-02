from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.api import router as api_router
from tortoise.contrib.fastapi import register_tortoise
from core.configs import models, DB_URL
import uvicorn

def fastApp() -> FastAPI:
    app = FastAPI(title="SportJom", description="Backend for SportJom. Postgres as database")
    
    register_tortoise(
            app,
            db_url=DB_URL,
            modules={"models": models
            },
            generate_schemas=True,
            add_exception_handlers=True,
        )  

    app.include_router(api_router)

    origins = [
    "http://localhost",
    "http://localhost:8080",
    ]
    
    app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
    return app

app = fastApp()



if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)