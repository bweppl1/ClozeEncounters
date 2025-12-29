from sqlalchemy import func
import re
import unicodedata
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Query,
)  # HTTPEx. for error responses
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from typing import Annotated, Optional
import app.models as models, app.schemas as schemas
from fastapi.middleware.cors import CORSMiddleware
import random
# Adds for auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Indentify the JWT in code
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Where CORS will allow access from 
origins = [
        "http://localhost:5173",
        "http://productionserver.com" # For use when I deploy
        ]
# CORS - allowing communication with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow HTTP methods
    allow_headers=["*"],  # Allow headers
)


def get_db():
    db = SessionLocal()  # Create db session
    try:
        yield db  # provide to request
    finally:
        db.close()  # close

#PWD Context
pwd_context = CryptContext(schema=["bcrypt"], deprecated="auto")

#JWD Secret and Algo
SECRET_KEY = "my_secret" #Automate randomness in the future?
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# API CRUD Ops
# GET, PUT, POST, DELETE

# db dependency variable
db_dependency = Annotated[Session, Depends(get_db)]

######################
# AUTH API/FUNCTIONS #
######################

def get_user_by_email(email: str, db: db_dependency):
    return db.query(User).filter(User.email == email).firt()

def create_new_user(user: schemas.UserCreate, db: db_dependency):
    hashed_password = pwd.context.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return "User added to DB."

# User Register API Endpoint
@app.post("/auth/register")
def register_user(user: schemas.UserCreate, db: db_dependency):
    db_user = get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return create_new_user(user, db)

# Authenticate User
def authenticate_user(email: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not pwd_context.very(password, user.hashed_password):
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
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: db_dependency):
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user: raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="Incorrect auth contents",
            headers={"WWW-Authenticate": "Bearer"},
            )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

def verify_token(token: str= Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        return payload
    except:
        raise HTTPException(status_code=403, detail="Token is invalid")

# Token verification endpoint
@app.get("verify-token/{token}")
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message": "Token is valid!!!"}

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


# Clean accents
def normalize_string(answer):
    no_accents = "".join(
        c
        for c in unicodedata.normalize("NFD", answer)
        if unicodedata.category(c) != "Mn"
    )
    return no_accents.lower().strip()


# reg ex to hide word in the cloze
def hide_word(cloze, word):
    pattern = rf"\b{re.escape(word)}\b"
    return re.sub(pattern, "____", cloze, flags=re.IGNORECASE)


@app.get("/random_cloze", response_model=schemas.ClozeResponse)
def get_random_cloze_endpoint(
    max_id: Optional[int] = Query(
        None, description="Max word id to use, for titrating exposed vocabulary"
    ),
    db: Session = Depends(get_db),
):

    # Get random word
    query = db.query(models.Word)

    if max_id is not None:
        query = query.filter(models.Word.id <= max_id)

    if not query:
        raise HTTPException(status_code=404, detail="No words with sentences found")

    word = query.order_by(func.random()).first()

    # Pick a random sentence from this word
    sentence = random.choice(word.sentences)

    # Create cloze
    hidden_cloze = hide_word(sentence.spanish, word.word)
    if hidden_cloze and hidden_cloze[0] != "_":
        hidden_cloze = hidden_cloze[0].upper() + hidden_cloze[1:]

    answer = normalize_string(word.word)

    return {
        "word_id": word.id,
        "word": word.word,
        "answer": answer,
        "cloze": hidden_cloze,
        "spanish": sentence.spanish,
        "english": sentence.english,
    }
