import requests
import os
import subprocess
import time

def test_endpoint(image_path, expected_status):
    url = "http://localhost:8000/predict"
    print(f"\n--- Testing {image_path} (Expected: {expected_status}) ---")
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post(url, files=files)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
            print("[PASS]")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting uvicorn server...")
    base = os.path.dirname(os.path.abspath(__file__))
    server = subprocess.Popen(["python", "-m", "uvicorn", "main:app", "--port", "8000"], cwd=base)
    time.sleep(12)
    
    try:
        # Test 1: Real leaf
        test_endpoint(os.path.join(base, "dataset/1_leaf/real_leaf_0000.jpg"), 200)
        # Test 2: Real non-leaf everyday object
        test_endpoint(os.path.join(base, "dataset/0_garbage/trash_0000.jpg"), 400)
        # Test 3: Real skin / hand tone
        test_endpoint(os.path.join(base, "dataset/0_garbage/env_skin_0000.jpg"), 400)
    finally:
        print("\nStopping uvicorn server...")
        server.terminate()
        server.wait()
