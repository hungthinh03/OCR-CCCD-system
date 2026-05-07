from ultralytics import YOLO

# Load model 1 lần
model = YOLO("models/document/best.pt")


def detect_document(image):
    results = model(image)

    # Lấy bbox đầu tiên
    boxes = results[0].boxes.xyxy.cpu().numpy()

    if len(boxes) == 0:
        return image

    x1, y1, x2, y2 = map(int, boxes[0])

    # Crop document
    cropped = image[y1:y2, x1:x2]

    return cropped