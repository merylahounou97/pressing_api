from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import Settings

settings = Settings()



SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}/{settings.database_name}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
