# ClozeEncounters

## Summary

CLI Cloze style quizes to help improve vocabulary in early language learning.
![Picture of the CLI(http://`https://github.com/bweppl1/ClozeEncounters/assets/cli.png)]

## Feature Focus

Going to work on getting a baseline top 100 words, then get game modes for Top 10, 25, 50, 100 words. After that I'll work on implementing the spaced repetition system.

### MVP [ Complete ]

1. Produce random cloze
2. Accept input
3. Provide result, and repeat

### Stack

#### Frontend

- Python CLI with Rich package

#### Backend

- FastAPI
- PostgreSQL
- SQLAlchemy & Pydantic

### Bugs

- [ ] Normalizing entire display sentence to account for accents

### Features

- [ ] Quiz groups (Top 10, 25, 50, 100 most common words)
- [ ] Point system
- [ ] Result tracking
- [x] Quiz rounds (e.g. 10 questions, or timed)
- [ ] Implementing learning theory spaced repitition systems
- [x] Rich Terminal Styling
- [ ] User progress
- [x] PostgreSQL and FastAPI integration

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
|- seed_db.py                   # Initial data
|- requiremets.txt              # Program requirements
|- README.md                    # You're lookin at it
```

## How To Use

```bash
# 1. Clone and enter
git clone https://github.com/bweppl1/ClozeEncounters.git
cd ClozeEncounters

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your database (PostgreSQL)
# Run these, make sure to replace clozeuser and password123 with whaever you want
sudo -u postgres psql -c "CREATE DATABASE clozeencounters;"
sudo -u postgres psql -c "CREATE USER clozeuser WITH ENCRYPTED PASSWORD 'password123';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE clozeencounters TO clozeuser;"

# 5. Set database URL in your .env
echo "DATABASE_URL=postgresql://clozeuser:password123@localhost:5432/clozeencounters" > .env

# 6. Seed the database
python seed_db.py

# 7. Play!
python clozeencounters.py

```
