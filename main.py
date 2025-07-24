"""
Entrypoint for the PR Reviewer backend.
Sets up FastAPI, Celery, and dependency injection.
"""

import os
import platform
from dotenv import load_dotenv
from fastapi import FastAPI
from celery import Celery
from app.utils.logger import get_logger
from app.utils.celery_utils import create_task
from app.gateways.github_pr import GithubPRGateway
from app.gateways.task_repo_pg import PostgresTaskRepo
from app.gateways.openrouter import OpenRouterLanguageModel
from app.gateways.llm_openai import OpenAILanguageModel
from app.gateways.llm_llama import LlamaLanguageModel
from app.gateways.llm_grok import GrokLanguageModel
from app.gateways.task_publisher import CeleryTaskPublisher
from app.core.reviewer_agent import ReviewerAgent
from app.core.task_manager import TaskManager
from app.core.crud_service import CrudService
from app.entrypoints.api_v1 import get_router

def create_app():
    load_dotenv()
    logger = get_logger()

    github_token = os.getenv("GITHUB_ACCESS_TOKEN", "")
    pr_repo = GithubPRGateway(github_token, logger)

    postgres_conn_string = os.getenv("POSTGRES_CONN_STRING", "postgresql://postgres:password@localhost:5432/pr_reviewer")
    task_repo = PostgresTaskRepo(postgres_conn_string)

    # Choose LLM provider (example: OpenRouter)
    openrouter_api_key = os.getenv("OPEN_ROUTER_API_KEY", "")
    llm = OpenRouterLanguageModel(logger, openrouter_api_key, "gpt-4o-mini")
    # To use OpenAI, Llama, or Grok, instantiate the appropriate class

    reviewer = ReviewerAgent(llm)
    task_manager = TaskManager(logger, pr_repo, task_repo, reviewer)

    redis_conn_string = os.getenv("REDIS_CONN_STRING", "redis://localhost:6379")
    celery_app = Celery(
        "tasks", broker=redis_conn_string + "/0", backend=redis_conn_string + "/1"
    )
    run_task = create_task(celery_app, task_manager)
    celery_app.register_task(run_task)

    celery_args = ["worker", "-l", "info", "--max-memory-per-child", "100"]
    if platform.system() == "Windows":
        celery_args.append("--pool=solo")

    # Start Celery worker in a background thread (if running as a single process)
    import threading
    worker_thread = threading.Thread(
        target=celery_app.worker_main,
        args=(celery_args,),
    )
    worker_thread.daemon = True
    worker_thread.start()

    task_publisher = CeleryTaskPublisher(run_task)
    crud_service = CrudService(logger, task_repo, task_publisher)
    app = FastAPI()
    app.include_router(get_router(crud_service), prefix="/api/v1")
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("SERVER_HOST", "127.0.0.1")
    port = int(os.getenv("SERVER_PORT", "8080"))
    uvicorn.run("main:app", host=host, port=port, reload=True)