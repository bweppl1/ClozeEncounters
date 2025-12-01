from sqlalchemy import func
from fastapi import FastAPI, Depends, HTTPException  # HTTPEx. for error responses
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()  # Create db session
    try:
        yield db  # provide to request
    finally:
        db.close()  # close


# API CRUD Ops
# GET, PUT, POST, DELETE


@app.post("/words/", response_model=schemas.WordResponse)
def create_word(word: schemas.WordCreate, db: Session = Depends(get_db)):
    db_word = models.Word(word=word.word)
    for s in word.sentences:
        db_word.sentences.append(models.Sentence(spanish=s.spanish, english=s.english))
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


# @app.get("/sentences/", response_model=schema.SentenceResponse)
# def get_sentence(sentence: schemas.SentenceCreate, db: Session = Depends(get_db)):
#     db_sentence =


@app.get("/random", response_model=schemas.WordResponse)
def get_random_cloze(db: Session = Depends(get_db)):
    # Get random word
    word = db.query(models.Word).order_by(func.random()).first()
    if not word or not word.sentences:
        raise HTTPException(404, "No words in database")

    # returning word.id, word.word, sentence.spanish, sentence.english
    return word
