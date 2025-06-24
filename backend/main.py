from fastapi import FastAPI, Depends, HTTPException, Query, Form
from sqlalchemy import and_
from sqlalchemy.orm import Session 
from pydantic import BaseModel
from typing import Optional
from auth import hash_password, verify_password, create_access_token, decode_access_token, get_current_user
from models import User, UserCreate, UserResponse, Item, ItemCreate, ItemResponse, ItemPatch, Base
from database import engine, get_db
app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/signup/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
   exsisting_user = db.query(User).filter(User.username == user.username).first()
   if exsisting_user:
      raise HTTPException(status_code=400, detail="Username already taken")
   
   hashed_password = hash_password(user.password)
   new_user = User(username = user.username, hashed_password = hashed_password)

   db.add(new_user)
   db.commit()
   db.refresh(new_user)

   return new_user

@app.post("/login/")
async def login_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
   db_user = db.query(User).filter(User.username == username).first()
   if not db_user or not verify_password(password, db_user.hashed_password):
      raise HTTPException(status_code=400, detail="Invalid credentials")
   
   access_token = create_access_token(data={"sub": db_user.username})

   return {"access_token": access_token, "token_type": "bearer", "user": db_user}

@app.post("/logout/")
def logout_user(user: User = Depends(get_current_user)):
   return {"message": "Logged out successfully — please delete token on client side."}


@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_item = Item(**item.model_dump(), owner_id = user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_item = db.query(Item).filter(
       and_(
            Item.id == item_id,
            user.id == Item.owner_id)).first()
    if db_item is None:
      raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=list[ItemResponse])
async def read_all_items(complete: Optional[bool] = Query(None), name: Optional[str] = Query(None), db: Session = Depends(get_db), 
                         user: User = Depends(get_current_user)):
   query = db.query(Item).filter(Item.owner_id == user.id)
   if complete is not None:
      query = query.filter(Item.complete == complete)
   if name is not None:
      query = query.filter(Item.name == name)
   return query.all()

@app.delete("/items/{item_id}", response_model=ItemResponse)
async def delete_item(item_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
   db_item = db.query(Item).filter(
        and_(
            Item.id == item_id,
            Item.owner_id == user.id
        )
    ).first()
   if db_item is None:
      raise HTTPException(status_code=404, detail="Item not found")
   db.delete(db_item)
   db.commit()
   return db_item

@app.patch("/items/{item_id}", response_model=ItemResponse)
async def patch_item(item: ItemPatch, item_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
   db_item = db.query(Item).filter(and_(Item.id == item_id, Item.owner_id == user.id)).first()
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
async def reverse_status(item_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
   db_item = db.query(Item).filter(and_(Item.id == item_id, Item.owner_id == user.id)).first()
   if db_item is None:
    raise HTTPException(status_code=404, detail="Item not found")
   db_item.complete = not db_item.complete

   db.commit()
   db.refresh(db_item)

   return db_item
