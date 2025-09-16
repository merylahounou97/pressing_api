from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from src.auth import auth_router
from src.config import Settings
from src.lifespans.create_default_admin import initialize_app
from .users import users_router
from .users import member_router
from .order import order_router
from .catalog import catalog_router
from .invoice import invoice_router
from .database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

settings = Settings()


Base.metadata.create_all(bind=engine)


def generate_unique_function_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title="Pressing API",
    docs_url="/",
    lifespan=initialize_app,
    generate_unique_id_function=generate_unique_function_id,
)

# Configurer les paramètres CORS
origins = [
    "http://localhost:5173",
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
app.include_router(order_router.router)
app.include_router(catalog_router.router)
app.include_router(invoice_router.router)
