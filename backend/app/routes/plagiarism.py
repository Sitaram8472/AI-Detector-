import os

from fastapi import APIRouter, File, UploadFile
from app.services.plagiarism_services import analyze_file

router = APIRouter()

@router.post("/plagiarism")
async def check_plagiarism(file: UploadFile = File(...)):
    os.makedirs("data", exist_ok=True)
    path = f"data/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    return analyze_file(path)