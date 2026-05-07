from ultralytics import YOLO

# Load model
model = YOLO("models/field/best.pt")

CLASSES = [
    "id",
    "name",
    "dob",
    "gender",
    "nationality",
    "hometown",
    "address",
    "expiry"
]

def detect_fields(image):
    results = model(image)

    boxes = results[0].boxes.xyxy.cpu().numpy()
    classes = results[0].boxes.cls.cpu().numpy()

    field_bboxes = {}

    for box, cls_id in zip(boxes, classes):
        x1, y1, x2, y2 = map(int, box)

        field_name = CLASSES[int(cls_id)]

        field_bboxes[field_name] = (x1, y1, x2, y2)

    return field_bboxes