import os
from PIL import Image, ImageDraw
import random

def create_mock_image(save_path, is_leaf):
    img = Image.new('RGB', (224, 224), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    if is_leaf:
        # Draw some green shapes to resemble a leaf
        color = (0, random.randint(100, 200), 0)
        points = [(random.randint(50, 150), random.randint(20, 100)),
                  (random.randint(100, 200), random.randint(100, 200)),
                  (random.randint(20, 100), random.randint(100, 200))]
        draw.polygon(points, fill=color)
    else:
        # Draw some arbitrary random shapes for garbage
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        shape_type = random.choice(['rectangle', 'ellipse'])
        box = [random.randint(20, 100), random.randint(20, 100), random.randint(120, 200), random.randint(120, 200)]
        if shape_type == 'rectangle':
            draw.rectangle(box, fill=color)
        else:
            draw.ellipse(box, fill=color)

    img.save(save_path)

def main():
    base_dir = "dataset"
    leaf_dir = os.path.join(base_dir, "1_leaf")
    garbage_dir = os.path.join(base_dir, "0_garbage")

    os.makedirs(leaf_dir, exist_ok=True)
    os.makedirs(garbage_dir, exist_ok=True)

    print("Generating Mock Leaf Images...")
    for i in range(10):
        create_mock_image(os.path.join(leaf_dir, f"leaf_{i}.jpg"), is_leaf=True)

    print("Generating Mock Garbage Images...")
    for i in range(10):
        create_mock_image(os.path.join(garbage_dir, f"garbage_{i}.jpg"), is_leaf=False)

    print("Data preparation complete.")

if __name__ == "__main__":
    main()
