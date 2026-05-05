import numpy as np
import cv2
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import torch

# Load model (1 lần)
config = Cfg.load_config_from_name('vgg_transformer')
config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'

ocr_model = Predictor(config)


def crop(image, bbox):
    # Crop image theo bounding box
    x1, y1, x2, y2 = bbox
    return image[y1:y2, x1:x2]


def ocr_single(cropped_img):
    # OCR cho 1 vùng ảnh
    if cropped_img is None or cropped_img.size == 0:
        return ""

    # VietOCR cần PIL Image
    img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)

    try:
        text = ocr_model.predict(img_rgb)
    except:
        text = ""

    return text.strip()


def run(image, bboxes):
    """
    OCR toàn bộ các field
    Args:
        image: numpy array (cv2 image)
        bboxes: dict {field_name: [x1,y1,x2,y2]}

    """
    results = {}

    for field, bbox in bboxes.items():
        cropped = crop(image, bbox)
        text = ocr_single(cropped)
        results[field] = text   # dict: text theo từng field

    return results