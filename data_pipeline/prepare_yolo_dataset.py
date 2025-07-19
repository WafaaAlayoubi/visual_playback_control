import os
import random
import shutil
from pathlib import Path

# --- CONFIGURE YOUR PATHS AND CLASSES HERE ---

# Path to the folder where you have all your annotated images and .txt files
SOURCE_FOLDER = "../dataset/source_images" 

# Path to the new folder where the final YOLO dataset will be created
OUTPUT_FOLDER = "../dataset/yolo_format"

# The names of your classes, IN THE ORDER YOU WANT THEM TO BE NUMBERED (0, 1, 2, ...)
# This order MUST match the `classes.txt` file if you used one in LabelImg.
CLASS_NAMES = [
    "headphones_on",
    "headphones_off"
]

# Define the split ratios
# 80% for training, 10% for validation, 10% for testing
TRAIN_RATIO = 0.8
VAL_RATIO = 0.1
TEST_RATIO = 0.1
# --- END OF CONFIGURATION ---


def split_data(source_folder, output_folder):
    """
    Splits data from a single folder into a YOLO-compatible train/val/test structure.
    """
    print("Starting dataset split...")

    # --- 1. Input Validation ---
    if abs(TRAIN_RATIO + VAL_RATIO + TEST_RATIO - 1.0) > 1e-8:
        print("Error: Ratios must sum to 1.")
        return

    source_path = Path(source_folder)
    if not source_path.is_dir():
        print(f"Error: Source folder not found at '{source_folder}'")
        return

    # --- 2. Create Output Directories ---
    output_path = Path(output_folder)
    print(f"Creating directory structure at '{output_path}'")
    for subset in ['train', 'val', 'test']:
        (output_path / 'images' / subset).mkdir(parents=True, exist_ok=True)
        (output_path / 'labels' / subset).mkdir(parents=True, exist_ok=True)

    # --- 3. Get all image files and shuffle them ---
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_files = [p for p in source_path.iterdir() if p.suffix.lower() in image_extensions]
    
    if not image_files:
        print("Error: No image files found in the source folder.")
        return
        
    random.shuffle(image_files)
    total_files = len(image_files)
    print(f"Found {total_files} images to process.")

    # --- 4. Calculate split points ---
    train_end = int(total_files * TRAIN_RATIO)
    val_end = train_end + int(total_files * VAL_RATIO)

    splits = {
        'train': image_files[:train_end],
        'val': image_files[train_end:val_end],
        'test': image_files[val_end:]
    }

    # --- 5. Move the files ---
    for subset, files in splits.items():
        print(f"\nProcessing {len(files)} files for the '{subset}' set...")
        for img_path in files:
            label_path = img_path.with_suffix('.txt')
            
            if label_path.exists():
                # Define destination paths
                dest_img_path = output_path / 'images' / subset / img_path.name
                dest_label_path = output_path / 'labels' / subset / label_path.name
                
                # Use shutil.move to move files. Use shutil.copy to copy instead.
                shutil.move(str(img_path), str(dest_img_path))
                shutil.move(str(label_path), str(dest_label_path))
            else:
                print(f"  [Warning] Label file not found for '{img_path.name}'. Skipping this image.")

    # --- 6. Create the dataset.yaml file ---
    yaml_content = f"""
# Path to the root directory of the dataset
path: {output_path.resolve()}

# Train, validation, and test sets
train: images/train
val: images/val
test: images/test

# Number of classes
nc: {len(CLASS_NAMES)}

# Class names
names: {CLASS_NAMES}
"""
    yaml_file_path = output_path / 'dataset.yaml'
    print(f"\nCreating dataset configuration file at '{yaml_file_path}'")
    with open(yaml_file_path, 'w') as f:
        f.write(yaml_content)

    print("\n--------------------")
    print("Dataset splitting complete!")
    print("--------------------")

if __name__ == '__main__':
    split_data(SOURCE_FOLDER, OUTPUT_FOLDER)