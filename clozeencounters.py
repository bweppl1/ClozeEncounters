# main game
import re
import unicodedata
import random
from app.cloze_generation import get_random_cloze_data

# from app.user import get_user
from app.database import engine

# from app.word_score import get_word_score
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
    # return re.sub(pattern, "____", normalize_string(cloze), flags=re.IGNORECASE)
    return re.sub(pattern, "____", cloze, flags=re.IGNORECASE)


def generate_quiz_data(game_round, total_rounds, game_word_category, chosen_word_ids):
    random_cloze_data = get_random_cloze_data(
        game_word_category, chosen_word_ids, Session(engine)
    )

    # print(f"test: {random_cloze_data}") - TEST PRINT
    random_word_id = random_cloze_data["id"]
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
    return [
        is_correct,
        random_cloze_data["id"],
        random_word,
        random_cloze,
        hidden_cloze,
        english_translation,
    ]


def redo_question(word, spanish, hidden_cloze, english_translation):
    print_panel(
        f"\nSpanish: {hidden_cloze}\n\n" f"English: {english_translation}\n",
        f"Failed Word Redo",
        style="orange3",
    )
    # User answer
    user_answer = Prompt.ask("\nTu respuesta / Your answer")

    # Submit answer
    is_correct = check_answer(word, user_answer, spanish)
    return is_correct
    # May need to return word, word_id or more for point/word_score tracking


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


# Main game loop
def start_game():
    # starting stats - eventually built into user table in PostgreSQL
    player_points = 0
    game_round = 1
    redo_list = []  # will append quiz questions that the user fails
    chosen_word_ids = []
    print_panel(
        "\nBienvenido a Cloze Encounters!\n\n"
        "Complete the Spanish sentence by filling in the blank!\n",
        "Cloze Encounters",
        "purple",
    )
    player_name = Prompt.ask("Cual es tu nombre? / What is your name?")
    game_round_limit = int(Prompt.ask("How many rounds do you want to play?"))
    category_options = [10, 50, 100]
    game_word_category = 0  # default setting
    while game_word_category not in category_options:
        game_word_category = int(
            Prompt.ask(
                "Choose game mode: 10 Common(10), 50 Common(50), 100 Common(100)"
            )
        )
        if game_word_category not in category_options:
            print(f"Must choose a valid option: {category_options}")
    gaming = True
    while gaming:
        is_correct, word_id, word, random_cloze, hidden_cloze, english_translation = (
            generate_quiz_data(
                game_round, game_round_limit, game_word_category, chosen_word_ids
            )
        )
        # Add word.id to chosen list to avoid repeat appearances in the same round
        chosen_word_ids.append(word_id)

        # Correct answer tasks
        if is_correct:
            player_points += 1
        # Incorrect answer tasks
        else:
            # add question to repeat list
            redo_list.append([word, random_cloze, hidden_cloze, english_translation])
            # DEBUG print(f"Redo Added: {redo_list[-1]}")
        # Increment game round
        game_round += 1
        if game_round > game_round_limit:
            while len(redo_list) > 0:
                for question in redo_list:
                    # breakdown question components to pass to the redo list
                    word, random_cloze, hidden_cloze, english_translation = question
                    is_correct = redo_question(
                        word, random_cloze, hidden_cloze, english_translation
                    )
                    # if user is right, remove from redo list
                    if is_correct:
                        redo_list.remove(question)
            gaming = False  # end game
            game_end_screen(
                player_name, player_points, game_round_limit
            )  # display the end game screen


def game_end_screen(player, points, rounds):
    player_accuracy = int((points / rounds) * 100)
    print_panel(
        f"Points: {points} / {rounds}\n\nAccuracy: {player_accuracy}%\n\nWell done {player}!",
        f"Game Over",
        "purple",
    )


start_game()
