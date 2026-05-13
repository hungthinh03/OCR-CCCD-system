from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.ocr import router as ocr_router
import torch

app = FastAPI(title="OCR API")

app.include_router(ocr_router, tags=["OCR"])

app.mount("/", StaticFiles(directory="templates", html=True), name="templates")
