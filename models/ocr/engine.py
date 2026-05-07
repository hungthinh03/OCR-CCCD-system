import numpy as np
import cv2
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import torch
from PIL import Image

# Load model (1 lần)
config = Cfg.load_config_from_name('vgg_transformer')
config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'

ocr_model = Predictor(config)


def extract_text(cropped_img):
    # OCR cho 1 vùng ảnh
    if cropped_img is None or cropped_img.size == 0:
        return ""

    # VietOCR cần PIL Image
    try:
        img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)

        pil_img = Image.fromarray(img_rgb)

        text = ocr_model.predict(pil_img)
    except:
        text = ""

    return text.strip()