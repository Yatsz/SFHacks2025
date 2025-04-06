"""
Setup script for the facial recognition module.

This script creates necessary directories and downloads required models.
"""

import os
import sys
from pathlib import Path
import shutil
import argparse

def setup_facial_recognition(
    data_dir="data",
    images_dir="images/persons",
    download_models=True,
    force_download=False
):
    """
    Set up the facial recognition module.
    
    Args:
        data_dir: Directory for storing JSON database
        images_dir: Directory for storing person images
        download_models: Whether to download required models
        force_download: Whether to force re-download of models
    """
    # Create directories
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    print(f"Created directory: {data_dir}")
    print(f"Created directory: {images_dir}")
    
    # Check for local face detection model
    local_model_path = os.path.join(os.path.dirname(__file__), 'model.pt')
    if os.path.exists(local_model_path):
        print(f"Found local face detection model: {local_model_path}")
        print("This local model will be prioritized for face detection.")
    else:
        print("Local face detection model not found.")
        print(f"You can add your own model by placing it at: {local_model_path}")
        
        if download_models:
            try:
                print("Downloading default YOLOv8 face detection model...")
                from ultralytics import YOLO
                
                if force_download:
                    # Directly download and save to local path
                    model = YOLO("yolov8n-face.pt")
                    print(f"Saving model to: {local_model_path}")
                    model_path = model.export(format="pytorch")
                    shutil.copy(model_path, local_model_path)
                else:
                    # Just download to cache (will be used as fallback)
                    model = YOLO("yolov8n-face.pt")
                    print("Model downloaded to cache and will be used as fallback if no local model is found.")
            except ImportError:
                print("Warning: ultralytics package not installed. Cannot download models.")
                print("Please install required packages using 'pip install ultralytics'")
    
    # Check DeepFace model availability
    if download_models:
        try:
            from deepface import DeepFace
            
            # This will trigger download of required models if they don't exist
            print("Checking DeepFace model availability...")
            DeepFace.build_model("Facenet")
            print("DeepFace models are ready.")
            
        except ImportError:
            print("Warning: deepface package not installed. Cannot check/download models.")
            print("Please install required packages using 'pip install deepface'")
    
    print("\nSetup complete!")
    print("\nTo register a new person, run:")
    print("python -m src.facial_recognition.demo --mode register --name \"Name\" --relation \"Relation\" --notes \"Notes\"")
    print("\nTo run recognition demo, run:")
    print("python -m src.facial_recognition.demo --mode recognize")

def main():
    """Main function for the setup script."""
    parser = argparse.ArgumentParser(description="Setup script for facial recognition module")
    parser.add_argument("--data-dir", default="data", help="Directory for storing JSON database")
    parser.add_argument("--images-dir", default="images/persons", help="Directory for storing person images")
    parser.add_argument("--no-download", action="store_false", dest="download_models", 
                        help="Skip downloading models")
    parser.add_argument("--force-download", action="store_true", help="Force re-download of models")
    
    args = parser.parse_args()
    
    setup_facial_recognition(
        args.data_dir,
        args.images_dir,
        args.download_models,
        args.force_download
    )

if __name__ == "__main__":
    main() 