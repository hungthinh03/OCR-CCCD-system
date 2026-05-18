import cv2

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.document.model import detect_document
from models.field.model import detect_fields
from models.ocr.engine import extract_text
from services.pipeline import run_pipeline
from services.preprocess import preprocess_image

# Read test image as bytes
with open("tests/test.jpg", "rb") as f:
    contents = f.read()

# PREPROCESS
image = preprocess_image(contents)

if image is None:
    print("Invalid image")
    exit()

# DOCUMENT DETECTION
document_image = detect_document(image)

cv2.imwrite("tests/output_document.jpg", document_image)

# FIELD DETECTION
field_bboxes = detect_fields(document_image)

debug_img = document_image.copy()


# OCR
raw_result = {}

for field_name, bboxes in field_bboxes.items():
    for bbox in bboxes:

        x1, y1, x2, y2 = bbox

        print(f"\n===== {field_name} =====")
        print(f"BBOX: {bbox}")

    # Draw bbox
        cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.putText(
        debug_img,
        field_name,
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # Crop field
        crop = document_image[y1:y2, x1:x2]

    # Save crop
        cv2.imwrite(f"tests/field_outputs/output_{field_name}.jpg", crop)

    # OCR
        text = extract_text(crop)
        print("OCR:", repr(text))

        raw_result[field_name] = text


# Save
cv2.imwrite("tests/output_fields.jpg", debug_img)

print("\n========== RAW RESULT ============")

for k, v in raw_result.items():
    print(f"{k}: {v}")


# FULL PIPELINE
print("\n========== FINAL RESULT ============")

final_result = run_pipeline(contents)
print(final_result)
