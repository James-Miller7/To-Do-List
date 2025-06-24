from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine) 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()