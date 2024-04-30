from fastapi import  FastAPI, HTTPException


from .database import  engine, Base
from src.config import Settings
from .customer import  customer_router
from src.mail.send_mail import send_email
from .routers import login
from .routers import login


settings = Settings()

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(customer_router.router)
app.include_router(login.router)
app.include_router(login.router)


@app.get("/")
def main_page():
    return "Ceci est un pressing de wash man"

@app.get("/mail")
async def test_mail():
    return await send_email(settings.sender_email,"test","Un test de mail \U0001FAE1")

# @app.post("/customers", response_model=Customer_schema)
# def create_customers(customer: Customer_create_schema , db: Session = Depends(get_db)):
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
