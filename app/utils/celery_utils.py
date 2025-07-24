"""
Celery task closure helper.
"""

def create_task(celery_app, task_manager):
    @celery_app.task(name="run_review_task")
    def run_review_task(task_id: int):
        task_manager.consume_task(task_id)
    return run_review_task