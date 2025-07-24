"""
PostgreSQL task repository.
"""

import psycopg2
import psycopg2.extras
from app.entities.task import ReviewTask, TaskStatus
from app.entities.review_result import ReviewResult, FileReview, Issue, ReviewSummary
from app.interfaces.task_repo import ITaskRepo

class PostgresTaskRepo(ITaskRepo):
    def __init__(self, dsn: str):
        self.dsn = dsn

    def add(self, repo_url: str, pr_number: int, auth_token: str = None) -> int:
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO review_tasks (repo_url, pr_number, auth_token, status) VALUES (%s, %s, %s, %s) RETURNING id",
                    (repo_url, pr_number, auth_token, TaskStatus.PENDING.value)
                )
                task_id = cur.fetchone()[0]
                conn.commit()
                return task_id

    def get(self, task_id: int) -> ReviewTask:
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("SELECT * FROM review_tasks WHERE id = %s", (task_id,))
                row = cur.fetchone()
                if not row:
                    raise Exception("Task not found")
                results = None
                if row["results"]:
                    import json
                    r = json.loads(row["results"])
                    files = [FileReview(f["file_name"], [Issue(**i) for i in f["issues"]]) for f in r["files"]]
                    summary = ReviewSummary(**r["summary"])
                    results = ReviewResult(files, summary)
                return ReviewTask(
                    id=row["id"],
                    repo_url=row["repo_url"],
                    pr_number=row["pr_number"],
                    auth_token=row["auth_token"],
                    status=TaskStatus(row["status"]),
                    results=results
                )

    def update(self, task_id: int, status: str, results: object = None):
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                if results:
                    import json
                    results_json = json.dumps({
                        "files": [
                            {
                                "file_name": f.file_name,
                                "issues": [vars(i) for i in f.issues]
                            } for f in results.files
                        ],
                        "summary": vars(results.summary)
                    })
                    cur.execute(
                        "UPDATE review_tasks SET status = %s, results = %s WHERE id = %s",
                        (status, results_json, task_id)
                    )
                else:
                    cur.execute(
                        "UPDATE review_tasks SET status = %s WHERE id = %s",
                        (status, task_id)
                    )
                conn.commit()