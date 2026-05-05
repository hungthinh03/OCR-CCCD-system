from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/")
async def ocr(file: UploadFile):
    image = await file.read()
    #result = pipeline.run_pipeline(image)
    #return result