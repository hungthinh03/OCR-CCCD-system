from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/")
async def ocr_cccd(file: UploadFile = File(...)):
    # 1. Read image
    image = await file.read()


    return True