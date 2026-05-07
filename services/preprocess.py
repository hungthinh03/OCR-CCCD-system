import cv2
import numpy as np

def decode_image(contents):
    np_arr = np.frombuffer(contents, np.uint8)

    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return image


def preprocess_image(contents):
    # Decode image
    image = decode_image(contents)

    if image is None:
        return None

    # Resize image
    h, w = image.shape[:2]
    max_size = 1280

    if w > max_size:
        scale = max_size / w

        new_w = int(w * scale)
        new_h = int(h * scale)

        image = cv2.resize(image, (new_w, new_h))
        
    return image