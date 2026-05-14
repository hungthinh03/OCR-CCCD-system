from fastapi import APIRouter, UploadFile, File
from services import pipeline

router = APIRouter()

@router.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    contents = await file.read()

    result = pipeline.run_pipeline(contents)

    return result