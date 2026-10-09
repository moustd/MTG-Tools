# MTG Card Scanner - Implementation Plan

## 🎯 Goals & Objectives

### Primary Goal
Build a functional MTG card detection system that can:
1. Capture frames from USB webcam/camera
2. Detect and identify Magic: The Gathering cards
3. Aggregate results across multiple captures
4. Calculate accuracy metrics for performance evaluation

---

## 📋 Implementation Phases

### Phase 1: Foundation (Current State → Next Steps)

#### Tasks
- [x] Create project directory structure
- [ ] Implement real camera capture (`camera.py`)
- [ ] Replace detection placeholder with actual pipeline (`detection.py`)
- [ ] Wire up `VisionApp` methods to camera/detection modules
- [ ] Add sample card list and basic CLI

#### Deliverables
- Working scanner that captures frames from USB webcam
- Detection returns at least one valid `DetectionResult` or None
- CLI shows mode selection menu with 3 options

**Estimated Time:** 2-4 hours (depending on camera hardware)

---

### Phase 2: Core Detection Pipeline

#### Tasks
1. **Contour Analysis**
   - Convert frames to grayscale
   - Apply thresholding and Canny edge detection
   - Extract contours, filter by area (>10k pixels)
   - Sort by largest first (likely card region)

2. **Region Extraction**
   - Crop ROI around detected contour
   - Apply perspective transform for better view normalization

3. **OCR Integration**
   - Install Tesseract OCR (`pip install pytesseract`)
   - Extract text from cropped region
   - Use fuzzy matching to find best card match

4. **Card Database Lookup**
   - Create SQLite database with MTG cards (or import existing)
   - Structure: `id`, `name`, `cost`, `rarity`, `powers`, etc.
   - Query for matches, return best result + confidence

#### Subtasks & Dependencies
- [ ] Create card database schema (`database.py`)
- [ ] Populate initial MTG cards (or fetch from API)
- [ ] Implement contour extraction function
- [ ] Integrate Tesseract OCR
- [ ] Build fuzzy matching wrapper

### Phase 3: Performance Optimization

#### Tasks
- [ ] Profile capture latency, identify bottlenecks
- [ ] Optimize image processing (resize before detection)
- [ ] Add early-exit if no contours found
- [ ] Batch-process multiple cards in parallel

#### Deliverables
- < 50ms per capture frame
- > 90% accuracy on known cards under good lighting

**Estimated Time:** 2-3 hours

---

### Phase 4: Advanced Features (Future Work)

- Multi-card detection per frame
- Condition assessment (stamps, damage)
- Real-time mode with video stream
- Export to CSV/JSON

---

## 🧪 Testing Strategy

### Unit Tests
```python
def test_fuzzy_matching():
    # Verify similarity threshold works correctly
    assert fuzzy_match_card_name("Blast of Selves", ["Blade of Selves"]) == "Blade of Selves"
```

### Integration Tests
```python
async def test_capture_detection_loop():
    result = await app.capture_and_detect_one_image("Test Card")
    assert result is None or result.is_valid  # Placeholder until detection works
```

### Performance Benchmarks
- Capture time: < 100ms (5 frames/sec)
- Detection time: < 2s for one card
- Memory footprint: < 200MB during batch processing

---

## 🔧 Development Workflow

### Daily Cycle
1. Write code for next feature
2. Test with USB webcam locally
3. Document issues/errors in `ARCHITECTURE.md`
4. Commit to repo with descriptive message

### Issue Tracking (Manual)
| Issue | Status | Notes |
|-------|--------|-------|
| Camera not capturing frames | 🔴 To Do | Need to implement `cv2.VideoCapture` |
| Detection returns None | 🟡 Planned | Contour → OCR pipeline pending |
| Database connection needed | 🟡 Pending | Create schema in Phase 2 |

---

## 📦 External Dependencies Plan

### Phase 1 Requirements (Minimal)
```bash
pip install Pillow numpy opencv-python
```

### Phase 2 Additions
- `pytesseract` + system Tesseract OCR binary
- Optional: `opencv-contrib-python` for additional modules
- Consider: `pandas` for data export

### Database Backend
- Start with SQLite (built-in)
- Upgrade to PostgreSQL/MySQL if needed
- Use existing `projects/DatabaseCreator/database.py` once it exists

---

## 🚦 Milestones & Success Criteria

### Milestone 1 (Day 1): Camera Working
- ✅ USB webcam captures frames into PIL Image
- ✅ Frames visible or saved to disk for inspection
- **Blocker Removed:** Can proceed with detection pipeline

### Milestone 2 (Day 2): Contour Extraction
- ✅ Detect rectangular shapes in image
- ✅ Filter and sort by area
- ✅ Extract ROI correctly

### Milestone 3 (Day 2-3): OCR & Matching
- ✅ Tesseract reads card text
- ✅ Fuzzy matching finds best match from DB
- ✅ Returns valid `DetectionResult`

### Milestone 4 (Day 3): Full Pipeline
- ✅ End-to-end: capture → process → match → store
- ✅ CLI shows results, accuracy metrics
- ✅ All modes functional (scan, tune, auto-tune)

---

## 📝 Documentation Updates Plan

As implementation progresses:
1. Update `SPECIFICATIONS.md` with completed features
2. Add new diagrams to `ARCHITECTURE.md` for advanced patterns
3. Create `README.md` summarizing usage once functional
4. Generate API docs from type hints (optional, using Sphinx)

---

## 🤝 Collaboration Guidelines

### Code Style
- Use existing type hints from current files
- Follow PEP 8 (4-space indent, max 79 chars line)
- Docstrings for all public methods (Sphinx-ready)

### Testing Commitment
- Write tests before new features if time permits
- At least one manual test with physical cards each day

### Version Control
- Commits: Feature-focused, descriptive messages
- Branches: `feature/camera-integration`, `feature/ocr-pipeline`
- PRs: Include screenshots of results when possible

---

## 🎓 Resources & References

### Card Detection Research
- "Real-Time Object Detection with YOLO" for template-free approaches
- Tesseract OCR documentation: https://github.com/tesseract-ocr/tesseract
- OpenCV contour tutorials

### MTG API Alternatives
- MyAbler (public API) for card metadata
- Scryfall (REST API) as fallback

---

*Plan Version: 1.0 | Last Updated: October 9, 2026*

**Estimated Time:** 4-8 hours