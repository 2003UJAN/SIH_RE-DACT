from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import os
from typing import Optional
from models.text_redactor import TextRedactor
from models.image_redactor import ImageRedactor
from models.video_redactor import VideoRedactor
from models.audio_redactor import AudioRedactor

app = FastAPI()

class RedactionDegree(BaseModel):
    degree: int

@app.post("/redact-text/")
async def redact_text(text: str = Form(...), degree: int = Form(...)):
    redactor = TextRedactor()
    entities = redactor.perform_ner(text)
    redacted_text = redactor.redact_text(text, entities, degree)
    return {"redacted_text": redacted_text}

@app.post("/upload-image/")
async def upload_image(degree: int = Form(...), file: UploadFile = File(...)):
    redactor = ImageRedactor()
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    redacted_image = redactor.redact_image(file_path, degree)
    os.remove(file_path)
    return {"message": "Image redacted successfully"}

@app.post("/upload-video/")
async def upload_video(degree: int = Form(...), file: UploadFile = File(...)):
    redactor = VideoRedactor()
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    redacted_video_path = redactor.redact_video(file_path, degree)
    os.remove(file_path)
    return {"message": "Video redacted successfully", "file_path": redacted_video_path}

@app.post("/upload-audio/")
async def upload_audio(degree: int = Form(...), file: UploadFile = File(...)):
    redactor = AudioRedactor()
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    redacted_audio_path = redactor.redact_audio(file_path, degree)
    os.remove(file_path)
    return {"message": "Audio redacted successfully", "file_path": redacted_audio_path}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Redaction Tool API. Use the endpoints to redact text, images, videos, and audio."}
