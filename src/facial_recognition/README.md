# Facial Recognition Module for Alzheimer's Patient Assistant

This module provides real-time face detection and recognition capabilities for the Alzheimer's Patient Assistant using the TurtleBot4 and OM1 platform.

## Features

- **Face Detection**: Uses YOLOv8 for efficient real-time face detection
- **Face Recognition**: Uses FaceNet or ArcFace for embedding generation and recognition
- **Person Database**: Stores known persons with multiple face embeddings and personal information
- **Image Augmentation**: Applies image transformations to increase recognition robustness
- **Robot Integration**: Integrates with the TurtleBot4 platform for real-world operation

## Components

- `face_detector.py`: Face detection using YOLOv8
- `face_recognizer.py`: Face recognition using DeepFace/FaceNet
- `database.py`: Person database management
- `utils.py`: Utility functions for image processing and augmentation
- `demo.py`: Demonstration script for testing facial recognition
- `robot_integration.py`: Integration with the TurtleBot4 platform
- `setup.py`: Setup script to prepare directories and download models

## Custom Model Support

The face detector is designed to work with a local face detection model:

1. Place your custom YOLOv8 model file named `model.pt` in the `src/facial_recognition/` directory.
2. The system will automatically detect and use this local model instead of downloading a default one.
3. This is useful when you have a specialized face detection model trained for your specific use case.

If no local model is found, the system will fall back to downloading and using the default YOLOv8 face detection model.

## Setup

Before using the facial recognition module, run the setup script to create necessary directories and check for required models:

```bash
# Basic setup
python -m src.facial_recognition.setup

# Skip model download (if you have already downloaded the models or are using a custom model)
python -m src.facial_recognition.setup --no-download

# Force download of default models (overwrites any local model.pt)
python -m src.facial_recognition.setup --force-download
```

The setup script creates the following directories:
- `data/`: For storing the JSON database of persons
- `images/persons/`: For storing the face images of registered persons

It will also check for the local model.pt file and download default models if needed.

## Usage

### Demo Mode

The module includes a demo script for testing facial recognition functionality:

```bash
# Register a new person
python -m src.facial_recognition.demo --mode register --name "John Doe" --relation "Grandson" --notes "Likes to play chess together on Sundays"

# Run recognition
python -m src.facial_recognition.demo --mode recognize
```

### Integration with TurtleBot4

To integrate facial recognition with the TurtleBot4 system:

```python
from src.facial_recognition.robot_integration import FacialRecognitionService

# Create a callback for speech output
def speak_message(message):
    print(f"Speaking: {message}")
    # Add integration with TTS system here

# Initialize the facial recognition service
facial_recognition = FacialRecognitionService(
    database_path="data/person_database.json",
    speaker_callback=speak_message
)

# Start the service
facial_recognition.start(camera_id=0)

# The service runs in a background thread
# When done:
facial_recognition.stop()
```

## Database Structure

The person database uses a JSON format:

```json
{
  "person_id": {
    "id": "person_id",
    "name": "Person Name",
    "relation": "Relationship to Patient",
    "notes": "Additional information (favorite shared activities, etc.)",
    "created": "2023-04-05T12:00:00Z",
    "updated": "2023-04-05T12:30:00Z",
    "embeddings": [
      [...], // Embedding vector 1
      [...], // Embedding vector 2
      ...
    ],
    "image_paths": [
      "images/persons/person_id/123456789.jpg",
      ...
    ]
  },
  ...
}
```

## Requirements

The following packages are required for the facial recognition system:

- **Python**: >=3.10
- **Core Libraries**:
  - opencv-python>=4.8.0
  - numpy>=1.24.0
  - deepface>=0.0.79
  - ultralytics>=8.0.0 (for YOLOv8)
  - torch>=2.0.0
  - torchvision>=0.15.0
  - tensorflow>=2.12.0
  - scikit-learn>=1.2.0
  - matplotlib
  - scipy

These dependencies are specified in the project's `pyproject.toml` file. You can install them using:

```bash
# Using pip
pip install -r requirements.txt

# Using uv
uv pip install -r requirements.txt
```

## Performance Considerations

- Face detection: ~15-20ms per frame on GPU
- Embedding generation: ~80-120ms per face on CPU
- Recognition: ~2-5ms per query
- Total latency: <100ms for end-to-end recognition

## Future Improvements

- Firebase integration for database storage
- Edge optimization for TurtleBot4 hardware
- Enhanced tracking for consistent person recognition
- Multi-face recognition with priority handling
- TensorRT optimization for faster inference 