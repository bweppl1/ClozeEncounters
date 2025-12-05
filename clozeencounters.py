# main game
import re
import unicodedata
import random
from app.cloze_generation import get_random_cloze_data
from app.user import get_user
from app.database import engine
from sqlalchemy.orm import Session

# console styling
from rich.console import Console
from rich.panel import Panel

# from rich.text import Text
from rich.prompt import Prompt

console = Console()


def normalize_string(answer):
    # Normalize unicode → removes accents (á → a, ñ → n, etc.)
    no_accents = "".join(
        c
        for c in unicodedata.normalize("NFD", answer)
        if unicodedata.category(c) != "Mn"
    )
    return no_accents.lower().strip()


def print_message(text: str, style: str = "white"):
    console.print(text, style=style)


def print_panel(text: str, title: str = "TITLE MISSING", style: str = "blue"):
    console.print(Panel(text, title=title, style=style))


# reg ex to hide word in the cloze
def hide_word(cloze, word):
    pattern = rf"\b{re.escape(word)}\b"
    return re.sub(pattern, "____", normalize_string(cloze), flags=re.IGNORECASE)


def generate_quiz_data(game_round, total_rounds):
    random_cloze_data = get_random_cloze_data(Session(engine))
    # print(f"test: {random_cloze_data}") - TEST PRINT
    random_word = random_cloze_data["word"]
    random_cloze = random_cloze_data["spanish"]
    english_translation = random_cloze_data["english"]
    # hide word
    hidden_cloze = hide_word(random_cloze, random_word)
    if hidden_cloze[0] != "_":
        hidden_cloze = hidden_cloze[0].upper() + hidden_cloze[1:]
    # UI Cloze display
    print_panel(
        f"\nSpanish: {hidden_cloze}\n\n" f"English: {english_translation}\n",
        f"Question {game_round}/{total_rounds}",
        style="yellow",
    )

    # User answer
    user_answer = Prompt.ask("\nTu respuesta / Your answer")
    print(f"TESTING word id: {random_cloze_data['id']}")

    # Submit answer
    is_correct = check_answer(random_word, user_answer, random_cloze)
    return [is_correct, random_cloze_data["id"]]


def check_answer(answer, guess, cloze):
    if normalize_string(guess) == normalize_string(answer):
        print_panel(
            f"{cloze}",
            random.choice(["You're a genius!", "Yes! You're amazing!"]),
            style="chartreuse1",
        )
        return True
    else:
        print_panel(f"{cloze}", random.choice(["Wrong", "Haha.. no"]), style="red")
        return False


# Updating user word score
# Need to implement some kind of interval value
def update_word_score(user, word, word_score):
    pass


# Main game loop
def start_game():
    # starting stats - eventually built into user table in PostgreSQL
    player_points = 0
    game_round = 1
    game_round_limit = 5
    print_panel(
        "\nBienvenido a Cloze Encounters!\n\n"
        "Complete the Spanish sentence by filling in the blank!\n",
        "Cloze Encounters",
        "purple",
    )
    player_name = Prompt.ask("Cual es tu nombre? / What is your name?")
    # find or create user
    user_data = get_user(player_name)
    # contains:
    # user_data.id
    # user_data.name
    gaming = True
    while gaming:
        # If correct, increment points
        is_correct, word_id = generate_quiz_data(game_round, game_round_limit)
        # update_word_score(word, user_data.id, word_score)
        # Correct answer tasks
        if is_correct:
            player_points += 1
            update_word_score(user_data.id, word_id, is_correct)
        # Incorrect answer tasks
        else:
            pass
        # Increment game round, will be used in 10 round game modes
        game_round += 1
        if game_round > game_round_limit:
            gaming = False
            # Good bye panel
            accuracy = (
                player_points / game_round_limit
            ) * 100  # This logic will need to adjust if player exits early
            # Calculating dynamic end game message based on performance, can remove later
            if accuracy > 79 and accuracy < 100:
                parting_words = f"Impressive performance {player_name}.. for a muggle."
            elif accuracy > 50 and accuracy < 80:
                parting_words = f"Well {player_name}, you're not a complete idiot."
            elif accuracy > 0 and accuracy <= 50:
                parting_words = f"{player_name}, the list of correct answers.. is about as long as your school bas was."
            elif accuracy == 0:
                parting_words = f"{player_name}, we calculate your score by dividing your points by your IQ... but that seems to have caused an error."
            else:
                parting_words = f"Esa fue una actuacion increible, {player_name}!"

            print_panel(
                f"\nFinal score: {player_points}\n"
                f"Accuracy: %{accuracy:.2f}\n\n"
                f"{parting_words}\n",
                "Good Bye!",
                style="purple",
            )


start_game()
