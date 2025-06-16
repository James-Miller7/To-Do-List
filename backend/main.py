from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel


app = FastAPI()

DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine) 
Base = declarative_base()

class Item(Base):
  __tablename__ = "items"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  description = Column(String)


class ItemCreate(BaseModel):
    name: str
    description: str

class ItemResponse(BaseModel):
   id: int
   name: str
   description: str  

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item