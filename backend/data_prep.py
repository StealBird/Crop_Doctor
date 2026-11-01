import os
import io
import zipfile
import shutil
import numpy as np
from PIL import Image, ImageFilter
import pyarrow.parquet as pq

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
LEAF_DIR = os.path.join(DATASET_DIR, "1_leaf")
GARBAGE_DIR = os.path.join(DATASET_DIR, "0_garbage")

def prep_leaves():
    os.makedirs(LEAF_DIR, exist_ok=True)
    parquet_path = os.path.join(BASE_DIR, "plant_test.parquet")
    if not os.path.exists(parquet_path):
        import urllib.request
        url = "https://huggingface.co/datasets/GVJahnavi/Plant_village_subset/resolve/main/data/test-00000-of-00001.parquet"
        print("Downloading PlantVillage leaf dataset...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            with open(parquet_path, "wb") as f:
                f.write(resp.read())

    print("Extracting real leaf images from PlantVillage...")
    table = pq.read_table(parquet_path)
    img_col = table["image"]
    total = min(1200, table.num_rows)
    for i in range(total):
        img_bytes = img_col[i]["bytes"].as_py()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((224, 224))
        img.save(os.path.join(LEAF_DIR, f"real_leaf_{i:04d}.jpg"), quality=90)
    print(f"Extracted {total} real leaf images.")

def prep_trashnet():
    os.makedirs(GARBAGE_DIR, exist_ok=True)
    zip_path = os.path.join(BASE_DIR, "trashnet.zip")
    if not os.path.exists(zip_path):
        import urllib.request
        url = "https://huggingface.co/datasets/garythung/trashnet/resolve/main/dataset-resized.zip"
        print("Downloading TrashNet (real objects: plastic, metal, cardboard, glass, paper)...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            with open(zip_path, "wb") as f:
                f.write(resp.read())

    print("Extracting real non-leaf objects from TrashNet...")
    count = 0
    with zipfile.ZipFile(zip_path, "r") as zf:
        for name in zf.namelist():
            if name.lower().endswith((".jpg", ".jpeg", ".png")) and not name.startswith("__MACOSX"):
                data = zf.read(name)
                try:
                    img = Image.open(io.BytesIO(data)).convert("RGB").resize((224, 224))
                    img.save(os.path.join(GARBAGE_DIR, f"trash_{count:04d}.jpg"), quality=90)
                    count += 1
                    if count >= 1000:
                        break
                except Exception:
                    pass
    print(f"Extracted {count} real object images.")

def prep_synthetic_environmental():
    print("Generating environmental non-leaf textures (soil, skin, sky, indoor surfaces)...")
    np.random.seed(42)
    count = 0

    # 1. Human skin tones (hands, fingers, faces)
    skin_base_colors = [
        (245, 220, 200), (230, 190, 160), (210, 160, 120),
        (180, 130, 90),  (140, 90, 60),   (90, 55, 35)
    ]
    for i, base in enumerate(skin_base_colors):
        for j in range(25):
            arr = np.ones((224, 224, 3), dtype=np.float32)
            noise = np.random.normal(0, 12, (224, 224, 3))
            arr[:, :] = base
            arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
            img = Image.fromarray(arr).filter(ImageFilter.GaussianBlur(radius=2))
            img.save(os.path.join(GARBAGE_DIR, f"env_skin_{count:04d}.jpg"), quality=90)
            count += 1

    # 2. Agricultural soil and mud textures
    soil_base_colors = [
        (80, 50, 30), (105, 75, 45), (130, 100, 70),
        (60, 45, 35), (90, 80, 65),  (120, 95, 60)
    ]
    for i, base in enumerate(soil_base_colors):
        for j in range(25):
            arr = np.ones((224, 224, 3), dtype=np.float32)
            noise = np.random.normal(0, 25, (224, 224, 3))
            arr[:, :] = base
            arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
            img = Image.fromarray(arr)
            img.save(os.path.join(GARBAGE_DIR, f"env_soil_{count:04d}.jpg"), quality=90)
            count += 1

    # 3. Sky, daylight, clouds, indoor walls
    sky_colors = [
        (135, 206, 235), (176, 224, 230), (240, 248, 255),
        (220, 220, 220), (180, 180, 190), (70, 70, 80)
    ]
    for i, base in enumerate(sky_colors):
        for j in range(15):
            arr = np.ones((224, 224, 3), dtype=np.float32)
            noise = np.random.normal(0, 10, (224, 224, 3))
            arr[:, :] = base
            arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
            img = Image.fromarray(arr).filter(ImageFilter.GaussianBlur(radius=3))
            img.save(os.path.join(GARBAGE_DIR, f"env_sky_{count:04d}.jpg"), quality=90)
            count += 1

    print(f"Generated {count} environmental non-leaf textures.")

def main():
    if os.path.exists(LEAF_DIR):
        shutil.rmtree(LEAF_DIR)
    if os.path.exists(GARBAGE_DIR):
        shutil.rmtree(GARBAGE_DIR)

    prep_leaves()
    prep_trashnet()
    prep_synthetic_environmental()

    leaves = len(os.listdir(LEAF_DIR))
    garbage = len(os.listdir(GARBAGE_DIR))
    print(f"\n==========================================")
    print(f"Dataset preparation complete:")
    print(f"  Class 1 (Real Crop Leaves):     {leaves} images")
    print(f"  Class 0 (Non-Leaf Objects/Env): {garbage} images")
    print(f"==========================================\n")

if __name__ == "__main__":
    main()
