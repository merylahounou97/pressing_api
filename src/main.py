from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth import auth_router
from src.config import Settings
from src.customer.customer_schema import Customer_create_input
from src.mail import mail_service
from src.person.person_schema import Person, Phone_number

from .customer import customer_router
from .database import Base, engine

settings = Settings()

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.mount("/files", StaticFiles(directory="src/static/"), name="static")

app.include_router(customer_router.router)
app.include_router(auth_router.router)


@app.get("/")
def main_page():
    return "Ceci est un pressing de wash man"


@app.get("/mail")
async def test_mail():
    meryl = Person(
        email=Customer_create_input.email,
        first_name=Customer_create_input.first_name,
        last_name=Customer_create_input.last_name,
        address=Customer_create_input.address,
        phone_number=Phone_number(
            dial_code=Customer_create_input.phone_number.dial_code,
            iso_code=Customer_create_input.phone_number.iso_code,
            phone_text=Customer_create_input.phone_number.phone_text,
        ),
    )
    return await mail_service.send_welcome_email(person=meryl)
    # return await mail_service.send_email(meryl.email,"aboo","shjdhf")


# @app.post("/customers", response_model=Customer_schema)
# def create_customers(customer: Customer_create_input , db: Session = Depends(get_db)):
#     return customer_service.create_customer(db,customer)

# @app.get("/customers", response_model=list[Customer_schema])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = customer_service.get_customers(db, skip=skip, limit=limit)
#     return users

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
