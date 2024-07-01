from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth import auth_router
from src.config import Settings
from src.lifespans.create_default_admin import create_default_admin_lifespan
from .users import users_router
from .users import member_router
from .database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

settings = Settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/",lifespan=create_default_admin_lifespan)

# Configurer les paramètres CORS
origins = [
    "http://localhost:5173",
    # vous pouvez ajouter d'autres origines si nécessaire
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/files", StaticFiles(directory="src/static/"), name="static")

app.include_router(member_router.router)
app.include_router(users_router.router)
app.include_router(auth_router.router)
