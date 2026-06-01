# ocr_test.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pathlib import Path
from services import pipeline
import cv2
import numpy as np

# =========================
# CONFIG
# =========================
TEST_DIR = "test"
IMAGE_DIR = Path(TEST_DIR) / "images"
LABEL_DIR = Path(TEST_DIR) / "labels"

MAX_IMAGES = 200

VALID_EXTENSIONS = [".jpg", ".jpeg", ".png"]


# =========================
# CER / WER
# =========================
def levenshtein(a, b):
    m = len(a)
    n = len(b)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):

            cost = 0 if a[i - 1] == b[j - 1] else 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    return dp[m][n]


def cer(gt, pred):
    gt = gt.strip()
    pred = pred.strip()

    if len(gt) == 0:
        return 0

    distance = levenshtein(gt, pred)

    return distance / len(gt)


def wer(gt, pred):
    gt_words = gt.strip().split()
    pred_words = pred.strip().split()

    if len(gt_words) == 0:
        return 0

    distance = levenshtein(gt_words, pred_words)

    return distance / len(gt_words)


# =========================
# LOAD LABEL
# =========================
def load_label(label_path):
    """
    Label format:
    52201008654 NGUYỄN LÊ NGUYÊN
    """

    text = label_path.read_text(encoding="utf-8").strip()

    parts = text.split(maxsplit=1)

    if len(parts) < 2:
        return "", ""

    id_number = parts[0].strip()
    full_name = parts[1].strip()

    return id_number, full_name


# =========================
# MAIN TEST
# =========================
def main():

    image_files = []

    for ext in VALID_EXTENSIONS:
        image_files.extend(IMAGE_DIR.glob(f"*{ext}"))

    image_files = sorted(image_files)[:MAX_IMAGES]

    total_id_cer = 0
    total_id_wer = 0

    total_name_cer = 0
    total_name_wer = 0

    total_samples = 0

    for image_path in image_files:

        label_path = LABEL_DIR / f"{image_path.name}.txt"

        if not label_path.exists():
            print(f"Missing label: {label_path.name}")
            continue

        gt_id, gt_name = load_label(label_path)

        try:
            # Read image
            image = cv2.imread(str(image_path))

            # Convert to bytes
            _, buffer = cv2.imencode(".jpg", image)
            image_bytes = buffer.tobytes()

            # Run pipeline
            result = pipeline.run_pipeline(image_bytes)

            pred_id = result.get("Số", "").strip()
            pred_name = result.get("Họ và tên", "").strip()

            # Metrics
            id_cer = cer(gt_id, pred_id)
            id_wer = wer(gt_id, pred_id)

            name_cer = cer(gt_name, pred_name)
            name_wer = wer(gt_name, pred_name)

            total_id_cer += id_cer
            total_id_wer += id_wer

            total_name_cer += name_cer
            total_name_wer += name_wer

            total_samples += 1

            print("=" * 50)
            print(f"Image: {image_path.name}")

            print(f"GT ID     : {gt_id}")
            print(f"PRED ID   : {pred_id}")

            print(f"GT NAME   : {gt_name}")
            print(f"PRED NAME : {pred_name}")

            print(f"ID CER    : {id_cer:.4f}")
            print(f"ID WER    : {id_wer:.4f}")

            print(f"NAME CER  : {name_cer:.4f}")
            print(f"NAME WER  : {name_wer:.4f}")

        except Exception as e:
            print(f"Error processing {image_path.name}: {e}")

    # =========================
    # FINAL RESULTS
    # =========================
    if total_samples == 0:
        print("No samples processed.")
        return

    avg_id_cer = total_id_cer / total_samples
    avg_id_wer = total_id_wer / total_samples

    avg_name_cer = total_name_cer / total_samples
    avg_name_wer = total_name_wer / total_samples

    print("\n")
    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)

    print(f"Total Samples: {total_samples}")

    print("\n--- ID FIELD ---")
    print(f"Average CER: {avg_id_cer:.4f}")
    print(f"Average WER: {avg_id_wer:.4f}")

    print("\n--- NAME FIELD ---")
    print(f"Average CER: {avg_name_cer:.4f}")
    print(f"Average WER: {avg_name_wer:.4f}")


if __name__ == "__main__":
    main()