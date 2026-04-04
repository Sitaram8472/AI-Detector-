from celery import Celery

celery_app = Celery(
    "deeptrace",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.task_routes = {
    "app.workers.video_tasks.*": {"queue": "video_queue"}
}