"""Webcam capture integration for MTG card dataset tool."""

import cv2
from typing import Optional, Tuple
import time


def get_webcam(device_id: int = 0) -> Optional["cv2.VideoCapture"]:
    """Get a webcam VideoCapture object.
    
    Args:
        device_id: Camera index (0 for default webcam).
        
    Returns:
        VideoCapture object or None if camera not found.
    """
    cap = cv2.VideoCapture(device_id)
    if not cap.isOpened():
        print(f"Error: Cannot open camera device {device_id}")
        return None
    
    # Set optimal properties for card scanning
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    return cap


def capture_frame(cap: "cv2.VideoCapture") -> Tuple[bool, Optional["cv2.Mat"]]:
    """Capture a single frame from the webcam.
    
    Args:
        cap: OpenCV VideoCapture object.
        
    Returns:
        Tuple of (success, frame) where frame is None if capture failed.
    """
    ret, frame = cap.read()
    return ret, frame


def show_webcam(cap: "cv2.VideoCapture") -> Optional["cv2.Mat"]:
    """Display webcam feed in a window and allow manual capture.
    
    Args:
        cap: OpenCV VideoCapture object.
        
    Returns:
        The captured frame if successful, None otherwise.
    """
    ret, frame = capture_frame(cap)
    return frame


def release_camera(cap: Optional["cv2.VideoCapture"]) -> None:
    """Release webcam resources."""
    if cap is not None:
        cap.release()