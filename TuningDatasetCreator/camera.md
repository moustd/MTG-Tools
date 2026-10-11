# Webcam Capture Module (camera.py)

This module handles webcam integration for capturing MTG card images.

## Key Functions

- `get_webcam(device_id: int = 0) -> Optional[VideoCapture]`:  
  Initializes a webcam device with default settings (1280x720 resolution, 30 FPS).

- `capture_frame(cap: VideoCapture) -> Tuple[bool, Optional[Mat]]`:  
  Captures a single frame from the webcam.

- `show_webcam(cap: VideoCapture) -> Optional[Mat]`:  
  Displays the webcam feed in a window for manual capture.

- `release_camera(cap: Optional[VideoCapture])`:  
  Releases camera resources to prevent leaks.

## Configuration
- Default camera index: `0` (default webcam)
- Frame resolution: `1280x720`
- Frame rate: `30 FPS`