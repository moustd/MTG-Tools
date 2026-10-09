"""Core scanner logic for processing and aggregating detections."""

from typing import List, Dict, Optional
import asyncio
from camera import capture_frame_from_camera
from detection import DetectionResult, detect_card_in_frame


class VisionApp:
    """Main application class for MTG Card Scanner."""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or "scanner_settings.json"
        self.settings = {}
        self.captured_images: Dict[str, List["PILImage"]] = {}
        self.detection_results: Dict[str, DetectionResult] = {}
        self.camera_streaming = False
        self.current_frame = None
        
        try:
            import json
            with open(self.config_path, "r") as f:
                self.settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load settings: {e}")
        
        from DatabaseCreator.database import DATABASE_URL as DB_URL
        self.db_connection = None
    
    def get_resolution(self) -> tuple:
        res_str = self.settings.get('capture_resolution', 'auto')
        if res_str.lower() == 'auto':
            return (1280, 720)
        try:
            height, width = map(int, str(res_str).split('x'))
            return (width, height)
        except ValueError:
            return (1280, 720)

        from camera import capture_frame as real_capture
        success, frame = real_capture()
        
        if success and frame is not None:
            self.current_frame = frame
        
        return success, frame

    async def capture_and_detect_one_image(self, expected_card_name: str) -> Optional[DetectionResult]:
    def capture_frame_from_camera(self) -> tuple: