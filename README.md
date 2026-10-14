# Wordwise — Spaced Repetition Vocabulary Trainer

A full-stack vocabulary trainer built for the Outcom.ai coding challenge. It uses FastAPI, SQLite, SQLAlchemy/Alembic, React, Axios, and an OpenAPI-generated Python SDK.

## Features

- Add and delete vocabulary words (word, definition, language).
- Review due words with scores from 0 to 5.
- SM-2-inspired scheduling that follows the brief's explicit examples: score 5 on the first review schedules the next review in 5 days; scores 0–2 schedule it for tomorrow; score 3 modestly increases the interval.
- Track easiness factor, repetition count, interval, and next review date for every review.
- View due words, upcoming schedule, recent review history, recall accuracy, streak, and difficult words.
- OpenAPI docs at `/docs`, backend tests, database migrations, seed data, and Windows setup/run scripts.

## Requirements

- Python 3.10 or newer (Python 3.11 is a safe choice for broad package compatibility).
- Node.js 20 or newer and npm.
- Java runtime compatible with the installed OpenAPI Generator CLI if generating the SDK locally.
- Docker is not required or used.

## Setup

### Windows

1. Open a terminal in the project directory.
2. Run `setupdev.bat`.
3. Run `runapplication.bat`.
4. Open the frontend at `http://localhost:5173` and API docs at `http://127.0.0.1:8000/docs`.

### macOS / Linux

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
alembic upgrade head
cd frontend && npm install && cd ..
```

Start the backend in one terminal:

```bash
source .venv/bin/activate
python main.py
```

Start the frontend in a second terminal:

```bash
cd frontend
npm start
```

Open `http://127.0.0.1:5173`. The backend docs are at `http://127.0.0.1:8000/docs`.

## Database migrations and sample data

Migrations are managed with Alembic:

```bash
alembic upgrade head
```

To load sample words into the default database after migration, run the SQL statements in `seed_data.sql` using SQLite. For example, if the `sqlite3` CLI is installed:

```bash
sqlite3 vocabulary.db < seed_data.sql
```

The app is usable without seed data; add words from the UI.

## Generate the Python SDK (required by the challenge)

The SDK must be generated from the running API's OpenAPI document rather than handwritten. Start the backend, install Node/npm and a compatible Java runtime, then install OpenAPI Generator CLI:

```bash
npm install -g @openapitools/openapi-generator-cli
```

Generate the SDK from the project root:

```bash
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o srs_sdk --additional-properties=packageName=srs_sdk,projectName=srs-sdk
```

On Windows, run `generate_sdk.bat`; on macOS/Linux, run `bash generate_sdk.sh`.
The generator output is intentionally not checked into this source bundle: generate it against the final running API so the client matches the exact OpenAPI schema. The generated package structure can vary slightly by generator version; inspect its generated README and imports before using it.

## API quick reference

- `POST /words/` — create a word; JSON: `{"word":"bonjour","definition":"hello","language":"French"}`
- `GET /words/due/` — list words due today, including words never reviewed.
- `POST /words/{word_id}/review/` — submit JSON `{"score": 0}` through `{"score": 5}`.
- `GET /words/history/` — performance metrics, upcoming schedule, difficult words, and recent reviews.
- `DELETE /words/{word_id}` — delete a word and its review history.

Interactive docs: `http://127.0.0.1:8000/docs`.

## Tests

```bash
python -m pytest -q
```

Tests use an isolated in-memory SQLite database and do not modify your development database.

## Implementation note

The challenge's stated rules and examples take priority over a textbook SM-2 implementation. In particular, the first score of 5 uses a 5-day interval to match the supplied example, and a score from 0–2 resets the interval to one day. The easiness-factor update follows the common SM-2 formula with a minimum factor of 1.3.
