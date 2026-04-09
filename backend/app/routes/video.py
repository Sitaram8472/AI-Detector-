import os
from fastapi import APIRouter, File, UploadFile
from app.services.video_services import process_video, get_video_result

router = APIRouter()

@router.post("/video")
async def upload_video(file: UploadFile = File(...)):

    os.makedirs("data", exist_ok=True)

    path = f"data/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    return process_video(path)


@router.get("/video-result/{task_id}")
async def video_result(task_id: str):
    return get_video_result(task_id)