from sqlalchemy import func
from fastapi import FastAPI, Depends, HTTPException  # HTTPEx. for error responses
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from typing import Annotated
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


# Retrieving a random word
@app.get("/random_cloze", response_model=schemas.WordResponse)
def get_random_cloze(db: db_dependency):
    # Get random word
    word = db.query(models.Word).order_by(func.random()).first()
    if not word or not word.sentences:
        raise HTTPException(404, "No words in database")

    # returning word.id, word.word, sentence.spanish, sentence.english
    return word


# @app.get("/random_cloze", response_model=schemas.)
# def get_random_cloze_data(max, chosen_word_ids, db: Session) -> dict:
#     word = (
#         db.query(Word)
#         .filter(Word.id <= max)
#         .filter(Word.id.notin_(chosen_word_ids))
#         .order_by(func.random())
#         .first()
#     )
#     if not word or not word.sentences:
#         raise ValueError("Error pulling data from database.")
#
#     sentence = random.choice(word.sentences)
#
#     return {
#         "id": word.id,
#         "word": word.word,
#         "english": sentence.english,
#         "spanish": sentence.spanish,
#     }
# Create user
# @app.post("/user/", response_model=schemas.UserCreate)
# def create_user(user: schemas.UserCreate, db: db_dependency):
#     db_user = models.User(name=user.name)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# Create word score - unused...
# @app.post("/user_words/", response_model=schemas.UserWordCreate)
# def create_word_score(word_score: schemas.UserWordCreate, db: db_dependency):
#     db_word_score = models.UserWords(
#         word_score=word_score.word_score,
#         word_id=word_score.word_id,
#         user_id=word_score.user_id,
#     )
#     db.add(db_word_score)
#     db.commit()
#     db.refresh(db_word_score)
#     return db_word_score


# Retrieve word score
# @app.get("/user_words/", response_model=schemas.UserWordResponse)
# def get_word_score(word_score: schemas.UserWordsBase, word, user, db: db_dependency):
#     word_score_data = db.query(models.UserWords).(word=UserWords.word_id)
#     hit_interval = 0
#     if word_score[-1] == False:
#         hit_interval = 1
#     else:
#         attempts = len(word_score)
#         correct_attempts = 0
#         for attempt in word_score:
#             if attempt == True:
#                 correct_attempts += 1
#         retrievability = (correct_attempts / attempts) * 100
#         print(f"TESTING -> retrievability: {retrievability}")
#

# get user


# update wordscore
