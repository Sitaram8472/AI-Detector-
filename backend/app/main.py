from fastapi import FastAPI
from app.routes import video, image, text, auth_routes, plagiarism

app = FastAPI()

app.include_router(video.router)
app.include_router(image.router)
app.include_router(text.router)
app.include_router(auth_routes.router)
app.include_router(plagiarism.router)

@app.get("/")
def home():
    return {"message": "DeepTrace API Running"}