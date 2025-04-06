"""
Build a face recognition database from images.

This script processes face images from a directory structure and builds a JSON database 
of face embeddings for recognition. The directory structure should be:

root_dir/
  person1/
    image1.jpg
    image2.jpg
    ...
  person2/
    image1.jpg
    image2.jpg
    ...

Usage:
  python build_database.py --input_dir path/to/images --output_db face_database.json
"""

import os
import cv2
import numpy as np
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

from face_detector import FaceDetector
from face_recognizer import FaceRecognizer

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Build a face recognition database")
    parser.add_argument("--input_dir", type=str, required=True,
                        help="Directory containing person folders with face images")
    parser.add_argument("--output_db", type=str, default="face_database.json",
                        help="Output JSON database file path")
    parser.add_argument("--max_images", type=int, default=5,
                        help="Maximum number of images to process per person")
    parser.add_argument("--min_face_size", type=int, default=80,
                        help="Minimum face size to include (width/height in pixels)")
    parser.add_argument("--confidence", type=float, default=0.7,
                        help="Confidence threshold for face detection")
    parser.add_argument("--augment", action="store_true",
                        help="Apply data augmentation to increase sample diversity")
    return parser.parse_args()

def load_existing_database(db_path: str) -> Dict[str, Dict[str, Any]]:
    """Load existing database if available"""
    if os.path.exists(db_path):
        try:
            with open(db_path, 'r') as f:
                database = json.load(f)
            print(f"Loaded existing database with {len(database)} persons")
            return database
        except Exception as e:
            print(f"Error loading existing database: {e}")
    
    print("Creating new database")
    return {}

def save_database(database: Dict[str, Dict[str, Any]], db_path: str) -> None:
    """Save database to JSON file"""
    try:
        with open(db_path, 'w') as f:
            json.dump(database, f, indent=2)
        print(f"Saved database with {len(database)} persons to {db_path}")
    except Exception as e:
        print(f"Error saving database: {e}")

def augment_face(face_img: np.ndarray) -> List[np.ndarray]:
    """
    Create augmented versions of a face image to improve recognition robustness.
    
    Args:
        face_img: Original face image
        
    Returns:
        List of augmented face images
    """
    augmented = [face_img]  # Start with the original image
    
    # 1. Horizontal flip
    flipped = cv2.flip(face_img, 1)
    augmented.append(flipped)
    
    # 2. Slightly brighter
    brightness = np.ones(face_img.shape, dtype=np.uint8) * 30
    brightened = cv2.add(face_img, brightness)
    augmented.append(brightened)
    
    # 3. Slightly darker
    darkness = np.ones(face_img.shape, dtype=np.uint8) * 30
    darkened = cv2.subtract(face_img, darkness)
    augmented.append(darkened)
    
    # 4. Small rotation clockwise (5 degrees)
    h, w = face_img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, -5, 1.0)
    rotated_cw = cv2.warpAffine(face_img, M, (w, h))
    augmented.append(rotated_cw)
    
    # 5. Small rotation counter-clockwise (5 degrees)
    M = cv2.getRotationMatrix2D(center, 5, 1.0)
    rotated_ccw = cv2.warpAffine(face_img, M, (w, h))
    augmented.append(rotated_ccw)
    
    return augmented

def process_person_images(person_id: str, 
                          image_dir: Path, 
                          detector: FaceDetector, 
                          recognizer: FaceRecognizer,
                          max_images: int,
                          min_face_size: int,
                          do_augment: bool) -> Dict[str, Any]:
    """
    Process images for a single person and generate face embeddings.
    
    Args:
        person_id: Person identifier
        image_dir: Directory containing person's images
        detector: Face detector instance
        recognizer: Face recognizer instance
        max_images: Maximum number of images to process
        min_face_size: Minimum face size to include
        do_augment: Whether to apply data augmentation
        
    Returns:
        Person data dictionary with embeddings
    """
    person_name = person_id.replace('_', ' ').title()
    print(f"\nProcessing images for {person_name}...")
    
    # Initialize person data
    person_data = {
        "id": person_id,
        "name": person_name,
        "embeddings": []
    }
    
    # Get image files
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png']:
        image_files.extend(list(image_dir.glob(f"*{ext}")))
        image_files.extend(list(image_dir.glob(f"*{ext.upper()}")))
    
    # Limit to max_images
    if len(image_files) > max_images:
        print(f"Found {len(image_files)} images, limiting to {max_images}")
        image_files = image_files[:max_images]
    else:
        print(f"Found {len(image_files)} images")
    
    # Process each image
    successful_images = 0
    for img_path in image_files:
        print(f"  Processing {img_path.name}...", end="")
        
        # Read image
        img = cv2.imread(str(img_path))
        if img is None:
            print(" ERROR: Could not read image")
            continue
        
        # Detect faces
        faces, metadata = detector.detect_faces(img)
        
        if not faces:
            print(" No faces detected")
            continue
        
        # Use the largest face
        largest_idx = 0
        largest_area = 0
        for i, meta in enumerate(metadata):
            x1, y1, x2, y2 = meta["bbox"]
            area = (x2 - x1) * (y2 - y1)
            if area > largest_area:
                largest_area = area
                largest_idx = i
        
        face_img = faces[largest_idx]
        bbox = metadata[largest_idx]["bbox"]
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        
        # Skip if face is too small
        if width < min_face_size or height < min_face_size:
            print(f" Face too small ({width}x{height})")
            continue
        
        # Apply augmentation if requested
        face_images = augment_face(face_img) if do_augment else [face_img]
        
        # Generate embeddings for each face version
        for i, f_img in enumerate(face_images):
            embedding = recognizer.generate_embedding(f_img)
            if len(embedding) > 0:
                person_data["embeddings"].append(embedding.tolist())
                
        successful_images += 1
        print(f" OK - Added {len(face_images)} embeddings")
        
        # Display progress
        cv2.imshow("Processing", cv2.resize(face_img, (200, 200)))
        cv2.waitKey(100)
    
    cv2.destroyAllWindows()
    
    print(f"Successfully processed {successful_images}/{len(image_files)} images")
    print(f"Total embeddings for {person_name}: {len(person_data['embeddings'])}")
    
    return person_data

def build_database(args):
    """Build the face recognition database"""
    # Initialize detector and recognizer
    print("Initializing face detector...")
    detector = FaceDetector(confidence=args.confidence)
    
    print("Initializing face recognizer...")
    recognizer = FaceRecognizer(enforce_detection=False)
    
    # Load existing database if available
    database = load_existing_database(args.output_db)
    
    # Get person directories
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"Error: Input directory {args.input_dir} does not exist")
        return
    
    person_dirs = [d for d in input_dir.iterdir() if d.is_dir()]
    if not person_dirs:
        print(f"Error: No person directories found in {args.input_dir}")
        return
    
    print(f"Found {len(person_dirs)} person directories")
    
    # Process each person
    for person_dir in person_dirs:
        person_id = person_dir.name
        
        # Process person's images
        person_data = process_person_images(
            person_id=person_id,
            image_dir=person_dir,
            detector=detector,
            recognizer=recognizer,
            max_images=args.max_images,
            min_face_size=args.min_face_size,
            do_augment=args.augment
        )
        
        # Add/update person in database
        if len(person_data["embeddings"]) > 0:
            database[person_id] = person_data
            print(f"Added/updated {person_id} in database")
        else:
            print(f"No valid embeddings generated for {person_id}, skipping")
    
    # Save the database
    save_database(database, args.output_db)
    
    # Print summary
    total_persons = len(database)
    total_embeddings = sum(len(person["embeddings"]) for person in database.values())
    print("\nDatabase Summary:")
    print(f"  Total persons: {total_persons}")
    print(f"  Total embeddings: {total_embeddings}")
    print(f"  Average embeddings per person: {total_embeddings / total_persons if total_persons > 0 else 0:.1f}")
    
    return database

def main():
    """Main function"""
    args = parse_args()
    build_database(args)

if __name__ == "__main__":
    main() 