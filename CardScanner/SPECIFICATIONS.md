# MTG Card Scanner - Technical Documentation

## 📋 Project Overview

The **MTG Card Scanner** is an open-source multi-mode detection system designed for scanning and detecting Magic: The Gathering (MTG) cards using computer vision techniques.

---

## 🏗️ Architecture Overview

### File Structure
```
projects/MTG-Tools/CardScanner/
├── __init__.py              # Package initialization
## 📐 Component Specifications

### 1. Camera Module (`camera.py`)

**Purpose:** Abstraction layer for camera capture operations.

**Current Implementation:**
- Placeholder implementation that simulates camera capture with a 0.5s delay
- Returns `Tuple[bool, Optional[PILImage]]` where:
  - `True` = success
  - `None` = no actual frame captured yet

**Key Functions:**
```python
def capture_frame_from_camera() -> Tuple[bool, Optional[PILImage]]:
    """Capture a frame from camera (placeholder)"""

def setup_camera(resolution: str = "auto"):
    """Setup camera with specified resolution"""
```

**TODO Items:**
- [ ] Implement actual USB/webcam capture using `cv2.VideoCapture`
- [ ] Add support for multiple camera resolutions
- [ ] Handle camera initialization/failure gracefully

---

### 2. Detection Module (`detection.py`)

**Purpose:** Card detection and analysis logic.

**Data Structures:**

```python
@dataclass
class DetectionResult:
    name: str = ""                    # Detected card name
    confidence: float = 0.0           # Confidence score (0-1)
    image_processed: Optional[PILImage] = None
    frame_timestamp: float = 0
    
    @property
    def is_valid(self) -> bool:
        return self.name != "" and self.confidence > 0
```

**Key Functions:**

#### `fuzzy_match_card_name(detected_text, target_cards)`
- Uses `difflib.SequenceMatcher` for fuzzy string matching
- Returns card name if similarity > 85% threshold
- Enables detection even with OCR errors/typos

#### `detect_card_in_frame(frame) -> DetectionResult | None`
- **Current:** Placeholder returning `None`
- **TODO:** Implement full pipeline:
  1. Extract contours from image
  2. Analyze contour shapes/positions
  3. Apply OCR on detected regions
  4. Match against MTG card database
  5. Return `DetectionResult` with confidence score

#### `analyze_contours(image) -> list`
- Uses OpenCV for edge detection and contour extraction
- Filters contours by area (>10,000 pixels) to find potential cards

---

### 3. Scanner Module (`scanner.py`)

**Purpose:** Core application logic and state management.

**Main Class: `VisionApp`**

| Attribute | Type | Description |
|-----------|------|-------------|
| `config_path` | str | Path to JSON config file (default: "scanner_settings.json") |
| `settings` | dict | Loaded configuration settings |
| `captured_images` | Dict[str, List[PILImage]] | Maps card names to captured frames |
| `detection_results` | Dict[str, DetectionResult] | Last detection for each card |
| `camera_streaming` | bool | Flag for streaming mode |
| `current_frame` | PILImage | Latest captured frame |
| `db_connection` | Any | Database connection (TODO) |

**Key Methods:**

#### Resolution Handling
```python
def get_resolution(self) -> tuple:
    # Returns (1280, 720) by default or parses "WxH" format from settings
```

#### Frame Capture & Detection
```python
async def capture_and_detect_one_image(self, expected_card_name: str) -> Optional[DetectionResult]:
    """Single capture attempt with detection"""
    # TODO: Implement actual capture and detection logic
```

#### Continuous Capture Mode
```python
async def run_continuous_capture(self, card_names: List[str]) -> Dict:
    """Multi-iteration capture for statistical analysis"""
    # Runs 5 iterations per card, aggregates results
    # Returns dict with raw results, best results, and accuracy
```


## 📊 Expected Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Capture latency | < 50ms | USB webcam |
| Detection accuracy | > 90% | With proper lighting/angle |
| Batch processing | ~1s/card | For 5-iteration mode |
| Memory usage | < 200MB | For standard laptop RAM |

---

## 🔮 Future Implementation Roadmap

### Phase 1: Camera Integration
- [ ] Replace placeholder with real `cv2.VideoCapture`
- [ ] Add USB webcam support
- [ ] Handle camera permissions on Windows/Linux

### Phase 2: Detection Pipeline
- [ ] Implement edge detection → contour finding
- [ ] Add template matching or YOLO/SSD model for cards
- [ ] Integrate Tesseract OCR for text recognition
- [ ] Build MTG card metadata database lookup

### Phase 3: Advanced Features
- [ ] Multi-card detection per frame
- [ ] Card condition assessment (damage/stickers)
- [ ] Real-time streaming mode
- [ ] Background subtraction for stationary scanner

### Phase 4: Database Integration
- [ ] Connect to existing `DatabaseCreator` schema
- [ ] Store detections with timestamps
- [ ] Export collections as CSV/JSON

---

## 📝 Configuration File Schema (`scanner_settings.json`)

```json
{
    "capture_resolution": "1280x720",  // Or "auto" for defaults
    "camera_device_id": 0,              // USB webcam index
    "detection_threshold": 0.75,        // Min confidence to accept detection
    "ocr_engine": "tesseract",          // OCR library choice
    "db_url": "sqlite:///cards.db"      // Database connection string
}
```

---

## 🛡️ Error Handling Strategy

1. **Camera Failures** - Try-catch around capture, fallback to None
2. **Detection Failures** - Continue processing, log warnings
3. **File I/O Errors** - Catch `FileNotFoundError`, provide defaults
4. **KeyboardInterrupt** - Graceful shutdown with cleanup

---

## 📦 Installation Requirements

```bash
pip install Pillow numpy opencv-python pytesseract
```

Optional (database):
- SQLite3 built-in
- Or PostgreSQL/MySQL via `psycopg2`/`mysqlclient`

---

## 🔧 Development Notes

### Current State (as of 9/10/2026)
- ✅ Basic project structure in place
- ✅ Data classes and interfaces defined
- ⏳ Placeholder implementations for core functions
- ⏳ Camera capture returns simulated results
- ⏳ Detection returns `None` (not yet implemented)

### Known Issues
- Camera module doesn't capture real frames yet
- Detection logic needs full pipeline implementation
- Database connection not initialized

### Testing Strategy
- Unit tests for fuzzy matching accuracy
- Integration tests for camera ↔ detection pipeline
- Performance benchmarks for batch processing

---

*Last updated: October 9, 2026*
#### Accuracy Calculation
```python
def calculate_accuracy(self, test_cards: List[str]) -> float:
    """Calculate percentage of correctly detected cards"""
```

#### Settings Persistence
```python
def save_settings(self) -> bool:
    # Saves current settings to JSON config file
```

#### Utility Methods
- `auto_tune_parameters()` - Placeholder for auto-calibration
- `show_tuning_mode()` - Debug interface with parameter sliders (placeholder)
- `load_sample_card_list()` - Returns sample MTG cards list
- `export_collection()` - Exports captured images as CSV-compatible format

---

### 4. Main Entry Point (`main.py`)

**Purpose:** CLI interface and user interaction layer.

**Entry Function: `main()`**
```python
async def main():
    # Creates VisionApp instance
    # Prints welcome banner
    # Presents mode selection menu:
    #   1 - Scan Mode (single capture per card)
    #   2 - Tuning Mode (debug interface)
    #   3 - Auto-Tune Mode (continuous capture)
    # Handles KeyboardInterrupt gracefully
    # Offers to save settings on exit
```

---

## 🎯 Design Patterns Used

1. **Singleton-like Pattern** - `VisionApp` maintains state across operations
2. **Strategy Pattern** - Different modes (scan, tune, auto-tune) as strategies
3. **Data Class** - `DetectionResult` for immutable detection outputs
4. **Async/Await** - Non-blocking I/O for camera captures

├── camera.py                # Camera abstraction layer
├── detection.py             # Card detection logic
├── scanner.py               # Core VisionApp class & main logic
└── main.py                  # Entry point with CLI interface
```

### External Dependencies
- `projects/DatabaseCreator/database.py` - Database connection (TODO)
- `PIL` / `Pillow` - Image processing
- `numpy` - Numerical operations
- `opencv-python` (cv2) - Contour analysis
