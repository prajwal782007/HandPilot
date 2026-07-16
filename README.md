# HandPilot

HandPilot is a computer vision application that allows users to control their computer using hand gestures.

## Milestone 1: Tracking Foundation
Currently, HandPilot is in Milestone 1. This milestone focuses entirely on providing a robust, modular, and performant hand-tracking foundation using OpenCV and MediaPipe. OS-level controllers and UI overlays are deliberately disabled to focus on the stability of the vision pipeline.

### Features
- Native OpenCV window showing webcam feed
- 21-point hand landmark extraction
- Computed stable palm center tracking
- Real-time FPS counter
- Robust error handling and camera management

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To run the Milestone 1 tracking foundation:
```bash
python src/main.py
```
Press `q` in the OpenCV window to exit the application.
