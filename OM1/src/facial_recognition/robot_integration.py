"""
Robot integration module for facial recognition system.

This module integrates the facial recognition system with the TurtleBot4
and other components of the Alzheimer's Patient Assistant.
"""

import os
import cv2
import time
import threading
import numpy as np
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
import json

from .face_detector import FaceDetector
from .face_recognizer import FaceRecognizer
from .database import PersonDatabase
from .utils import preprocess_image_for_recognition

class FacialRecognitionService:
    """
    Service for integrating facial recognition with the robot system.
    Handles continuous face detection, recognition, and event callbacks.
    """
    
    def __init__(self, 
                database_path: str = "data/person_database.json",
                image_folder: str = "images/persons",
                detector_confidence: float = 0.7,
                recognition_threshold: float = 0.6,
                recognition_interval: float = 2.0,
                speaker_callback: Optional[Callable[[str], None]] = None):
        """
        Initialize the facial recognition service.
        
        Args:
            database_path: Path to person database
            image_folder: Path to image storage folder
            detector_confidence: Confidence threshold for face detection
            recognition_threshold: Threshold for face recognition
            recognition_interval: Minimum time between recognition attempts (seconds)
            speaker_callback: Callback function for speaking recognition results
        """
        # Initialize components
        self.database = PersonDatabase(database_path, image_folder)
        self.detector = FaceDetector(confidence=detector_confidence)
        self.recognizer = FaceRecognizer(recognition_threshold=recognition_threshold)
        
        # Configuration
        self.recognition_interval = recognition_interval
        self.speaker_callback = speaker_callback
        
        # State variables
        self.running = False
        self.last_recognition_time = 0
        self.last_recognition_results = {}
        self.recognition_thread = None
        self.camera = None
        self.camera_id = 0
        
        # Load recognition database
        self.recognition_db = self.database.get_database_for_recognition()
        
    def set_speaker_callback(self, callback: Callable[[str], None]):
        """
        Set the callback function for speaking recognition results.
        
        Args:
            callback: Function that takes a string message and handles speech output
        """
        self.speaker_callback = callback
        
    def reload_database(self):
        """Reload the recognition database from storage."""
        self.recognition_db = self.database.get_database_for_recognition()
        
    def start(self, camera_id: int = 0):
        """
        Start the facial recognition service.
        
        Args:
            camera_id: Camera device ID to use
        """
        if self.running:
            print("Facial recognition service is already running")
            return
            
        # Set camera ID
        self.camera_id = camera_id
        
        # Start recognition thread
        self.running = True
        self.recognition_thread = threading.Thread(target=self._recognition_loop)
        self.recognition_thread.daemon = True
        self.recognition_thread.start()
        
        print(f"Facial recognition service started with camera {camera_id}")
        
    def stop(self):
        """Stop the facial recognition service."""
        if not self.running:
            print("Facial recognition service is not running")
            return
            
        # Stop thread
        self.running = False
        if self.recognition_thread:
            self.recognition_thread.join(timeout=1.0)
            
        # Release camera
        if self.camera:
            self.camera.release()
            self.camera = None
            
        print("Facial recognition service stopped")
        
    def _recognition_loop(self):
        """Main recognition loop running in a separate thread."""
        # Open camera
        self.camera = cv2.VideoCapture(self.camera_id)
        
        if not self.camera.isOpened():
            print(f"Error: Could not open camera {self.camera_id}")
            self.running = False
            return
            
        print("Facial recognition loop started")
        
        while self.running:
            # Capture frame
            ret, frame = self.camera.read()
            
            if not ret:
                print("Error: Failed to capture image from camera")
                time.sleep(0.1)
                continue
                
            # Check if it's time for another recognition attempt
            current_time = time.time()
            if current_time - self.last_recognition_time >= self.recognition_interval:
                # Detect faces
                faces, metadata = self.detector.detect_faces(frame)
                
                if faces:
                    # Perform recognition on detected faces
                    self._process_faces(faces, metadata, frame)
                    
                    # Update last recognition time
                    self.last_recognition_time = current_time
            
            # Short sleep to prevent maxing out CPU
            time.sleep(0.01)
            
        # Clean up
        if self.camera:
            self.camera.release()
            self.camera = None
    
    def _process_faces(self, faces: List[np.ndarray], metadata: List[Dict[str, Any]], frame: np.ndarray):
        """
        Process detected faces for recognition.
        
        Args:
            faces: List of face images
            metadata: List of face metadata
            frame: Original frame
        """
        # Dictionary to track current recognition results
        current_results = {}
        recognized_persons = []
        
        # Process each face
        for i, (face_img, face_meta) in enumerate(zip(faces, metadata)):
            # Preprocess face
            face_img = preprocess_image_for_recognition(face_img)
            
            # Recognize face
            person_id, similarity, person_data = self.recognizer.recognize_face_image(
                face_img, self.recognition_db
            )
            
            # Store result
            bbox = face_meta["bbox"]
            current_results[i] = {
                "bbox": bbox,
                "person_id": person_id,
                "similarity": similarity,
                "person_data": person_data
            }
            
            # Add to recognized persons if known
            if person_id != "unknown":
                recognized_persons.append(person_data)
        
        # Update last recognition results
        self.last_recognition_results = current_results
        
        # Generate speech for recognized persons
        self._announce_recognized_persons(recognized_persons)
    
    def _announce_recognized_persons(self, persons: List[Dict[str, Any]]):
        """
        Generate and speak announcements for recognized persons.
        
        Args:
            persons: List of recognized person data
        """
        if not self.speaker_callback or not persons:
            return
            
        # Process each recognized person
        for person in persons:
            name = person.get("name", "Unknown")
            relation = person.get("relation", "")
            notes = person.get("notes", "")
            
            # Build speech message
            message = f"This is {name}"
            
            if relation:
                message += f", your {relation}"
                
            if notes:
                message += f". {notes}"
                
            # Send to speaker
            self.speaker_callback(message)
            
    def get_current_recognition_results(self) -> Dict[int, Dict[str, Any]]:
        """
        Get the most recent recognition results.
        
        Returns:
            Dictionary of face index to recognition data
        """
        return self.last_recognition_results.copy()
    
    def is_running(self) -> bool:
        """
        Check if the service is running.
        
        Returns:
            True if running, False otherwise
        """
        return self.running 