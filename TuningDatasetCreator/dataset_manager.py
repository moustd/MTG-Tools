"""Dataset persistence and management for MTG card dataset tool."""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path


def sanitize_filename(name: str) -> str:
    """Create a safe filename from a card name.
    
    Args:
        name: Original card name.
        
    Returns:
        Sanitized string suitable for use as filename.
    """
    # Remove special characters and spaces, replace with underscores
    safe_name = "".join(c if c.isalnum() or c == "-" else "_" for c in name)
    return safe_name.replace(" ", "_")


def save_dataset(dataset: Dict[str, List[Dict]], output_path: str) -> None:
    """Save dataset to JSON file.
    
    Args:
        dataset: Dictionary mapping card names to list of image data (with paths).
        output_path: Path to save the dataset.json file (parent dir must exist).
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)


def load_dataset(json_path: str) -> Optional[Dict[str, List[Dict]]]:
    """Load dataset from JSON file.
    
    Args:
        json_path: Path to dataset.json file.
        
    Returns:
        Dataset dictionary or None if file not found/corrupted.
    """
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def get_dataset_metadata(json_path: str) -> Optional[Dict]:
    """Extract metadata from dataset JSON.
    
    Args:
        json_path: Path to dataset.json file.
        
    Returns:
        Dict with 'cards' list and total image count, or None on error.
    """
    dataset = load_dataset(json_path)
    if not dataset:
        return None
    
    card_list = [
        {"name": card["official_name"], "count": len(card.get("images", []))}
        for card in dataset.values()
    ]
    
    return {
        "cards": card_list,
        "total_images": sum(len(c.get("images", [])) for c in dataset.values()),
        "dataset_count": len(dataset)
    }


class CardImage:
    """Represents a captured image with its status."""
    
    def __init__(self, image_path: str, official_name: str):
        self.image_path = image_path
        self.official_name = official_name
        self.is_saved = False
    
    @classmethod
    def from_image_data(cls, data: Dict, official_name: str) -> "CardImage":
        """Create CardImage from dictionary (loaded from JSON)."""
        image = cls(
            image_path=data["path"],
            official_name=official_name
        )
        if isinstance(data.get("is_saved"), bool):
            image.is_saved = data["is_saved"]
        return image
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "path": self.image_path,
            "official_name": self.official_name,
            "is_saved": self.is_saved
        }


def save_image_to_folder(
    image_bytes: bytes, 
    card_name: str, 
    index: int, 
    output_dir: str
) -> Optional[str]:
    """Save an image to disk and return the path.
    
    Args:
        image_bytes: Raw image bytes (JPEG format).
        card_name: Official MTG card name (used for folder structure).
        index: Image index number (starts at 1).
        output_dir: Parent directory for this dataset.
        
    Returns:
        Relative path string or None on error.
    """
    safe_name = sanitize_filename(card_name)
    image_name = f"{safe_name}_{index:04d}.jpg"
    image_path = os.path.join(output_dir, image_name)
    
    try:
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        return image_path
    except IOError as e:
        print(f"Error saving image {image_name}: {e}")
        return None


def create_image_id_sequence(official_name: str, count: int) -> List[str]:
    """Create a sequence of image filenames for a card.
    
    Args:
        official_name: Official MTG card name.
        count: Number of images to generate names for.
        
    Returns:
        List of image path strings like "Azorius_Spirit_01.jpg".
    """
    safe_name = sanitize_filename(official_name)
    return [f"{safe_name}_{i:04d}.jpg" for i in range(1, count + 1)]


def get_relative_image_paths(
    images_dir: str, 
    image_paths: List[str], 
    base_dataset_path: str
) -> List[str]:
    """Convert absolute paths to relative paths.
    
    Args:
        images_dir: Path to the folder containing images.
        image_paths: List of absolute image paths.
        base_dataset_path: Dataset folder path (for context).
        
    Returns:
        List of relative path strings.
    """
    return [p.replace(base_dataset_path, "") for p in image_paths]


def get_or_create_dataset_directory(root_dir: str, official_name: str) -> Optional[str]:
    """Get existing or create new dataset directory.
    
    Args:
        root_dir: Root directory where datasets are stored.
        official_name: Card name (used for folder name).
        
    Returns:
        Path to the dataset directory or None on error.
    """
    safe_name = sanitize_filename(official_name)
    dataset_path = os.path.join(root_dir, safe_name)
    
    try:
        os.makedirs(dataset_path, exist_ok=True)
        return dataset_path
    except OSError as e:
        print(f"Error creating dataset directory {dataset_path}: {e}")
        return None
