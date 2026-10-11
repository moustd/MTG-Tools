# Dataset Manager (dataset_manager.py)

This module manages MTG card datasets with collection support.

## Key Features

- **Collection Handling**: Supports multiple cards (not single-card)
- **JSON Persistence**: Saves dataset to JSON files
- **Image Management**: Handles image storage and paths

## Core Classes

### `CardImage`
Represents a single card image with:
- `image_path`: Absolute path to the image
- `official_name`: Card name (used for organization)
- `is_saved`: Boolean flag for image status

## Key Functions

- `sanitize_filename(name: str) -> str`:  
  Creates safe filenames from card names (removes special characters).

- `save_dataset(dataset: Dict[str, List[Dict]], output_path: str)`:  
  Saves dataset to JSON (supports multiple cards).

- `load_dataset(json_path: str) -> Optional[Dict]`:  
  Loads dataset from JSON file.

- `get_dataset_metadata(json_path: str) -> Optional[Dict]`:  
  Provides metadata about the dataset (cards, total images).

- `create_image_id_sequence(official_name: str, count: int)`:  
  Generates image filenames for a card (e.g., `Azorius_Spirit_01.jpg`).

## Architecture Notes
- Uses JSON for dataset storage (allows easy sharing and versioning)
- Separates image handling from dataset logic
- Designed for collection workflows (multiple cards)