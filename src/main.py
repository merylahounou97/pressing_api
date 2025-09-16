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

api_description = """
**Pressing API** est un backend **FastAPI** pour automatiser la gestion d’un service de pressing :
- 👥 Utilisateurs (clients, secrétaires, administrateurs), auth **JWT**, vérif **email/SMS**
- 📦 Catalogue d’articles (CRUD, recherche)
- 📜 Commandes (cycle de vie complet)
- 🧾 Facturation **HTML/PDF** + envoi par email
- ✉️ Notifications email & **Twilio** SMS
- 🚀 CI/CD GitHub Actions, déploiement Docker + **Traefik**

**Liens :**
- API : https://portefolio.ulrichaiounou.com/pressing_api
- Code : https://github.com/merylahounou97/pressing_api
"""

app = FastAPI(
    title="Pressing API",
    summary="API FastAPI pour gérer utilisateurs, catalogue, commandes et facturation d’un pressing.",
    description=api_description,
    version="1.0.0", 
    terms_of_service="https://github.com/merylahounou97/pressing_api#readme",  
    contact={
        "name": "Pressing API Team (Ulrich, Sem, Meryl)",
        "url": "https://github.com/merylahounou97/pressing_api",
        "email": "merylahounou@gmail.com"
    },
    license_info={
       
    },
    docs_url="/",  
    lifespan=initialize_app,
    generate_unique_id_function=generate_unique_function_id,
)

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
