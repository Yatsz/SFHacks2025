"""
Demo script for facial recognition module.

This script demonstrates the functionality of the facial recognition system
for the Alzheimer's Patient Assistant.
"""

import os
import cv2
import numpy as np
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

from .face_detector import FaceDetector
from .face_recognizer import FaceRecognizer
from .database import PersonDatabase
from .utils import augment_face_image, preprocess_image_for_recognition

def register_person(database: PersonDatabase, 
                   recognizer: FaceRecognizer,
                   detector: FaceDetector,
                   name: str,
                   relation: str, 
                   notes: Optional[str] = None,
                   camera_id: int = 0,
                   num_images: int = 5,
                   num_augmentations: int = 4):
    """
    Register a new person using the webcam.
    
    Args:
        database: Person database
        recognizer: Face recognizer
        detector: Face detector
        name: Person's name
        relation: Relationship to patient
        notes: Additional notes
        camera_id: Camera device ID
        num_images: Number of images to capture
        num_augmentations: Number of augmentations per image
    """
    # Add person to database
    person_id = database.add_person(name, relation, notes)
    
    # Open webcam
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_id}")
        return
    
    print(f"Registering {name} (ID: {person_id})")
    print(f"Will capture {num_images} images. Press SPACE to capture.")
    print("Press ESC to cancel.")
    
    images_captured = 0
    embeddings = []
    
    while images_captured < num_images:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture image")
            break
            
        # Detect faces
        faces, metadata = detector.detect_faces(frame)
        
        # Draw detection on frame
        display_frame = detector.detect_faces_and_draw(frame)
        
        # Show info
        cv2.putText(display_frame, f"Captured: {images_captured}/{num_images}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, "Press SPACE to capture, ESC to cancel", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
        # Display
        cv2.imshow("Register Person", display_frame)
        
        key = cv2.waitKey(1)
        
        # Cancel registration
        if key == 27:  # ESC key
            print("Registration cancelled")
            break
            
        # Capture image
        if key == 32 and faces:  # SPACE key and faces detected
            face_img = faces[0]  # Use the first detected face
            
            # Preprocess the face image
            face_img = preprocess_image_for_recognition(face_img)
            
            # Add original face image to database
            embedding = recognizer.generate_embedding(face_img).tolist()
            database.add_face_image(person_id, face_img, embedding)
            embeddings.append(embedding)
            
            # Create augmented versions
            augmented_faces = augment_face_image(face_img, num_augmentations)
            
            # Add each augmented face
            for aug_face in augmented_faces[1:]:  # Skip the first one (original)
                aug_embedding = recognizer.generate_embedding(aug_face).tolist()
                database.add_face_image(person_id, aug_face, aug_embedding)
                embeddings.append(aug_embedding)
            
            print(f"Captured image {images_captured + 1}/{num_images}")
            images_captured += 1
            
            # Add a small delay to allow user to change pose
            time.sleep(1)
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    
    if images_captured > 0:
        print(f"Successfully registered {name} with {len(embeddings)} face embeddings.")
    else:
        print("Registration failed. No images captured.")
        database.remove_person(person_id)

def run_recognition_demo(database: PersonDatabase,
                        recognizer: FaceRecognizer,
                        detector: FaceDetector,
                        camera_id: int = 0,
                        recognition_interval: float = 1.0):
    """
    Run a live facial recognition demo using webcam.
    
    Args:
        database: Person database
        recognizer: Face recognizer
        detector: Face detector
        camera_id: Camera device ID
        recognition_interval: Time between recognition attempts (seconds)
    """
    # Open webcam
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_id}")
        return
    
    print("Starting face recognition demo")
    print("Press 'q' to quit")
    
    # Get recognition database (with embeddings)
    recognition_db = database.get_database_for_recognition()
    
    # Time of last recognition attempt
    last_recognition_time = 0
    
    # Last recognition results (for display consistency)
    last_results = {}
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture image")
            break
            
        # Detect faces
        faces, metadata = detector.detect_faces(frame)
        
        # Create a copy for display
        display_frame = frame.copy()
        
        # Perform recognition at specified intervals
        current_time = time.time()
        if current_time - last_recognition_time >= recognition_interval and faces:
            last_recognition_time = current_time
            
            # Clear previous results
            last_results = {}
            
            # Process each detected face
            for i, (face_img, face_meta) in enumerate(zip(faces, metadata)):
                # Preprocess the face
                face_img = preprocess_image_for_recognition(face_img)
                
                # Recognize face
                person_id, similarity, person_data = recognizer.recognize_face_image(
                    face_img, recognition_db
                )
                
                # Store result for this face
                bbox = face_meta["bbox"]
                last_results[i] = {
                    "bbox": bbox,
                    "person_id": person_id,
                    "similarity": similarity,
                    "person_data": person_data
                }
        
        # Draw results on display frame
        for face_idx, result in last_results.items():
            bbox = result["bbox"]
            person_id = result["person_id"]
            similarity = result["similarity"]
            person_data = result["person_data"]
            
            # Draw bounding box
            color = (0, 255, 0) if person_id != "unknown" else (0, 0, 255)
            cv2.rectangle(display_frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            
            # Prepare text to display
            if person_id != "unknown":
                name = person_data.get("name", "Unknown")
                relation = person_data.get("relation", "")
                notes = person_data.get("notes", "")
                
                # Draw name and relation
                cv2.putText(display_frame, f"{name} ({relation})", 
                           (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                # Draw confidence
                cv2.putText(display_frame, f"Conf: {similarity:.2f}", 
                           (bbox[0], bbox[3] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                
                # Draw notes if available
                if notes:
                    # Wrap text to fit on screen
                    notes_short = notes[:50] + "..." if len(notes) > 50 else notes
                    cv2.putText(display_frame, f"Notes: {notes_short}", 
                               (10, display_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            else:
                # Draw unknown label
                cv2.putText(display_frame, "Unknown", 
                           (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Display info
        cv2.putText(display_frame, "Face Recognition Demo", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
        # Display the frame
        cv2.imshow("Face Recognition", display_frame)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

def main():
    """Main function for the facial recognition demo."""
    parser = argparse.ArgumentParser(description="Facial Recognition Demo")
    parser.add_argument("--mode", choices=["register", "recognize"], default="recognize",
                      help="Demo mode: register a new person or run recognition")
    parser.add_argument("--name", help="Person's name (for registration)")
    parser.add_argument("--relation", help="Relationship to patient (for registration)")
    parser.add_argument("--notes", help="Additional notes (for registration)")
    parser.add_argument("--camera", type=int, default=0, help="Camera device ID")
    parser.add_argument("--images", type=int, default=5, help="Number of images to capture (for registration)")
    parser.add_argument("--interval", type=float, default=1.0, help="Recognition interval in seconds")
    parser.add_argument("--db", default="data/person_database.json", help="Database file path")
    parser.add_argument("--img-dir", default="images/persons", help="Image directory")
    
    args = parser.parse_args()
    
    # Initialize components
    database = PersonDatabase(args.db, args.img_dir)
    detector = FaceDetector(confidence=0.7)
    recognizer = FaceRecognizer(recognition_threshold=0.6)
    
    # Run selected mode
    if args.mode == "register":
        if not args.name or not args.relation:
            parser.error("--name and --relation are required for registration")
        
        register_person(
            database, 
            recognizer, 
            detector,
            args.name,
            args.relation,
            args.notes,
            args.camera,
            args.images
        )
    else:
        run_recognition_demo(
            database,
            recognizer,
            detector,
            args.camera,
            args.interval
        )

if __name__ == "__main__":
    main() 