from app.workers.video_task import analyze_video_task

def process_video(path):
    task = analyze_video_task.delay(path)
    return {
        "message": "Processing started",
        "task_id": task.id
    }