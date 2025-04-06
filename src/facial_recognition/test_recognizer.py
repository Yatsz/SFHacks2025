"""
Real-time face recognition system.

This script performs real-time face detection and recognition using a webcam.
It uses the FaceDetector and FaceRecognizer classes to detect and recognize faces
against a database of known faces.

Usage:
  python test_recognizer.py --database face_database.json
"""

import os
import cv2
import numpy as np
import json
import argparse
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple

from face_detector import FaceDetector
from face_recognizer import FaceRecognizer

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Real-time face recognition")
    parser.add_argument("--database", type=str, default="face_database.json",
                        help="Path to face database JSON file")
    parser.add_argument("--camera", type=int, default=0,
                        help="Camera index (default: 0)")
    parser.add_argument("--width", type=int, default=640,
                        help="Camera width")
    parser.add_argument("--height", type=int, default=480,
                        help="Camera height")
    parser.add_argument("--confidence", type=float, default=0.5,
                        help="Face detection confidence threshold")
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="Face recognition similarity threshold")
    parser.add_argument("--display_scale", type=float, default=1.0,
                        help="Display scaling factor")
    return parser.parse_args()

def load_database(database_path: str) -> Dict[str, Dict[str, Any]]:
    """Load face recognition database from JSON file"""
    if not os.path.exists(database_path):
        print(f"Error: Database file {database_path} not found")
        return {}
    
    try:
        with open(database_path, 'r') as f:
            database = json.load(f)
        
        print(f"Loaded database with {len(database)} persons:")
        for person_id, person_data in database.items():
            embeddings_count = len(person_data.get("embeddings", []))
            name = person_data.get("name", person_id)
            print(f"  - {name}: {embeddings_count} embeddings")
        
        return database
    except Exception as e:
        print(f"Error loading database: {e}")
        return {}

def draw_detection(
    image: np.ndarray,
    bbox: Tuple[int, int, int, int],
    person_id: str,
    name: str,
    similarity: float,
    threshold: float
) -> np.ndarray:
    """
    Draw detection results on the image.
    
    Args:
        image: Input image
        bbox: Bounding box coordinates (x1, y1, x2, y2)
        person_id: Recognized person ID
        name: Person's name
        similarity: Recognition similarity score
        threshold: Recognition threshold
        
    Returns:
        Image with detection visualization
    """
    x1, y1, x2, y2 = bbox
    
    # Determine color based on recognition result
    if person_id == "unknown":
        # Red for unknown
        color = (0, 0, 255)
        text_color = (255, 255, 255)
    else:
        # Green gradient based on similarity
        green = min(255, int(255 * similarity / threshold))
        red = max(0, min(255, int(255 * (1 - similarity / (threshold * 2)))))
        color = (0, green, red)
        text_color = (255, 255, 255)
    
    # Draw bounding box
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    
    # Prepare text
    if person_id == "unknown":
        display_text = "Unknown"
    else:
        display_text = f"{name} ({similarity:.2f})"
    
    # Draw a background rectangle for text
    text_size, baseline = cv2.getTextSize(display_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    cv2.rectangle(image, (x1, y1 - text_size[1] - 10), (x1 + text_size[0], y1), color, -1)
    
    # Draw text
    cv2.putText(image, display_text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
    
    return image

def run_recognition(args):
    """Run real-time face recognition"""
    # Load database
    database = load_database(args.database)
    if not database:
        print("No database loaded. Recognition will always return 'unknown'.")
    
    # Initialize detector and recognizer
    print("Initializing face detector...")
    detector = FaceDetector(confidence=args.confidence)
    
    print("Initializing face recognizer...")
    recognizer = FaceRecognizer(
        recognition_threshold=args.threshold,
        enforce_detection=False
    )
    
    # Open webcam
    print(f"Opening camera {args.camera}...")
    cap = cv2.VideoCapture(args.camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # FPS calculation variables
    fps_counter = 0
    fps_start_time = time.time()
    fps = 0
    
    print("Starting real-time recognition. Press 'q' to quit.")
    
    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from webcam")
            break
        
        # Update FPS calculation
        fps_counter += 1
        current_time = time.time()
        if current_time - fps_start_time >= 1.0:
            fps = fps_counter / (current_time - fps_start_time)
            fps_counter = 0
            fps_start_time = current_time
        
        # Detect faces
        start_time = time.time()
        faces, metadata = detector.detect_faces(frame)
        detection_time = time.time() - start_time
        
        # Process each detected face
        for i, (face, meta) in enumerate(zip(faces, metadata)):
            # Get bounding box
            x1, y1, x2, y2 = meta["bbox"]
            
            # Recognize face
            start_time = time.time()
            person_id, similarity, person_data = recognizer.recognize_face_image(face, database)
            recognition_time = time.time() - start_time
            
            # Get person name
            if person_id == "unknown":
                name = "Unknown"
            else:
                name = person_data.get("name", person_id)
            
            # Draw results
            frame = draw_detection(
                frame, 
                (x1, y1, x2, y2), 
                person_id, 
                name, 
                similarity, 
                args.threshold
            )
        
        # Add performance metrics
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Add instructions
        cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Scale the display if needed
        if args.display_scale != 1.0:
            display_size = (int(frame.shape[1] * args.display_scale), int(frame.shape[0] * args.display_scale))
            display_frame = cv2.resize(frame, display_size)
        else:
            display_frame = frame
        
        # Display the frame
        cv2.imshow("Face Recognition", display_frame)
        
        # Check for user input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    print("Recognition stopped")

def main():
    """Main function"""
    args = parse_args()
    run_recognition(args)

if __name__ == "__main__":
    main() 