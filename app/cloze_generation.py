import random
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Word


def get_random_cloze_data(db: Session) -> dict:
    word = db.query(Word).order_by(func.random()).first()
    if not word or not word.sentences:
        raise ValueError("Error pulling data from database.")

    sentence = random.choice(word.sentences)

    return {
        "id": word.id,
        "word": word.word,
        "english": sentence.english,
        "spanish": sentence.spanish,
    }
