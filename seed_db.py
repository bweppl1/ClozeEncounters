# seeding database with some test data
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models import Word, Sentence, Base, UserWords, User
from app.database import engine
from fastapi import Depends
from app.main import get_db
from seed_data import test_clozes

# test data
# test_clozes = {
#     "el": [
#         ["El sol sale por la mañana.", "The sun rises in the morning."],
#         ["Mi hermano lleva el sombrero nuevo.", "My brother is wearing the new hat."],
#     ],
#     "la": [
#         [
#             "La casa de mis abuelos es muy grande.",
#             "My grandparents' house is very big.",
#         ],
#         ["Ella perdió la llave otra vez.", "She lost the key again."],
#     ],
#     "de": [
#         ["Este libro es de María.", "This book belongs to María."],
#         ["El coche de mi padre es rojo.", "My father's car is red."],
#     ],
#     "que": [
#         ["No sé qué hora es.", "I don't know what time it is."],
#         ["Dice que vendrá mañana.", "He/she says that he/she will come tomorrow."],
#     ],
#     "y": [
#         ["Me gustan el café y el té.", "I like coffee and tea."],
#         ["Juan y María son primos.", "Juan and María are cousins."],
#     ],
#     "a": [
#         [
#             "Vamos a la playa este fin de semana.",
#             "We're going to the beach this weekend.",
#         ],
#         ["Le di el regalo a mi madre.", "I gave the gift to my mother."],
#     ],
#     "en": [
#         [
#             "Vivo en Madrid desde hace cinco años.",
#             "I’ve been living in Madrid for five years.",
#         ],
#         ["Los niños juegan en el parque.", "The children are playing in the park."],
#     ],
#     "un": [
#         ["Compré un regalo para ti.", "I bought a gift for you."],
#         ["Hay un gato en el tejado.", "There’s a cat on the roof."],
#     ],
#     "ser": [
#         ["Mañana va a ser un día largo.", "Tomorrow is going to be a long day."],
#         [
#             "Ellos quieren ser médicos cuando crezcan.",
#             "They want to be doctors when they grow up.",
#         ],
#     ],
#     "no": [
#         ["No quiero café, gracias.", "I don’t want coffee, thank you."],
#         ["No tengo tiempo hoy.", "I don’t have time today."],
#     ],
#     "es": [
#         ["Mi comida favorita es la pizza.", "My favorite food is pizza."],
#         ["Eso es exactamente lo que quería decir.", "That’s exactly what I meant."],
#     ],
#     "se": [
#         [
#             "Se lavó las manos antes de comer.",
#             "He/she washed their hands before eating.",
#         ],
#         [
#             "No se puede entrar sin invitación.",
#             "You can’t enter without an invitation.",
#         ],
#     ],
#     "con": [
#         ["Salgo con mis amigos los viernes.", "I go out with my friends on Fridays."],
#         ["Café con leche, por favor.", "Coffee with milk, please."],
#     ],
#     "por": [
#         ["Paseamos por el centro de la ciudad.", "We walked through the city center."],
#         ["Gracias por tu ayuda.", "Thank you for your help."],
#     ],
#     "para": [
#         ["Este regalo es para ti.", "This gift is for you."],
#         ["Necesito dinero para el autobús.", "I need money for the bus."],
#     ],
#     "su": [
#         ["Su perro es muy grande y amistoso.", "Their dog is very big and friendly."],
#         ["¿Dónde está su casa?", "Where is his/her/your (formal)/their house?"],
#     ],
#     "lo": [
#         ["Lo vi en la televisión ayer.", "I saw it/him on TV yesterday."],
#         ["No lo entiendo.", "I don’t know it/him."],
#     ],
#     "me": [
#         ["Me gusta bailar salsa.", "I like to dance salsa."],
#         ["¿Me puedes ayudar con esto?", "Can you help me with this?"],
#     ],
#     "una": [
#         ["Tengo una idea genial.", "I have a great idea."],
#         ["Compré una camiseta roja.", "I bought a red T-shirt."],
#     ],
#     "te": [
#         ["Te llamo más tarde.", "I’ll call you later."],
#         ["Te quiero mucho.", "I love you very much."],
#     ],
#     "los": [
#         ["Los niños juegan en el jardín.", "The kids are playing in the garden."],
#         ["Vi a los actores en la película.", "I saw the actors in the movie."],
#     ],
#     "pero": [
#         ["Quiero ir, pero estoy muy cansado.", "I want to go, but I’m very tired."],
#         ["Es caro, pero vale la pena.", "It’s expensive, but it’s worth it."],
#     ],
#     "las": [
#         ["Las flores son para mi madre.", "The flowers are for my mother."],
#         ["Limpio las ventanas los sábados.", "I clean the windows on Saturdays."],
#     ],
#     "si": [
#         ["Si llueve, nos quedamos en casa.", "If it rains, we stay home."],
#         ["No sé si podré venir mañana.", "I don’t know if I can come tomorrow."],
#     ],
#     "más": [
#         ["Quiero más helado, por favor.", "I want more ice cream, please."],
#         [
#             "Este libro es más interesante que el otro.",
#             "This book is more interesting than the other one.",
#         ],
#     ],
#     "mi": [
#         ["Mi hermano mayor vive en Barcelona.", "My older brother lives in Barcelona."],
#         ["Este es mi libro favorito.", "This is my favorite book."],
#     ],
#     "ya": [
#         ["Ya terminé mis deberes.", "I already finished my homework."],
#         ["¡Ya voy!", "I’m coming!"],
#     ],
#     "todo": [
#         ["Todo está listo para la fiesta.", "Everything is ready for the party."],
#         ["Come todo lo que quieras.", "Eat everything you want."],
#     ],
#     "esta": [
#         ["Esta película es increíble.", "This movie is amazing."],
#         ["¿Has visto esta serie?", "Have you seen this series?"],
#     ],
#     "como": [
#         ["Come como un campeón.", "He/she eats like a champion."],
#         ["No sé cómo hacerlo.", "I don’t know how to do it."],
#     ],
#     "le": [
#         ["Le di un abrazo a mi abuela.", "I gave my grandma a hug."],
#         ["Le gusta leer novelas.", "He/she likes to read novels."],
#     ],
#     "esto": [
#         ["¿Qué es esto?", "What is this?"],
#         ["Esto no funciona bien.", "This doesn’t work well."],
#     ],
#     "al": [
#         ["Voy al supermercado ahora.", "I’m going to the supermarket now."],
#         ["Llegamos al aeropuerto a las siete.", "We arrive at the airport at seven."],
#     ],
#     "del": [
#         ["Es el coche del vecino.", "It’s the neighbor’s car."],
#         ["Salimos del cine muy tarde.", "We left the cinema very late."],
#     ],
#     "muy": [
#         ["Estoy muy cansado después del trabajo.", "I’m very tired after work."],
#         ["¡Qué muy bonito!", "How very beautiful!"],
#     ],
#     "nos": [
#         ["Nos vemos mañana.", "See you tomorrow."],
#         ["Nos gusta viajar juntos.", "We like to travel together."],
#     ],
#     "tu": [
#         ["Tu casa es más grande que la mía.", "Your house is bigger than mine."],
#         ["¿Dónde está tu móvil?", "Where is your phone?"],
#     ],
#     "yo": [
#         ["Yo soy profesor de español.", "I am a Spanish teacher."],
#         ["Yo mismo lo haré.", "I’ll do it myself."],
#     ],
#     "él": [
#         ["Él llega mañana por la mañana.", "He arrives tomorrow morning."],
#         ["Él siempre paga la cuenta.", "He always pays the bill."],
#     ],
#     "son": [
#         ["Mis hijos son muy traviesos.", "My children are very naughty."],
#         ["¿A qué hora son las clases?", "What time are the classes?"],
#     ],
#     "tiene": [
#         ["Mi hermana tiene dos gatos.", "My sister has two cats."],
#         ["¿Cuántos años tienes?", "How old are you?"],
#     ],
#     "hay": [
#         ["Hay mucha gente en la playa.", "There are a lot of people on the beach."],
#         ["No hay problema.", "No problem."],
#     ],
#     "era": [
#         ["Era una noche oscura y tormentosa.", "It was a dark and stormy night."],
#         ["Cuando era niño, vivía en México.", "When I was a child, I lived in Mexico."],
#     ],
#     "o": [
#         ["¿Prefieres té o café?", "Do you prefer tea or coffee?"],
#         ["Puedes venir hoy o mañana.", "You can come today or tomorrow."],
#     ],
#     "fue": [
#         ["El concierto fue increíble.", "The concert was amazing."],
#         ["Ayer fue mi cumpleaños.", "Yesterday was my birthday."],
#     ],
#     "este": [
#         ["Este libro es muy interesante.", "This book is very interesting."],
#         ["Este año voy a aprender italiano.", "This year I’m going to learn Italian."],
#     ],
#     "también": [
#         ["Yo también quiero ir al cine.", "I want to go to the cinema too."],
#         [
#             "Ella habla español y también francés.",
#             "She speaks Spanish and also French.",
#         ],
#     ],
#     "ha": [
#         ["Ya ha terminado el examen.", "He/she has already finished the exam."],
#         ["Nunca ha estado en Asia.", "He/she has never been to Asia."],
#     ],
#     "otro": [
#         ["Necesito otro bolígrafo.", "I need another pen."],
#         ["Vamos a otro restaurante.", "Let’s go to another restaurant."],
#     ],
#     "estaba": [
#         ["Estaba lloviendo cuando salimos.", "It was raining when we left."],
#         ["Yo estaba en casa todo el día.", "I was at home all day."],
#     ],
# }


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

# Used after user_words originally created to contain an int .. may reuse
# Base.metadata.create_all(bind=engine)
# print("user_words table recreated with correct boolean[] column")


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
