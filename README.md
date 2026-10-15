# Wordwise — Spaced Repetition Vocabulary Trainer

A full-stack vocabulary learning application that helps users remember
words through spaced repetition. Built as part of the Aumne AI coding
challenge.

The application allows users to manage vocabulary, review words based
on scheduled dates, track learning progress, and inspect review history.

## Features

- **Vocabulary Management:** Add and delete words with their definitions
  and languages.
- **Spaced Repetition:** Schedule reviews based on recall scores from 0
  to 5.
- **Review Scheduling:** Apply challenge-specific scheduling rules for
  successful and unsuccessful reviews.
- **Learning History:** Track review attempts, scores, and scheduling
  information.
- **Progress Tracking:** View vocabulary counts, review statistics,
  recall accuracy, learning streaks, and difficult words.
- **Upcoming Reviews:** Inspect scheduled vocabulary reviews.
- **REST API:** Access application functionality through FastAPI endpoints.
- **Interactive API Documentation:** Explore endpoints through Swagger UI.
- **Python SDK:** Generate a Python client from the OpenAPI specification
  using OpenAPI Generator.
- **Database Migrations:** Manage schema changes with Alembic.
- **Automated Tests:** Run backend and SDK test suites.

## Technology Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pydantic

### Frontend
- React
- Vite
- JavaScript
- Axios

### SDK and Testing
- OpenAPI
- OpenAPI Generator
- Python SDK
- Pytest

## Application Architecture

The application follows a client-server architecture.

1. The React frontend provides the user interface.
2. Axios sends HTTP requests to the FastAPI backend.
3. FastAPI validates requests and executes application logic.
4. SQLAlchemy manages database operations.
5. SQLite stores vocabulary and review information.
6. The backend returns responses to the frontend.

The frontend communicates with the backend through API requests rather
than accessing the database directly.

## Requirements

- Python 3.10 or newer
- Node.js and npm
- Java runtime compatible with OpenAPI Generator, if regenerating the SDK

Docker is not required.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/samruddi-sk/wordwise-vocabulary-trainer.git
cd wordwise-vocabulary-trainer