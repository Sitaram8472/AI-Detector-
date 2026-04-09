import os

from fastapi import APIRouter, File, UploadFile
from app.services.image_services import analyze_image

router = APIRouter()

@router.post("/image")
async def image_detect(file: UploadFile = File(...)):
    os.makedirs("data", exist_ok=True)
    path = f"data/{file.filename}"

    # Save file
    with open(path, "wb") as f:
        f.write(await file.read())

    result = analyze_image(path)

    return result