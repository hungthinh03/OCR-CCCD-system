from models.document.model import detect_document
from models.field.model import detect_fields
from models.ocr.engine import extract_text
from services.postprocess import postprocess_result
from services.preprocess import preprocess_image

def run_pipeline(contents):
    # Preprocess
    image = preprocess_image(contents)

    if image is None:
        return {"error": "Invalid image"}

    # Detect document
    document_image = detect_document(image)

    # Detect information fields
    field_bboxes = detect_fields(document_image)

    # OCR each field
    raw_result = {}

    for field_name, bbox in field_bboxes.items():
        x1, y1, x2, y2 = bbox

        # Crop field image
        crop = document_image[y1:y2, x1:x2]

        # OCR prediction
        text = extract_text(crop)

        raw_result[field_name] = text

    # Post-process result
    final_result = postprocess_result(raw_result)

    return final_result