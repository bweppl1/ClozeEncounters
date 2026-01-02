from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
import random
from typing import Optional

from ..database import get_db
from ..auth.auth_handler import get_current_active_user
from .. import models, schemas
from ..cloze_generation import hide_word, normalize_string

router = APIRouter()


@router.get("/random_cloze", response_model=schemas.ClozeResponse)
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
