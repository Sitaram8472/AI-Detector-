from fastapi import APIRouter
from pydantic import BaseModel
from app.services.text_services import analyze_text

router = APIRouter()

class TextInput(BaseModel):
    text: str

@router.post("/text")
def detect_text(input: TextInput):
    return analyze_text(input.text)