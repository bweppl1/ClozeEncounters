from sqlalchemy import func
import re
import unicodedata
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from typing import Annotated, Optional
import app.models as models, app.schemas as schemas
from fastapi.middleware.cors import CORSMiddleware
import random

# Adds for auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError

# Indentify the JWT in code
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
# PWD Context
pwd_context = CryptContext(schema=["bcrypt"], deprecated="auto")

router = APIRouter()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Where CORS will allow access from
origins = [
    "http://localhost:5173",
    "http://productionserver.com",  # For use when I deploy
]
# CORS - allowing communication with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow HTTP methods
    allow_headers=["*"],  # Allow headers
)


# API CRUD Ops
# GET, PUT, POST, DELETE

# db dependency variable
db_dependency = Annotated[Session, Depends(get_db)]

######################
# AUTH API/FUNCTIONS #
######################

def get_user_by_email(email: str, db: db_dependency):
    return db.query(User).filter(User.email == email).first()


def create_new_user(user: schemas.UserCreate, db: db_dependency):
    hashed_password = pwd.context.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return "User added to DB."


# User Register API Endpoint
@app.post("/auth/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: db_dependency):
    db_user = get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    return create_new_user(user, db)


# User login API Endpoint
@app.post("/auth/login")
def login_user(user_data: schemas.UserLogin, db: db_dependency):
    # print(f"{user} backend")
    user = authenticate_user(user_data.email, user_data.password, db)

    if not user:
        print("failed to fetch user!")

    # create token
    access_token = create_access_token(data={"sub": user.email})


# Authenticate User
def authenticate_user(email: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    return user


# Create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# @app.post("/token")
# def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: db_dependency):
#     user = authenticate_user(form_data.email, form_data.password, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             details="Incorrect auth contents",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        return payload
    except:
        raise HTTPException(status_code=403, detail="Token is invalid")


# Token verification endpoint
# @app.get("verify-token/{token}")
# async def verify_user_token(token: str):
#     verify_token(token=token)
#     return {"message": "Token is valid!!!"}


########################
#  WORD API/FUNCTIONS  #
########################


# Creating a new word
@app.post("/words/", response_model=schemas.WordResponse)
def create_word(word: schemas.WordCreate, db: db_dependency):
    db_word = models.Word(word=word.word)
    for s in word.sentences:
        db_word.sentences.append(models.Sentence(spanish=s.spanish, english=s.english))
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


# Fetching all words
@app.get("/words/", response_model=schemas.WordResponse)
def get_all_words(db: db_dependency):
    word = db.query(models.Word)
    return {"word_id": word.id, "word": word.word}



