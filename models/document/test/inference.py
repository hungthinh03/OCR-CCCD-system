import cv2
from ultralytics import YOLO

model = YOLO("models/document/best.pt")
results = model("models/document/test.jpg")

img = cv2.imread("models/document/test.jpg")

for box in results[0].boxes.xyxy:
    x1, y1, x2, y2 = map(int, box)
    cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 10)

cv2.imwrite("models/document/output.jpg", img)

