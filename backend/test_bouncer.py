import requests
import os
import subprocess
import time

def test_endpoint(image_path, expected_status):
    url = "http://localhost:8000/predict"
    print(f"\n--- Testing {image_path} ---")
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post(url, files=files)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting uvicorn server...")
    server = subprocess.Popen(["python", "-m", "uvicorn", "main:app", "--port", "8000"])
    time.sleep(10) # wait for server to start
    
    try:
        test_endpoint("dataset/1_leaf/leaf_0.jpg", 200)
        test_endpoint("dataset/0_garbage/garbage_0.jpg", 400)
    finally:
        print("Stopping uvicorn server...")
        server.terminate()
        server.wait()
