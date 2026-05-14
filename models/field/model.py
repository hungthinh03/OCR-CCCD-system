from ultralytics import YOLO

model = YOLO('models/field/text_detect.pt')

def detect_fields(image):
    results = model(image)

    boxes = results[0].boxes.xyxy.cpu().numpy()
    classes = results[0].boxes.cls.cpu().numpy()

    model_classes = model.names

    field_bboxes = {}

    for box, cls_id in zip(boxes, classes):
        x1, y1, x2, y2 = map(int, box)

        field_name = model_classes[int(cls_id)]

        # Create list if field not exists
        if field_name not in field_bboxes:
            field_bboxes[field_name] = []

        field_bboxes[field_name].append(
            (x1, y1, x2, y2)
        )
    return field_bboxes
