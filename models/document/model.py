import cv2
import numpy as np
from ultralytics import YOLO

# Load model once
model = YOLO("models/document/best.pt")


def rotate_image(image, angle):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)

    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    rotated = cv2.warpAffine(
        image,
        matrix,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]

    lines = cv2.HoughLinesP(
        thresh,
        1,
        np.pi / 180,
        threshold=100,
        minLineLength=100,
        maxLineGap=10
    )

    if lines is None: 
        return image

    angles = []

    for line in lines:
        x1, y1, x2, y2 = line[0]

        angle = np.degrees(
            np.arctan2(y2 - y1, x2 - x1)
        )

        # Ignore near-vertical lines
        if -45 < angle < 45:
            angles.append(angle)

    if len(angles) == 0: # No usable angles found
        return image

    median_angle = np.median(angles)

    rotated = rotate_image(image, median_angle)
    return rotated


def detect_document(image):
    results = model(image)

    boxes = results[0].boxes

    if len(boxes) == 0:
        return image

    # Get highest confidence box
    confs = boxes.conf.cpu().numpy()
    best_idx = np.argmax(confs)

    x1, y1, x2, y2 = map(
        int,
        boxes.xyxy.cpu().numpy()[best_idx]
    )

    h, w = image.shape[:2]

    # Add padding
    pad = 0
    x1 = max(0, x1 - pad)
    y1 = max(0, y1 - pad)
    x2 = min(w, x2 + pad)
    y2 = min(h, y2 + pad)

    # Crop document
    cropped = image[y1:y2, x1:x2]

    # Deskew
    cropped = deskew(cropped)

    return cropped