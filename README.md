# ClozeEncounters

## Summary

CLI Cloze style quizes to help improve vocabulary in early language learning.

### MVP [ Complete ]

1. Produce random cloze
2. Accept input
3. Provide result, and repeat

### Structure

- CLI UI, using Rich
- FastAPI backend
- PostgreSQL

### Bugs

[ ] Normalizing entire display sentence to account for accents
[ ]
[ ]
[ ]

### Features

[ ] Quiz groups (Top 10, 25, 50, 100 most common words)
[ ] Point system
[ ] Result tracking
[X] Quiz rounds (e.g. 10 questions, or timed)
[ ] Implementing learning theory spaced repitition systems
[X] Rich Terminal Styling
[ ] User progress

### File Structure

```
ClozeEncounters/
|- app/
|   |--- __init__.py
|   |--- main.py                # FastAPI application
|   |--- database.py            # Database connection
|   |--- schemas.py             # Database schema - Pydantic
|   |--- models.py              # Structure format of data - SQLAlchemy
|   |--- cloze_generation.py    # Cloze generation logic
|- clozeencounters.py           # Launch game
|- seed_database.py             # Initial data
|- .env                         # Secure variables
|- README.md                    # You're lookin at it
```
