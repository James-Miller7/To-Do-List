from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from models import User
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKENS_EXPIRE = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

def hash_password(password: str):
  return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
  return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKENS_EXPIRE))

  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def decode_access_token(token: str):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return payload
  except JWTError:
    return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  payload = decode_access_token(token)
  if not payload:
    raise HTTPException(status_code=401, detail="Invalid token")
  username = payload.get("sub")
  if username is None:
    raise HTTPException(status_code=401, detail="Invalid token")
  current_user = db.query(User).filter(User.username == username).first()
  if current_user is None:
    raise HTTPException(status_code=404, detail="User not found")
  return current_user


