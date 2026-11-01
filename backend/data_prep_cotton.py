import os
import io
import pyarrow.parquet as pq
from PIL import Image, ImageOps
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset_cotton")

CLASS_DIRS = {
    "bollworm": os.path.join(DATASET_DIR, "0_Bollworm"),
    "bacterial_blight": os.path.join(DATASET_DIR, "1_Bacterial_Blight"),
    "curl_virus": os.path.join(DATASET_DIR, "2_Curl_Virus"),
    "healthy": os.path.join(DATASET_DIR, "3_Healthy"),
    "other_crop": os.path.join(DATASET_DIR, "4_Other_Crop"),
}

for d in CLASS_DIRS.values():
    os.makedirs(d, exist_ok=True)

def prep_bollworm():
    print("\n--- Extracting Cotton Bollworm & Pest Samples ---")
    parquet_path = os.path.join(BASE_DIR, "pests_train.parquet")
    if not os.path.exists(parquet_path):
        print(f"File {parquet_path} not found!")
        return

    table = pq.read_table(parquet_path)
    img_col = table["image"]
    obj_col = table["objects"]
    w_col = table["width"]
    h_col = table["height"]

    count = 0
    # Targeted categories: 13 (Helicoverpa armigera / Cotton Bollworm), 25 (Spodoptera exigua / Armyworm)
    target_cats = {13, 25}

    for i in range(table.num_rows):
        obj = obj_col[i].as_py()
        if not obj or "category" not in obj:
            continue

        cats = obj.get("category", [])
        matched_cats = [c for c in cats if c in target_cats]
        if not matched_cats:
            continue

        img_bytes = img_col[i]["bytes"].as_py()
        full_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img_w = w_col[i].as_py()
        img_h = h_col[i].as_py()

        # 1. Save full image
        save_path = os.path.join(CLASS_DIRS["bollworm"], f"pest_full_{count:04d}.jpg")
        full_img.resize((224, 224)).save(save_path, quality=90)
        count += 1

        # 2. Extract crops for each matched bounding box
        bboxes = obj.get("bbox", [])
        for b_idx, cat in enumerate(cats):
            if cat in target_cats and b_idx < len(bboxes):
                bx, by, bw, bh = bboxes[b_idx]
                if bw > 10 and bh > 10:
                    pad_x = bw * 0.3
                    pad_y = bh * 0.3
                    x1 = max(0, int(bx - pad_x))
                    y1 = max(0, int(by - pad_y))
                    x2 = min(img_w, int(bx + bw + pad_x))
                    y2 = min(img_h, int(by + bh + pad_y))

                    crop = full_img.crop((x1, y1, x2, y2)).resize((224, 224))
                    crop.save(os.path.join(CLASS_DIRS["bollworm"], f"pest_crop_{count:04d}.jpg"), quality=90)
                    count += 1

                    # Augment with horizontal flip
                    crop.transpose(Image.FLIP_LEFT_RIGHT).save(
                        os.path.join(CLASS_DIRS["bollworm"], f"pest_aug_{count:04d}.jpg"), quality=90
                    )
                    count += 1

    print(f"Extracted {count} Bollworm & pest images into {CLASS_DIRS['bollworm']}")

def prep_cotton_diseases():
    print("\n--- Extracting Cotton Disease & Healthy Leaf Samples ---")
    parquet_files = [
        os.path.join(BASE_DIR, "cotton_leaf_test.parquet"),
        os.path.join(BASE_DIR, "cotton_leaf_val.parquet"),
    ]

    label_map = {
        0: "bacterial_blight",  # Bacterial Blight
        1: "curl_virus",        # Curl Virus
        2: "healthy",           # Healthy Leaf
    }

    counts = {k: 0 for k in label_map.values()}

    for p_path in parquet_files:
        if not os.path.exists(p_path):
            continue
        print(f"Reading {os.path.basename(p_path)}...")
        table = pq.read_table(p_path)
        img_col = table["image"]
        label_col = table["label"]

        for i in range(table.num_rows):
            lbl = label_col[i].as_py()
            if lbl in label_map:
                c_name = label_map[lbl]
                dest_dir = CLASS_DIRS[c_name]
                img_bytes = img_col[i]["bytes"].as_py()
                img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((224, 224))
                
                c_idx = counts[c_name]
                img.save(os.path.join(dest_dir, f"{c_name}_{c_idx:04d}.jpg"), quality=90)
                counts[c_name] += 1

    for k, v in counts.items():
        print(f"Extracted {v} images for Cotton {k}")

def prep_other_crops():
    print("\n--- Sampling Other Crops (Apple, Tomato, Grape, Corn, Pepper) ---")
    leaf_dir = os.path.join(BASE_DIR, "dataset", "1_leaf")
    dest_dir = CLASS_DIRS["other_crop"]

    if not os.path.exists(leaf_dir):
        print(f"Dataset dir {leaf_dir} not found!")
        return

    files = [f for f in os.listdir(leaf_dir) if f.endswith(".jpg")]
    # Take a balanced sample of 150 images
    step = max(1, len(files) // 150)
    sampled = files[::step][:150]

    count = 0
    for f in sampled:
        src = os.path.join(leaf_dir, f)
        img = Image.open(src).convert("RGB").resize((224, 224))
        img.save(os.path.join(dest_dir, f"other_crop_{count:04d}.jpg"), quality=90)
        count += 1

    print(f"Sampled {count} other crop leaves into {dest_dir}")

def main():
    prep_bollworm()
    prep_cotton_diseases()
    prep_other_crops()
    print("\n[SUCCESS] Cotton & Pest dataset preparation complete!")

if __name__ == "__main__":
    main()
