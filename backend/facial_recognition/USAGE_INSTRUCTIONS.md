# Face Recognition System Usage Instructions

This document provides instructions for using the face recognition system.

## Overview

The system consists of two main components:

1. **Database Building** (`build_database.py`) - Creates a database of face embeddings from images
2. **Real-time Recognition** (`test_recognizer.py`) - Performs real-time face recognition using a webcam

## Quick Start

For a complete workflow that guides you through both steps, you can use:

```bash
python example_workflow.py
```

This will:
1. Check if you have person folders with face images
2. Build a face database from these images
3. Run real-time recognition using your webcam

## Step 1: Prepare Your Data

Organize your face images in a directory structure:

```
face_images/
  person1/
    image1.jpg
    image2.jpg
    ...
  person2/
    image1.jpg
    image2.jpg
    ...
```

Guidelines:
- Use 3-5 clear face images per person
- Images should show the face clearly with good lighting
- Use different angles/expressions for better recognition

## Step 2: Build Your Database

Use the `build_database.py` script to create your face recognition database:

```bash
python build_database.py --input_dir face_images --output_db face_database.json
```

Options:
- `--input_dir`: Directory containing person folders with face images
- `--output_db`: Output database path (default: face_database.json)
- `--max_images`: Maximum number of images per person (default: 5)
- `--min_face_size`: Minimum face size to include (default: 80 pixels)
- `--confidence`: Face detection confidence threshold (default: 0.5)
- `--augment`: Apply data augmentation to increase sample diversity

Example with all options:

```bash
python build_database.py \
  --input_dir face_images \
  --output_db my_database.json \
  --max_images 5 \
  --min_face_size 100 \
  --confidence 0.6 \
  --augment
```

## Step 3: Run Real-time Recognition

Use the `test_recognizer.py` script to run real-time face recognition:

```bash
python test_recognizer.py --database face_database.json
```

Options:
- `--database`: Path to your face database JSON file
- `--camera`: Camera index (default: 0)
- `--width`: Camera width (default: 640)
- `--height`: Camera height (default: 480)
- `--confidence`: Face detection confidence threshold (default: 0.5)
- `--threshold`: Face recognition similarity threshold (default: 0.5)
- `--display_scale`: Display scaling factor (default: 1.0)

Example with all options:

```bash
python test_recognizer.py \
  --database my_database.json \
  --camera 0 \
  --width 1280 \
  --height 720 \
  --confidence 0.6 \
  --threshold 0.5 \
  --display_scale 0.75
```

## Tips for Best Results

1. **Use good lighting**: Face recognition works best with well-lit faces
2. **Collect diverse images**: Include different angles and expressions for each person
3. **Adjust thresholds**: 
   - Higher confidence threshold (e.g., 0.7) = fewer but more accurate face detections
   - Lower recognition threshold (e.g., 0.4) = stricter matching, fewer false positives
   - Higher recognition threshold (e.g., 0.6) = more lenient matching, fewer unknowns
4. **Use data augmentation**: Enable the `--augment` option to improve recognition robustness
5. **Keep database updated**: Regularly add new images to improve recognition accuracy

## Troubleshooting

1. **No faces detected**: 
   - Check lighting conditions
   - Make sure face is clearly visible
   - Try lowering the detection confidence threshold

2. **Incorrect recognition**:
   - Add more diverse images to the database
   - Try adjusting the recognition threshold
   - Make sure the face is well-lit and clearly visible

3. **Performance issues**:
   - Reduce camera resolution (--width and --height)
   - Use display scaling to show a smaller preview (--display_scale)

## Technical Details

- **Face Detection**: Uses YOLOv8 for efficient face detection
- **Face Recognition**: Uses FaceNet embeddings with cosine similarity matching
- **Database Format**: JSON file with person IDs, names, and face embeddings 