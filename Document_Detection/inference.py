import cv2
from ultralytics import YOLO

model = YOLO("best (1).pt")
results = model("test.jpg")

img = cv2.imread("/test.jpg")

for box in results[0].boxes.xyxy:
    x1, y1, x2, y2 = map(int, box)
    cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 10)

cv2.imwrite("output1.jpg", img)

