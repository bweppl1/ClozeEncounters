# ClozeEncounters

## Summary

CLI Cloze style quizes to help improve vocabulary in early language learning.
![Picture of the CLI](https://github.com/bweppl1/ClozeEncounters/blob/main/assets/cli.png)

## Problem

Effective language learning happens through immersion in target language content. Early learning requires simple content. Often, this low levelcontent is only available in mediums which aren't interesting to adult learners (children's books & shows). When an early learner starts to lose motivation, and the tools they are using aren't interseting for them, they give up. Many early language learners quit after \_\_\_.

## Solution

The top 500 words account for ~80% of spanish conversation. Attaining this milestone allows learners to immerse in diverse content that interests them, increasing goal adherence and improving the likelihood that a learner will successfully acquire their target language.

ClozeEncounters combines **_Gamification_** and **_Spaced Repetition_** principles to help early language learners quickly and efficiently acquire the most common vocabulary.

#### Gamification

- Users are more likely to study if the tool feels like a game
- Learning sessions are longer with gamification<sup>1</sup>
- Faster short term acquisition with streaks and xp bars<sup>2</sup>

<sup>1</sup> (Nicholson 2015, Dichev 2020)
<sup>2</sup> (Lamb 2019, Dichev 2020)

#### Spaced Repetition

Spaced repetition is the use of repeat exposure to items, with intervals set just before the item leaves a learner's short term memory.

ClozeEncounters uses **_FSRS_** (Free Spaced Repetition Scheudler). At a high level this algorithm uses 3 variables to determine repetition intervals:

1. Difficulty - How inherently difficult an item is to understand (Simple vocabulary vs. vs complex tense \_\_\_\_)
2. Stability - How long an item stays in memory before significant decay (Measured in days)
3. Retrievability - The probability that an item can be recalled at any given time (Measured in percent)

With **_FSRS_** a user can set their **_Retrievability_**, esentially trading memory(+/-) for repetitions(+/-). The algorithm is "free" because it allows flexibility in learning habits. Older spaced repetition models were optimized for daily, single sessions. **_FSRS_** allows users to review more or less frequently and adapts as they do.

To read more about FSRS visit:

- <https://github.com/open-spaced-repetition/srs-benchmark?tab=readme-ov-file>
- <https://github.com/open-spaced-repetition/fsrs-vs-sm17>

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

- [x] Normalizing entire display sentence to account for accents
- [x] Some words aren't being hidden -> [tambien, como, aqui(88), estas(75), esta(82) que(51)] -> Testing fix

### Features

- [x] Quiz groups (Top 10, 50, 100 most common words)
- [x] Quiz rounds (e.g. 10 questions, or timed)
- [x] Rich Terminal Styling
- [x] PostgreSQL and FastAPI integration
- [x] System to eliminate duplication

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
|- seed_db.py                   # Creating DB
|- seed_data.py                 # Seeding data
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
