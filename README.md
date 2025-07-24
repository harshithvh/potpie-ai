# PR Reviewer Agent

An autonomous code review agent system that uses AI to analyze GitHub pull requests, process them asynchronously, and provide structured feedback through an API.

## Setup

```bash
pip install -r requirements.txt
docker-compose up
alembic upgrade head
python main.py
```

- After launching, access the interactive API docs at `/docs` (e.g., http://127.0.0.1:8080/docs).

## Migrations

- Use Alembic for DB migrations (`alembic upgrade head`)

## System Structure

- `/entities`: Core business models (PR, review, task, exceptions)
- `/core`: Main business logic (reviewer agent, task manager, CRUD)
- `/interfaces`: Contracts for LLMs, PR repo, reviewer, task repo, task queue
- `/gateways`: Adapters for GitHub, LLMs (OpenAI, OpenRouter, Llama, Grok), Postgres, Celery
- `/entrypoints`: FastAPI endpoints and schemas
- `/utils`: Logger and Celery helpers

---

## TODO

- [ ] **Prompt engineering:** Refine and experiment with LLM prompts for more insightful, actionable reviews - batching and context windows.
- [ ] **Contextual RAG:** Integrate hierarchical retrieval-augmented generation for deeper codebase understanding.
- [ ] **Rate limiting:** Limit the number of review requests per user or repository, and add logging/cloudwatch to monitor and track rate limit events for auditing and debugging.

---

**For more details, see code comments and docstrings in each module.**