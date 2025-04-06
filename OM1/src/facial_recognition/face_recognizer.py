"""
Face recognition module for identifying people from face images.
Uses DeepFace with FaceNet for generating face embeddings and recognition.
"""

import os
import cv2
import numpy as np
from typing import List, Dict, Any, Tuple, Optional, Union
from pathlib import Path
import json
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity

class FaceRecognizer:
    """Face recognition system using DeepFace and FaceNet embeddings."""
    
    def __init__(self, 
                 model_name: str = "Facenet",
                 distance_metric: str = "cosine",
                 recognition_threshold: float = 0.6,
                 enforce_detection: bool = False):
        """
        Initialize face recognition system.
        
        Args:
            model_name: Model to use for face recognition (e.g., "Facenet", "ArcFace")
            distance_metric: Distance metric for similarity ("cosine", "euclidean", etc.)
            recognition_threshold: Threshold for recognition (lower is more strict)
            enforce_detection: Whether to enforce face detection in DeepFace
        """
        self.model_name = model_name
        self.distance_metric = distance_metric
        self.recognition_threshold = recognition_threshold
        self.enforce_detection = enforce_detection
        
    def generate_embedding(self, face_img: np.ndarray) -> np.ndarray:
        """
        Generate embedding for a face image.
        
        Args:
            face_img: Face image (BGR format)
            
        Returns:
            Embedding vector as numpy array
        """
        try:
            # Generate embedding using DeepFace
            embedding_obj = DeepFace.represent(
                img_path=face_img,
                model_name=self.model_name,
                enforce_detection=self.enforce_detection
            )
            
            # Extract the embedding vector
            embedding = np.array(embedding_obj[0]["embedding"])
            return embedding
            
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            # Return empty embedding in case of error
            return np.array([])
        
    def recognize_face(self, 
                       face_embedding: np.ndarray, 
                       database: Dict[str, Dict[str, Any]]) -> Tuple[str, float, Dict[str, Any]]:
        """
        Recognize a face by comparing its embedding with the database.
        
        Args:
            face_embedding: Embedding vector of the query face
            database: Dictionary of person records with embeddings
            
        Returns:
            Tuple containing:
            - ID of the recognized person (or "unknown")
            - Similarity score
            - Person record from database (or empty dict)
        """
        if len(face_embedding) == 0 or not database:
            return "unknown", 0.0, {}
        
        max_similarity = -1
        recognized_id = "unknown"
        person_record = {}
        
        # Compare with each person in the database
        for person_id, person_data in database.items():
            # Get all embeddings for this person
            person_embeddings = person_data.get("embeddings", [])
            
            if not person_embeddings:
                continue
                
            # Calculate similarity with each embedding
            similarities = []
            for emb in person_embeddings:
                emb_array = np.array(emb)
                # Reshape for sklearn
                similarity = cosine_similarity([face_embedding], [emb_array])[0][0]
                similarities.append(similarity)
            
            # Get maximum similarity
            person_similarity = max(similarities)
            
            # Update if this is the best match so far
            if person_similarity > max_similarity:
                max_similarity = person_similarity
                recognized_id = person_id
                person_record = person_data
        
        # Return unknown if similarity is below threshold
        if max_similarity < self.recognition_threshold:
            return "unknown", max_similarity, {}
            
        return recognized_id, max_similarity, person_record
    
    def recognize_face_image(self, 
                           face_img: np.ndarray, 
                           database: Dict[str, Dict[str, Any]]) -> Tuple[str, float, Dict[str, Any]]:
        """
        Recognize a face directly from an image.
        
        Args:
            face_img: Face image (BGR format)
            database: Dictionary of person records with embeddings
            
        Returns:
            Tuple containing:
            - ID of the recognized person (or "unknown")
            - Similarity score
            - Person record from database (or empty dict)
        """
        # Generate embedding
        embedding = self.generate_embedding(face_img)
        
        # Recognize face
        return self.recognize_face(embedding, database) 