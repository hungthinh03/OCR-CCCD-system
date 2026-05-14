import cv2
from ultralytics import YOLO

# Load model
model = YOLO("models/field/text_detect.pt")

# Predict
results = model("models/field/test/test.jpg")

# Read image
img = cv2.imread("models/field/test/test.jpg")

# Get boxes + classes
boxes = results[0].boxes.xyxy.cpu().numpy()
classes = results[0].boxes.cls.cpu().numpy()

# Draw predictions
for box, cls_id in zip(boxes, classes):
    x1, y1, x2, y2 = map(int, box)

    field_name = model.names[int(cls_id)]

    # Draw rectangle
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

    # Draw label
    cv2.putText(
        img,
        field_name,
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

# Save output
cv2.imwrite("models/field/test/output.jpg", img)