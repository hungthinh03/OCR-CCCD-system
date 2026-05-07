from fastapi import APIRouter, UploadFile, File
from services import pipeline
import numpy as np
import cv2

router = APIRouter()

@router.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    contents = await file.read()

    np_arr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        return {"error": "Invalid image"}

    result = pipeline.run_pipeline(image)

    return result