import cv2
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[3]))
from models.document.model import detect_document

# Read image
img = cv2.imread("models/document/test/test.jpg")

# Document detection
cropped = detect_document(img)

# Save result
cv2.imwrite("models/document/test/output.jpg", cropped)