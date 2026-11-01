import os
import sys
import json
import io
import numpy as np
from PIL import Image

# Ensure backend directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from predict import diagnose_crop

def test_pipeline():
    print("==================================================")
    print("  VERIFYING TOP 10 INDIAN CROPS & BOLLWORM FIX   ")
    print("==================================================")

    test_cases = []

    # 1. Cotton Bollworm on green leaf
    cotton_bw_dir = os.path.join(BASE_DIR, "dataset_indian", "Cotton___Bollworm")
    if os.path.exists(cotton_bw_dir):
        files = [f for f in os.listdir(cotton_bw_dir) if f.startswith("bollworm_leaf_")]
        if files:
            test_cases.append(("Cotton Bollworm (on green foliage)", os.path.join(cotton_bw_dir, files[0]), "Cotton", "Bollworm"))

    # 2. Rice Blast
    rice_dir = os.path.join(BASE_DIR, "dataset_indian", "Rice___Blast")
    if os.path.exists(rice_dir):
        files = [f for f in os.listdir(rice_dir) if f.endswith(".jpg")]
        if files:
            test_cases.append(("Rice Blast", os.path.join(rice_dir, files[0]), "Rice", "Blast"))

    # 3. Sugarcane Red Rot
    sugar_dir = os.path.join(BASE_DIR, "dataset_indian", "Sugarcane___Red_Rot")
    if os.path.exists(sugar_dir):
        files = [f for f in os.listdir(sugar_dir) if f.endswith(".jpg")]
        if files:
            test_cases.append(("Sugarcane Red Rot", os.path.join(sugar_dir, files[0]), "Sugarcane", "Red Rot"))

    # 4. Wheat Rust
    wheat_dir = os.path.join(BASE_DIR, "dataset_indian", "Wheat___Rust")
    if os.path.exists(wheat_dir):
        files = [f for f in os.listdir(wheat_dir) if f.endswith(".jpg")]
        if files:
            test_cases.append(("Wheat Rust", os.path.join(wheat_dir, files[0]), "Wheat", "Rust"))

    # 5. Maize Fall Armyworm
    maize_dir = os.path.join(BASE_DIR, "dataset_indian", "Maize___Fall_Armyworm")
    if os.path.exists(maize_dir):
        files = [f for f in os.listdir(maize_dir) if f.endswith(".jpg")]
        if files:
            test_cases.append(("Maize Fall Armyworm", os.path.join(maize_dir, files[0]), "Maize", "Fall Armyworm"))

    # 6. Non-crop / Garbage Test
    garbage_dir = os.path.join(BASE_DIR, "dataset", "0_garbage")
    if os.path.exists(garbage_dir):
        files = [f for f in os.listdir(garbage_dir) if f.endswith(".jpg")]
        if files:
            test_cases.append(("Non-Crop Object (Bouncer Block)", os.path.join(garbage_dir, files[0]), "ERROR", "not_a_crop"))

    passed = 0
    total = len(test_cases)

    for desc, img_path, exp_crop, exp_disease in test_cases:
        print(f"\n--- Testing: {desc} ---")
        print(f"File: {os.path.basename(img_path)}")
        with open(img_path, "rb") as f:
            img_bytes = f.read()

        res = diagnose_crop(img_bytes)
        print(f"Result: {json.dumps(res, indent=2)}")

        if exp_crop == "ERROR":
            if res.get("error") == exp_disease:
                print(f"[PASS] Correctly blocked non-crop: {res.get('error')}")
                passed += 1
            else:
                print(f"[FAIL] Expected error {exp_disease}, got {res}")
        else:
            pred_crop = res.get("crop")
            pred_disease = res.get("disease")
            pred_conf = res.get("confidence")

            # Check matching
            crop_match = exp_crop.lower() in str(pred_crop).lower()
            disease_match = exp_disease.lower() in str(pred_disease).lower()

            if crop_match and disease_match:
                print(f"[PASS] {pred_crop} - {pred_disease} ({pred_conf}) matched expected {exp_crop} - {exp_disease}!")
                passed += 1
            else:
                print(f"[WARN/FAIL] Expected {exp_crop} - {exp_disease}, got {pred_crop} - {pred_disease} ({pred_conf})")

    print("\n==================================================")
    print(f"  TEST SUMMARY: {passed} / {total} PASSED")
    print("==================================================")

if __name__ == "__main__":
    test_pipeline()
