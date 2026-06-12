import os
import random
import shutil


# --- Configuration ---
source_dataset_dir = "/content/custom_data"
dest_dataset_dir = "/content/data"
images_dir = os.path.join(source_dataset_dir, "images")
labels_dir = os.path.join(source_dataset_dir, "labels")

train_ratio = 0.9  # 90% train, 10% validation

# Output directories
train_images = os.path.join(dest_dataset_dir, "images", "train")
val_images   = os.path.join(dest_dataset_dir, "images", "val")
train_labels = os.path.join(dest_dataset_dir, "labels", "train")
val_labels   = os.path.join(dest_dataset_dir, "labels", "val")

for d in [train_images, val_images, train_labels, val_labels]:
    os.makedirs(d, exist_ok=True)

# --- Collect all image files ---
image_files = [f for f in os.listdir(images_dir) if f.endswith((".jpg", ".png"))]
random.shuffle(image_files)

# --- Split into train/val ---
split_index = int(len(image_files) * train_ratio)
train_files = image_files[:split_index]
val_files   = image_files[split_index:]

def move_files(file_list, target_img_dir, target_lbl_dir):
    for img_file in file_list:
        # Move image
        shutil.copy(os.path.join(images_dir, img_file), os.path.join(target_img_dir, img_file))
        
        # Move corresponding label (same name but .txt)
        label_file = os.path.splitext(img_file)[0] + ".txt"
        if os.path.exists(os.path.join(labels_dir, label_file)):
            shutil.copy(os.path.join(labels_dir, label_file), os.path.join(target_lbl_dir, label_file))

# Move train and val sets
move_files(train_files, train_images, train_labels)
move_files(val_files, val_images, val_labels)

print(f"✅ Split complete: {len(train_files)} train, {len(val_files)} val")
