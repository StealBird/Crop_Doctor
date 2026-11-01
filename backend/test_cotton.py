import os
import json
from predict import diagnose_crop

def run_tests():
    print("=== CROP DOCTOR 3-STAGE PIPELINE TESTS ===")

    test_cases = [
        {
            "name": "Cotton Bollworm",
            "path": "backend/dataset_cotton/0_Bollworm/pest_full_0000.jpg",
            "expected_crop": "Cotton",
            "expected_condition": "Bollworm",
            "expect_error": False,
        },
        {
            "name": "Cotton Bacterial Blight",
            "path": "backend/dataset_cotton/1_Bacterial_Blight/bacterial_blight_0000.jpg",
            "expected_crop": "Cotton",
            "expected_condition": "Bacterial Blight",
            "expect_error": False,
        },
        {
            "name": "Cotton Leaf Curl Virus",
            "path": "backend/dataset_cotton/2_Curl_Virus/curl_virus_0000.jpg",
            "expected_crop": "Cotton",
            "expected_condition": "Curl Virus",
            "expect_error": False,
        },
        {
            "name": "Standard Crop: Apple Scab",
            "path": "backend/dataset/1_leaf/real_leaf_0000.jpg",
            "expected_crop": "Apple",
            "expected_condition": "Apple scab",
            "expect_error": False,
        },
        {
            "name": "Non-Crop: Trash Object",
            "path": "backend/dataset/0_garbage/trash_0000.jpg",
            "expected_crop": None,
            "expected_condition": None,
            "expect_error": True,
        },
    ]

    all_passed = True
    for tc in test_cases:
        print(f"\n--- Testing: {tc['name']} ---")
        if not os.path.exists(tc["path"]):
            print(f"[SKIP] Test file {tc['path']} not found.")
            continue

        with open(tc["path"], "rb") as f:
            img_bytes = f.read()

        result = diagnose_crop(img_bytes)
        print(f"Result: {result.get('crop')} | {result.get('disease')} | Confidence: {result.get('confidence')} | Error: {result.get('error')}")

        if tc["expect_error"]:
            if result.get("error") == "not_a_crop":
                print(f"[PASS] Blocked by Gatekeeper as expected ({result.get('message')})")
            else:
                print(f"[FAIL] Expected gatekeeper error, but got: {result}")
                all_passed = False
        else:
            if result.get("error"):
                print(f"[FAIL] Unexpected error: {result}")
                all_passed = False
            else:
                crop = result.get("crop")
                disease = result.get("disease")
                if crop == tc["expected_crop"] and tc["expected_condition"].lower() in disease.lower():
                    print(f"[PASS] Correctly diagnosed as {crop} - {disease} ({result.get('confidence')})")
                    print(f"       Organic cure: {result.get('organic_cure')[:60]}...")
                    print(f"       Chemical cure: {result.get('chemical_cure')[:60]}...")
                else:
                    print(f"[FAIL] Expected {tc['expected_crop']} - {tc['expected_condition']}, got {crop} - {disease}")
                    all_passed = False

    print("\n" + ("=" * 45))
    if all_passed:
        print("[ALL TESTS PASSED] 3-Stage Pipeline operates with high accuracy!")
    else:
        print("[SOME TESTS FAILED] Review test output above.")
    print("=" * 45)

if __name__ == "__main__":
    run_tests()
