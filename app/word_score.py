from app.database import SessionLocal
from app.models import UserWords

db = SessionLocal()


def get_word_score(user_id, word_id):
    user_word = (
        db.query(UserWords)
        .filter(UserWords.user_id == user_id, UserWords.word_id == word_id)
        .first()
    )

    # word hasnt been attempted so not entry exists
    if user_word is None:
        user_word = UserWords(user_id=user_id, word_id=word_id, word_score=[])
        db.add(user_word)
        db.commit()
        db.refresh(user_word)

    return user_word
