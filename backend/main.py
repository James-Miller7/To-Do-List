from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine) 
Base = declarative_base()

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True, nullable=False)
  hashed_password = Column(String, nullable=False)

class Item(Base):
  __tablename__ = "items"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  description = Column(String)
  complete = Column(Boolean, default=False, nullable=False)


class ItemCreate(BaseModel):
    name: str
    description: str

class ItemResponse(BaseModel):
   id: int
   name: str
   description: str  
   complete: bool

   model_config = {"from_attributes": True}

class ItemPatch(BaseModel):
   name: Optional[str] = None
   description: Optional[str] = None

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

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
      raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=list[ItemResponse])
async def read_all_items(complete: Optional[bool] = Query(None), name: Optional[str] = Query(None), db: Session = Depends(get_db)):
   query = db.query(Item)
   if complete is not None:
      query = query.filter(Item.complete == complete)
   if name is not None:
      query = query.filter(Item.name == name)
   return query

@app.delete("/items/{item_id}", response_model=ItemResponse)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
   db_item = db.query(Item).filter(Item.id == item_id).first()
   if db_item is None:
      raise HTTPException(status_code=404, detail="Item not found")
   db.delete(db_item)
   db.commit()
   return db_item

@app.patch("/items/{item_id}", response_model=ItemResponse)
async def patch_item(item: ItemPatch, item_id: int, db: Session = Depends(get_db)):
   db_item = db.query(Item).filter(Item.id == item_id).first()
   if db_item is None:
      raise HTTPException(status_code=404, detail="Item not found")
   if item.description:
    db_item.description = item.description
   if item.name:
    db_item.name = item.name

   db.commit()
   db.refresh(db_item)

   return db_item

@app.patch("/items/{item_id}/complete", response_model=ItemResponse)
async def reverse_status(item_id: int, db: Session = Depends(get_db)):
   db_item = db.query(Item).filter(Item.id == item_id).first()
   if db_item is None:
    raise HTTPException(status_code=404, detail="Item not found")
   db_item.complete = not db_item.complete

   db.commit()
   db.refresh(db_item)

   return db_item
