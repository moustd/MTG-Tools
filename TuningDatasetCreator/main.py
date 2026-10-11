from camera import get_webcam, capture_frame
from dataset_manager import (load_dataset, save_dataset, sanitize_filename, CardImage)


import os
import json

def main():
    print("\nMTG Card Dataset Builder (Multi-Card Support)")
    print("Type 'exit' to quit at any time")
    
    # Configuration
    DATASET_PATH = "C:/Users/dionmoustos/VSCode Workspace/projects/MTG-Tools/dataset.json"
    DATASET_DIR = os.path.dirname(DATASET_PATH)
    
    # Initialize dataset
    dataset = {}
    
    # Check if existing dataset exists
    if os.path.exists(DATASET_PATH):
        print(f"\n✅ Loaded existing dataset from: {DATASET_PATH}")
        dataset = load_dataset(DATASET_PATH)
    else:
        print("\n⚠️ Starting new dataset (no existing data)")
    
    # Main interaction loop
    while True:
        user_input = input("Enter card name (or 'exit' to quit): ").strip()
        
        if user_input.lower() == "exit":
            break
        
        # Process card
        card_name = sanitize_filename(user_input)
        cap = get_webcam()
        if not cap:
            print("Error: Camera not available")
            continue
        
        ret, frame = capture_frame(cap)
        if not ret:
            print("Error: Failed to capture image")
            cap.release()
            continue
        
        # Save image (simplified for demo)
        image_path = os.path.join(DATASET_DIR, f"{card_name}_01.jpg")
        try:
            with open(image_path, "wb") as f:
                f.write(frame)  # In real use: convert to JPEG
            print(f"✅ Saved image: {image_path}")
        except Exception as e:
            print(f"Error saving image: {e}")
            cap.release()
            continue
        
        # Add to dataset
        if card_name not in dataset:
            dataset[card_name] = []
        
        # Create CardImage object
        card_image = CardImage(image_path, card_name)
        dataset[card_name].append(card_image.to_dict())
    
    # Save updated dataset
    save_dataset(dataset, DATASET_PATH)
    print(f"\n✅ Dataset saved to: {DATASET_PATH}")
    print(f"Total cards: {len(dataset)} | Total images: {sum(len(v) for v in dataset.values())}")

if __name__ == "__main__":
    main()