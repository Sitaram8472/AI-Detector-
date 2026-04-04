import os
from fastapi import APIRouter, UploadFile
from app.services.video_services import process_video

router = APIRouter()

@router.post("/video")
async def upload_video(file: UploadFile):

    os.makedirs("data", exist_ok=True)

    path = f"data/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    return process_video(path)