# seeding database with some test data
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models import Word, Sentence, Base, UserWords, User
from app.database import engine
from fastapi import Depends
from app.main import get_db

# test data
test_clozes = {
    "el": [
        ["El sol sale por la mañana.", "The sun rises in the morning."],
        ["Mi hermano lleva el sombrero nuevo.", "My brother is wearing the new hat."],
    ],
    "la": [
        [
            "La casa de mis abuelos es muy grande.",
            "My grandparents' house is very big.",
        ],
        ["Ella perdió la llave otra vez.", "She lost the key again."],
    ],
    "de": [
        ["Este libro es de María.", "This book belongs to María."],
        ["El coche de mi padre es rojo.", "My father's car is red."],
    ],
    "que": [
        ["No sé qué hora es.", "I don't know what time it is."],
        ["Dice que vendrá mañana.", "He/she says that he/she will come tomorrow."],
    ],
    "y": [
        ["Me gustan el café y el té.", "I like coffee and tea."],
        ["Juan y María son primos.", "Juan and María are cousins."],
    ],
    "a": [
        [
            "Vamos a la playa este fin de semana.",
            "We're going to the beach this weekend.",
        ],
        ["Le di el regalo a mi madre.", "I gave the gift to my mother."],
    ],
    "en": [
        [
            "Vivo en Madrid desde hace cinco años.",
            "I’ve been living in Madrid for five years.",
        ],
        ["Los niños juegan en el parque.", "The children are playing in the park."],
    ],
    "un": [
        ["Compré un regalo para ti.", "I bought a gift for you."],
        ["Hay un gato en el tejado.", "There’s a cat on the roof."],
    ],
    "ser": [
        ["Mañana va a ser un día largo.", "Tomorrow is going to be a long day."],
        [
            "Ellos quieren ser médicos cuando crezcan.",
            "They want to be doctors when they grow up.",
        ],
    ],
    "no": [
        ["No quiero café, gracias.", "I don’t want coffee, thank you."],
        ["No tengo tiempo hoy.", "I don’t have time today."],
    ],
}


def reset_db(db=Depends(get_db)):
    db.execute(
        text(
            """
                TRUNCATE TABLE
                    users,
                    words,
                    sentences,
                    user_words
                RESTART IDENTITY CASCADE
                                   """
        )
    )
    db.commit()


with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS user_words CASCADE;"))

Base.metadata.create_all(bind=engine)
print("user_words table recreated with correct boolean[] column")


def seed():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:

        # clear existing data
        reset_db(db)

        # db.query(Sentence).delete()
        # db.query(Word).delete()
        # db.query(UserWords).delete()
        # db.query(User).delete()
        # db.commit()

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
