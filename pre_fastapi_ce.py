# main game
import re
import unicodedata
import random
from app.cloze_generation import get_random_cloze_data

# console styling
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
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
    return re.sub(pattern, "____", cloze, flags=re.IGNORECASE)


def generate_random_cloze(game_round, total_rounds):
    random_word = random.choice(list(test_clozes))
    random_choice = random.randint(0, 1)
    random_cloze, english_translation = test_clozes[random_word][random_choice]
    # hide word
    hidden_cloze = hide_word(normalize_string(random_cloze), random_word)
    if hidden_cloze[0] != "_":
        hidden_cloze = hidden_cloze[0].upper() + hidden_cloze[1:]
    # UI Cloze display
    print_panel(
        f"Spanish: {hidden_cloze}\n\n" f"English: {english_translation}",
        f"Question {game_round}/{total_rounds}",
        style="yellow",
    )

    # User answer
    user_answer = Prompt.ask("\nYour answer")

    # Submit answer
    return check_answer(random_word, user_answer, random_cloze)


def check_answer(answer, guess, cloze):
    if normalize_string(guess) == normalize_string(answer):
        print_panel(f"{cloze}", "Correct!", style="green")
        return True
    else:
        print_panel(f"{cloze}", "Wrong, idiot.", style="red")
        return False


# Main game loop
def start_game():
    # starting stats - eventually built into user table in PostgreSQL
    player_points = 0
    game_round = 1
    game_round_limit = 5
    print_panel(
        "Bienvenido a Cloze Encounters!\n\n"
        "Complete the Spanish sentence by filling in the blank!",
        "Cloze Encounters",
        "red",
    )
    player_name = Prompt.ask("What is your name?")
    gaming = True
    while gaming:
        # If correct, increment points
        earn_points = generate_random_cloze(game_round, game_round_limit)
        if earn_points:
            player_points += 1
        # Increment game round, will be used in 10 round game modes
        game_round += 1
        if game_round > game_round_limit:
            gaming = False
            # Good bye panel
            accuracy = (
                player_points / game_round_limit
            ) * 100  # This logic will need to adjust if player exits early
            print_panel(
                f"\nFinal score: {player_points}\n"
                f"Accuracy: %{accuracy:.2f}\n\n"
                f"You suck {player_name}.\n",
                "Good Bye!",
                style="purple",
            )


start_game()
