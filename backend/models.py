from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional
from pydantic import BaseModel

Base = declarative_base()


class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True, nullable=False)
  hashed_password = Column(String, nullable=False)

  items = relationship("Item", back_populates="owner")


class Item(Base):
  __tablename__ = "items"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  description = Column(String)
  complete = Column(Boolean, default=False, nullable=False)

  owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  owner = relationship("User", back_populates="items")

class UserCreate(BaseModel):
   username: str
   password: str

class UserResponse(BaseModel):
   id: int
   username: str

   model_config = {"from_attributes": True}

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

