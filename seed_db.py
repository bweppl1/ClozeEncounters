# seeding database with some test data
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models import Word, Sentence, Base
from app.database import engine
from fastapi import Depends
from app.database import get_db
from seed_data import test_clozes


def reset_db(db=Depends(get_db)):
    db.execute(
        text(
            """
                TRUNCATE TABLE
                    words,
                    sentences,
                    users
                RESTART IDENTITY CASCADE
                                   """
        )
    )
    db.commit()


# !!CLEAR PostgreSQL table schema when redesigning with this:
# with engine.begin() as conn:
    # conn.execute(text("DROP TABLE IF EXISTS user_words CASCADE;"))
    # conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))

# Used after user_words originally created to contain an int .. may reuse
# Base.metadata.create_all(bind=engine)
# print("user_words table recreated with correct boolean[] column")


def seed():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:

        # clear existing data
        reset_db(db)

        total_sentences = 0

        for word_text, pairs in test_clozes.items():
            # Create the Word
            word = Word(word=word_text)
            db.add(word)
            db.flush()  # to generate ids; sends current data but doesn't commit

            # Create all sentences for this word
            for spanish, english in pairs:
                sentence = Sentence(
                    spanish=spanish,
                    english=english,
                    word_id=word.id,
                )
                db.add(sentence)
                total_sentences += 1

        db.commit()
        db.close()

        print(
            f"Successfully seeded {len(test_clozes)} words and {total_sentences} sentences!!!"
        )


if __name__ == "__main__":
    seed()
