# SentinelMod

Skeleton implementation for a Telegram moderation bot built with [Aiogram 3](https://github.com/aiogram/aiogram) and
asynchronous SQLAlchemy. The project provides database models, handler structure and basic services to build upon.

## Setup

Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file with your bot token and PostgreSQL DSN:

```
BOT_TOKEN=123456:ABCDEF
POSTGRES_DSN=postgresql+asyncpg://user:pass@localhost:5432/sentinel
```

Run database migrations (not included) and start the bot:

```bash
python main.py
```

## Tests

Run a small test suite with:

```bash
pytest
```
