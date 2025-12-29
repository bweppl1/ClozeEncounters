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


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS - allowing communication with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React port may use 3000
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


# API CRUD Ops
# GET, PUT, POST, DELETE

# db dependency variable
db_dependency = Annotated[Session, Depends(get_db)]


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


# Clean accts
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
