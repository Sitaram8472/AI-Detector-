from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import video, image, text, auth_routes, plagiarism

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video.router)
app.include_router(image.router)
app.include_router(text.router)
app.include_router(auth_routes.router)
app.include_router(plagiarism.router)

@app.get("/")
def home():
    return {"message": "DeepTrace API Running"}