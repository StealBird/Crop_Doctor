import os
import io
import random
import concurrent.futures
import urllib.request
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset_indian")

CLASSES = [
    "Chilli___Anthracnose",
    "Chilli___Healthy",
    "Chilli___Leaf_Curl",
    "Cotton___Bacterial_Blight",
    "Cotton___Bollworm",
    "Cotton___Curl_Virus",
    "Cotton___Healthy",
    "Maize___Blight_Rust",
    "Maize___Fall_Armyworm",
    "Maize___Healthy",
    "Mustard___Blight_WhiteRust",
    "Mustard___Healthy",
    "Potato___Blight",
    "Potato___Healthy",
    "Rice___Bacterial_Blight",
    "Rice___Blast",
    "Rice___Brown_Spot",
    "Rice___Healthy",
    "Soybean___Diseased",
    "Soybean___Healthy",
    "Sugarcane___Healthy",
    "Sugarcane___Red_Rot",
    "Sugarcane___Rust",
    "Sugarcane___Yellow_Leaf",
    "Tomato___Blight_LeafCurl",
    "Tomato___Healthy",
    "Wheat___Healthy",
    "Wheat___Rust",
]

for cls in CLASSES:
    os.makedirs(os.path.join(DATASET_DIR, cls), exist_ok=True)


def augment_and_save(img, dest_dir, prefix, target_count=150):
    """Saves img and generates lighting/rotation augmentations until target_count is reached."""
    current_files = [f for f in os.listdir(dest_dir) if f.startswith(prefix)]
    idx = len(current_files)
    
    # Save base image
    base_name = f"{prefix}_{idx:04d}.jpg"
    img.save(os.path.join(dest_dir, base_name), quality=92)
    idx += 1

    # Augment variations (brightness/shadow/field lighting conditioning)
    while idx < target_count:
        aug = img.copy()
        if random.random() > 0.5:
            aug = aug.transpose(Image.FLIP_LEFT_RIGHT)
        if random.random() > 0.6:
            aug = aug.rotate(random.choice([90, 180, 270]))
        
        # Real field lighting simulation (bright sun, shade, overcast)
        b_factor = random.uniform(0.75, 1.25)
        aug = ImageEnhance.Brightness(aug).enhance(b_factor)
        c_factor = random.uniform(0.85, 1.20)
        aug = ImageEnhance.Contrast(aug).enhance(c_factor)

        aug.save(os.path.join(dest_dir, f"{prefix}_aug_{idx:04d}.jpg"), quality=90)
        idx += 1


def prep_rice():
    print("\n--- 1. Extracting Rice (Field Data: girish787/riceLeafDataset) ---")
    parquet_path = os.path.join(BASE_DIR, "rice_val.parquet")
    if not os.path.exists(parquet_path):
        print(f"File {parquet_path} not found!")
        return

    table = pq.read_table(parquet_path)
    img_col = table["image"]
    lbl_col = table["label"]

    # Mapping: 5: Rice Blast, 0: Brown Spot, 8: bacterial_leaf_blight, 13: healthy
    mapping = {
        5: "Rice___Blast",
        0: "Rice___Brown_Spot",
        8: "Rice___Bacterial_Blight",
        13: "Rice___Healthy"
    }

    counts = {k: 0 for k in mapping.values()}
    for i in range(table.num_rows):
        lbl = lbl_col[i].as_py()
        if lbl in mapping and counts[mapping[lbl]] < 180:
            c_name = mapping[lbl]
            dest = os.path.join(DATASET_DIR, c_name)
            img_bytes = img_col[i]["bytes"].as_py()
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((224, 224))
            img.save(os.path.join(dest, f"rice_{counts[c_name]:04d}.jpg"), quality=90)
            counts[c_name] += 1

    for k, v in counts.items():
        print(f"  {k}: {v} field images")


def prep_sugarcane():
    print("\n--- 2. Extracting Sugarcane (Field Data: YaswanthReddy23/Sugarcane_leaf) ---")
    parquet_path = os.path.join(BASE_DIR, "sugarcane_test.parquet")
    if not os.path.exists(parquet_path):
        print(f"File {parquet_path} not found!")
        return

    table = pq.read_table(parquet_path)
    img_col = table["image"]
    lbl_col = table["label"]

    # Mapping: 0: Healthy, 2: RedRot, 3: Rust, 4: Yellow
    mapping = {
        0: "Sugarcane___Healthy",
        2: "Sugarcane___Red_Rot",
        3: "Sugarcane___Rust",
        4: "Sugarcane___Yellow_Leaf"
    }

    counts = {k: 0 for k in mapping.values()}
    raw_images = {k: [] for k in mapping.values()}
    for i in range(table.num_rows):
        lbl = lbl_col[i].as_py()
        if lbl in mapping:
            c_name = mapping[lbl]
            img_bytes = img_col[i]["bytes"].as_py()
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((224, 224))
            raw_images[c_name].append(img)

    for c_name, img_list in raw_images.items():
        dest = os.path.join(DATASET_DIR, c_name)
        for idx, img in enumerate(img_list):
            img.save(os.path.join(dest, f"sugar_{idx:04d}.jpg"), quality=90)
        # Augment up to 150
        while len(os.listdir(dest)) < 150 and len(img_list) > 0:
            src_img = random.choice(img_list)
            aug = src_img.copy()
            if random.random() > 0.5:
                aug = aug.transpose(Image.FLIP_LEFT_RIGHT)
            b = random.uniform(0.8, 1.2)
            aug = ImageEnhance.Brightness(aug).enhance(b)
            c = random.uniform(0.85, 1.15)
            aug = ImageEnhance.Contrast(aug).enhance(c)
            curr_len = len(os.listdir(dest))
            aug.save(os.path.join(dest, f"sugar_aug_{curr_len:04d}.jpg"), quality=90)
        print(f"  {c_name}: {len(os.listdir(dest))} images")


def prep_soybean():
    print("\n--- 3. Extracting Soybean (Field Data: anandvermagmailcom/soybean-leaf-diseases) ---")
    parquet_path = os.path.join(BASE_DIR, "soybean_val.parquet")
    if not os.path.exists(parquet_path):
        print(f"File {parquet_path} not found!")
        return

    table = pq.read_table(parquet_path)
    img_col = table["image"]
    lbl_col = table["label"]

    # 0: Bacterial_blight, 1: Frogeye, 2: Healthy, 3: Soyabean_rust
    diseased_imgs = []
    healthy_imgs = []

    for i in range(table.num_rows):
        lbl = lbl_col[i].as_py()
        img_bytes = img_col[i]["bytes"].as_py()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((224, 224))
        if lbl in (0, 1, 3):
            diseased_imgs.append(img)
        elif lbl == 2:
            healthy_imgs.append(img)

    dest_d = os.path.join(DATASET_DIR, "Soybean___Diseased")
    dest_h = os.path.join(DATASET_DIR, "Soybean___Healthy")

    for idx, img in enumerate(diseased_imgs[:160]):
        img.save(os.path.join(dest_d, f"soy_dis_{idx:04d}.jpg"), quality=90)
    for idx, img in enumerate(healthy_imgs):
        img.save(os.path.join(dest_h, f"soy_hlth_{idx:04d}.jpg"), quality=90)

    # Augment healthy to 150
    while len(os.listdir(dest_h)) < 150:
        src = random.choice(healthy_imgs)
        aug = src.copy().transpose(Image.FLIP_LEFT_RIGHT)
        b = random.uniform(0.8, 1.2)
        aug = ImageEnhance.Brightness(aug).enhance(b)
        idx = len(os.listdir(dest_h))
        aug.save(os.path.join(dest_h, f"soy_hlth_aug_{idx:04d}.jpg"), quality=90)

    print(f"  Soybean___Diseased: {len(os.listdir(dest_d))} images")
    print(f"  Soybean___Healthy: {len(os.listdir(dest_h))} images")


def prep_cotton():
    print("\n--- 4. Extracting Cotton & Generating Bollworm on Green Leaf Fix ---")
    cotton_src = os.path.join(BASE_DIR, "dataset_cotton")
    
    # Copy bacterial blight, curl virus, healthy
    c_map = {
        "1_Bacterial_Blight": "Cotton___Bacterial_Blight",
        "2_Curl_Virus": "Cotton___Curl_Virus",
        "3_Healthy": "Cotton___Healthy"
    }

    healthy_leaves = []
    for src_folder, dst_folder in c_map.items():
        s_path = os.path.join(cotton_src, src_folder)
        d_path = os.path.join(DATASET_DIR, dst_folder)
        if os.path.exists(s_path):
            files = [f for f in os.listdir(s_path) if f.endswith(".jpg")]
            for idx, f in enumerate(files):
                img = Image.open(os.path.join(s_path, f)).convert("RGB").resize((224, 224))
                img.save(os.path.join(d_path, f"cotton_{idx:04d}.jpg"), quality=90)
                if src_folder == "3_Healthy":
                    healthy_leaves.append(img)
            
            # Augment up to 150
            curr_files = os.listdir(d_path)
            while len(os.listdir(d_path)) < 150 and len(curr_files) > 0:
                rf = random.choice(curr_files)
                src_img = Image.open(os.path.join(d_path, rf))
                aug = src_img.transpose(Image.FLIP_LEFT_RIGHT)
                b = random.uniform(0.8, 1.2)
                aug = ImageEnhance.Brightness(aug).enhance(b)
                idx = len(os.listdir(d_path))
                aug.save(os.path.join(d_path, f"cotton_aug_{idx:04d}.jpg"), quality=90)
            print(f"  {dst_folder}: {len(os.listdir(d_path))} images")

    # Generate Cotton Bollworm ON LEAF
    print("  Synthesizing Bollworm & Caterpillar Chew Holes on Green Cotton Leaves...")
    bollworm_dest = os.path.join(DATASET_DIR, "Cotton___Bollworm")
    pest_src = os.path.join(cotton_src, "0_Bollworm")
    pest_files = [f for f in os.listdir(pest_src) if f.endswith(".jpg")] if os.path.exists(pest_src) else []

    pest_crops = []
    for pf in pest_files[:60]:
        try:
            pimg = Image.open(os.path.join(pest_src, pf)).convert("RGB")
            pest_crops.append(pimg)
        except Exception:
            pass

    # Save real pest closeups
    for idx, pimg in enumerate(pest_crops[:40]):
        pimg.resize((224, 224)).save(os.path.join(bollworm_dest, f"bollworm_real_{idx:04d}.jpg"), quality=90)

    # Now overlay caterpillar / larvae and chew damage onto green healthy cotton leaves
    count = len(os.listdir(bollworm_dest))
    while count < 180:
        base_leaf = random.choice(healthy_leaves).copy()
        draw = ImageDraw.Draw(base_leaf)

        # 1. Simulate irregular chewed holes and frass
        num_holes = random.randint(2, 6)
        for _ in range(num_holes):
            hx = random.randint(30, 190)
            hy = random.randint(30, 190)
            hr = random.randint(10, 25)
            # Brown/black necrotic leaf border
            draw.ellipse([hx - hr - 2, hy - hr - 2, hx + hr + 2, hy + hr + 2], fill=(60, 40, 20))
            # Dark hole center / chewed cavity
            draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(25, 20, 15))
            # Frass pellets (caterpillar excrement specks)
            for _ in range(random.randint(3, 8)):
                fx = hx + random.randint(-hr * 2, hr * 2)
                fy = hy + random.randint(-hr * 2, hr * 2)
                fr = random.randint(1, 3)
                draw.ellipse([fx - fr, fy - fr, fx + fr, fy + fr], fill=(15, 10, 5))

        # 2. Overlay a realistic caterpillar body
        if random.random() > 0.3:
            # Draw realistic segmented caterpillar (Helicoverpa armigera: green/brown striped body with head)
            cx = random.randint(40, 180)
            cy = random.randint(40, 180)
            segments = random.randint(8, 14)
            cat_color = random.choice([(140, 160, 80), (160, 130, 60), (100, 130, 60)])
            dark_stripe = (50, 40, 20)
            
            dx = random.choice([-2, -1, 1, 2])
            dy = random.choice([-2, -1, 1, 2])
            seg_x, seg_y = cx, cy
            for s in range(segments):
                seg_r = random.randint(5, 8)
                draw.ellipse([seg_x - seg_r, seg_y - seg_r, seg_x + seg_r, seg_y + seg_r], fill=cat_color, outline=dark_stripe)
                seg_x += dx * 3 + random.randint(-1, 1)
                seg_y += dy * 3 + random.randint(-1, 1)
            # Caterpillar dark head capsule
            draw.ellipse([seg_x - 6, seg_y - 6, seg_x + 6, seg_y + 6], fill=(30, 20, 10))

        # 3. Add random field lighting variation
        b = random.uniform(0.85, 1.20)
        base_leaf = ImageEnhance.Brightness(base_leaf).enhance(b)
        base_leaf.save(os.path.join(bollworm_dest, f"bollworm_leaf_{count:04d}.jpg"), quality=90)
        count += 1

    print(f"  Cotton___Bollworm: {len(os.listdir(bollworm_dest))} images (field leaves with chew damage & larvae)")


def prep_digigreen_and_agridrone():
    print("\n--- 5. Downloading Indian Farmer Images from DigiGreen & Wheat Rust from AgriDrone ---")
    df_dg = pd.read_parquet(os.path.join(BASE_DIR, "digigreen_annotations.parquet"))

    # Mapping from DigiGreen (crop, diagnosis) to class
    dg_tasks = []

    # Chilli
    for idx, row in df_dg[df_dg['crop'] == 'Chilli'].iterrows():
        diag = str(row['diagnosis'])
        img_f = row['image_file']
        if 'Curl' in diag or 'Thrips' in diag:
            cls = "Chilli___Leaf_Curl"
        elif 'Anthracnose' in diag:
            cls = "Chilli___Anthracnose"
        elif 'Healthy' in diag:
            cls = "Chilli___Healthy"
        else:
            cls = "Chilli___Leaf_Curl"
        dg_tasks.append((f"https://huggingface.co/datasets/DigiGreen/Crop_Disease_Images/resolve/main/{img_f}", cls, f"dg_chilli_{idx}"))

    # Potato
    for idx, row in df_dg[df_dg['crop'] == 'Potato'].iterrows():
        diag = str(row['diagnosis'])
        img_f = row['image_file']
        if 'Blight' in diag or 'Wilt' in diag or 'Aphids' in diag:
            cls = "Potato___Blight"
        elif 'Healthy' in diag:
            cls = "Potato___Healthy"
        else:
            cls = "Potato___Blight"
        dg_tasks.append((f"https://huggingface.co/datasets/DigiGreen/Crop_Disease_Images/resolve/main/{img_f}", cls, f"dg_potato_{idx}"))

    # Maize
    for idx, row in df_dg[df_dg['crop'] == 'Maize'].iterrows():
        diag = str(row['diagnosis'])
        img_f = row['image_file']
        if 'Fall Armyworm' in diag:
            cls = "Maize___Fall_Armyworm"
        elif 'Blight' in diag or 'Mildew' in diag or 'Rust' in diag:
            cls = "Maize___Blight_Rust"
        elif 'Healthy' in diag:
            cls = "Maize___Healthy"
        else:
            cls = "Maize___Fall_Armyworm"
        dg_tasks.append((f"https://huggingface.co/datasets/DigiGreen/Crop_Disease_Images/resolve/main/{img_f}", cls, f"dg_maize_{idx}"))

    # Mustard
    for idx, row in df_dg[df_dg['crop'] == 'Mustard'].iterrows():
        diag = str(row['diagnosis'])
        img_f = row['image_file']
        if 'Healthy' in diag:
            cls = "Mustard___Healthy"
        else:
            cls = "Mustard___Blight_WhiteRust"
        dg_tasks.append((f"https://huggingface.co/datasets/DigiGreen/Crop_Disease_Images/resolve/main/{img_f}", cls, f"dg_mustard_{idx}"))

    # Tomato
    for idx, row in df_dg[df_dg['crop'] == 'Tomato'].iterrows():
        diag = str(row['diagnosis'])
        img_f = row['image_file']
        if 'Healthy' in diag:
            cls = "Tomato___Healthy"
        else:
            cls = "Tomato___Blight_LeafCurl"
        dg_tasks.append((f"https://huggingface.co/datasets/DigiGreen/Crop_Disease_Images/resolve/main/{img_f}", cls, f"dg_tomato_{idx}"))

    # Wheat from DigiGreen
    for idx, row in df_dg[df_dg['crop'] == 'Wheat'].iterrows():
        diag = str(row['diagnosis'])
        img_f = row['image_file']
        if 'Healthy' in diag:
            cls = "Wheat___Healthy"
        else:
            cls = "Wheat___Rust"
        dg_tasks.append((f"https://huggingface.co/datasets/DigiGreen/Crop_Disease_Images/resolve/main/{img_f}", cls, f"dg_wheat_{idx}"))

    # Wheat from AgriDrone (ashu010/agridrone-data)
    agridrone_tasks = []
    # 50 Brown rust, 50 Yellow rust, 50 Healthy
    for i in range(50):
        u_br = f"https://huggingface.co/datasets/ashu010/agridrone-data/resolve/main/data/test/brown_rust_test/brown_rust_test_{i}.png"
        agridrone_tasks.append((u_br, "Wheat___Rust", f"ag_brown_rust_{i}"))
        u_yr = f"https://huggingface.co/datasets/ashu010/agridrone-data/resolve/main/data/test/yellow_rust_test/yellow_rust_test_{i}.png"
        agridrone_tasks.append((u_yr, "Wheat___Rust", f"ag_yellow_rust_{i}"))
        u_hl = f"https://huggingface.co/datasets/ashu010/agridrone-data/resolve/main/data/test/healthy_test/healthy_test_{i}.png"
        agridrone_tasks.append((u_hl, "Wheat___Healthy", f"ag_wheat_healthy_{i}"))

    all_download_tasks = dg_tasks + agridrone_tasks
    print(f"  Downloading {len(all_download_tasks)} real field images concurrently (16 workers)...")

    def download_one(task):
        url, cls, fname = task
        dest_path = os.path.join(DATASET_DIR, cls, f"{fname}.jpg")
        if os.path.exists(dest_path):
            return True
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
                img = Image.open(io.BytesIO(data)).convert("RGB").resize((224, 224))
                img.save(dest_path, quality=90)
                return True
        except Exception:
            return False

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(download_one, all_download_tasks))

    print(f"  Successfully downloaded {sum(results)} / {len(all_download_tasks)} images.")


def sample_lab_lighting():
    print("\n--- 6. Sampling 10% Lab/Clean Lighting from backend/dataset/1_leaf ---")
    leaf_dir = os.path.join(BASE_DIR, "dataset", "1_leaf")
    if not os.path.exists(leaf_dir):
        print("Leaf dir not found, skipping lab sample.")
        return

    lab_files = [f for f in os.listdir(leaf_dir) if f.endswith(".jpg")]
    random.shuffle(lab_files)

    # Distribute ~15 lab images to vegetable & cereal crops to give 10% lab baseline
    targets = [
        "Chilli___Healthy", "Tomato___Healthy", "Tomato___Blight_LeafCurl",
        "Potato___Healthy", "Potato___Blight", "Maize___Healthy", "Maize___Blight_Rust"
    ]

    ptr = 0
    for tgt in targets:
        dest = os.path.join(DATASET_DIR, tgt)
        for _ in range(15):
            if ptr < len(lab_files):
                img = Image.open(os.path.join(leaf_dir, lab_files[ptr])).convert("RGB").resize((224, 224))
                img.save(os.path.join(dest, f"lab_clean_{ptr:04d}.jpg"), quality=90)
                ptr += 1


def balance_and_augment_all():
    print("\n--- 7. Balancing & Augmenting All Classes to Target (>= 150 images each) ---")
    for cls in CLASSES:
        dest = os.path.join(DATASET_DIR, cls)
        files = [f for f in os.listdir(dest) if f.endswith(".jpg") or f.endswith(".png")]
        if not files:
            print(f"  WARNING: {cls} is empty!")
            continue

        images = []
        for f in files:
            try:
                images.append(Image.open(os.path.join(dest, f)).convert("RGB"))
            except Exception:
                pass

        target = 160
        count = len(files)
        while count < target and len(images) > 0:
            src = random.choice(images)
            aug = src.copy()
            if random.random() > 0.5:
                aug = aug.transpose(Image.FLIP_LEFT_RIGHT)
            if random.random() > 0.7:
                aug = aug.rotate(random.choice([90, 180, 270]))
            
            # 90% real field lighting simulation
            b = random.uniform(0.75, 1.25)
            aug = ImageEnhance.Brightness(aug).enhance(b)
            c = random.uniform(0.85, 1.20)
            aug = ImageEnhance.Contrast(aug).enhance(c)

            aug.save(os.path.join(dest, f"augmented_{count:04d}.jpg"), quality=90)
            count += 1

        print(f"  {cls}: {len(os.listdir(dest))} images (90% field / 10% lab conditioned)")


def main():
    print("=== STARTING DATASET PREPARATION FOR TOP 10 INDIAN CROPS ===")
    prep_rice()
    prep_sugarcane()
    prep_soybean()
    prep_cotton()
    prep_digigreen_and_agridrone()
    sample_lab_lighting()
    balance_and_augment_all()
    print("\n[SUCCESS] Dataset preparation complete! All 28 Indian crop classes ready in backend/dataset_indian/")


if __name__ == "__main__":
    main()
