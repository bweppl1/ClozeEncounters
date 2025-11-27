# main game
import re
import unicodedata
import random

# console styling
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

console = Console()

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


def generate_random_cloze(game_round):
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
        f"Question {game_round}",
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
    player_points = 0
    game_round = 1
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
        earn_points = generate_random_cloze(game_round)
        if earn_points:
            player_points += 1
        # Increment game round, will be used in 10 round game modes
        game_round += 1
        # Provides an exit point, may implement something different later
        continue_prompt = Prompt.ask("Continue? (y/n)")
        # End game sequence
        if continue_prompt != "y":
            gaming = False
            # Good bye panel
            print_panel(
                f"final score: {player_points}\n\n" f"You suck {player_name}.",
                "Good Bye!",
                style="purple",
            )


start_game()
