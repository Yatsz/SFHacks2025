"""
Database module for managing person records and embeddings.
Uses JSON for storing data locally with plans for Firebase integration.
"""

import os
import json
import numpy as np
import cv2
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import time
from datetime import datetime
import uuid

class PersonDatabase:
    """Database for managing person records and face embeddings."""
    
    def __init__(self, 
                database_path: str = "data/person_database.json",
                image_folder: str = "images/persons"):
        """
        Initialize the person database.
        
        Args:
            database_path: Path to the JSON database file
            image_folder: Path to the folder storing person images
        """
        self.database_path = Path(database_path)
        self.image_folder = Path(image_folder)
        
        # Ensure directories exist
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.image_folder.mkdir(parents=True, exist_ok=True)
        
        # Initialize or load database
        self.database = self._load_database()
        
    def _load_database(self) -> Dict[str, Dict[str, Any]]:
        """
        Load the database from the JSON file.
        Creates a new empty database if file doesn't exist.
        
        Returns:
            Dictionary containing person records
        """
        if self.database_path.exists():
            try:
                with open(self.database_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading database: {str(e)}")
                return {}
        else:
            return {}
    
    def _save_database(self) -> bool:
        """
        Save the database to the JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.database_path, 'w') as f:
                json.dump(self.database, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving database: {str(e)}")
            return False
    
    def add_person(self, 
                  name: str,
                  relation: str,
                  notes: Optional[str] = None,
                  person_id: Optional[str] = None) -> str:
        """
        Add a new person to the database.
        
        Args:
            name: Person's name
            relation: Relationship to the patient (e.g., "Granddaughter")
            notes: Additional notes about the person (e.g., "Favorite shared song is...")
            person_id: Specific ID to use (generates UUID if None)
            
        Returns:
            Person ID
        """
        # Generate ID if not provided
        if person_id is None:
            person_id = str(uuid.uuid4())
            
        # Check if person already exists
        if person_id in self.database:
            print(f"Person with ID {person_id} already exists, updating info")
            
        # Create or update person record
        self.database[person_id] = {
            "id": person_id,
            "name": name,
            "relation": relation,
            "notes": notes,
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "embeddings": self.database.get(person_id, {}).get("embeddings", []),
            "image_paths": self.database.get(person_id, {}).get("image_paths", [])
        }
        
        # Save database
        self._save_database()
        
        return person_id
    
    def add_face_image(self,
                      person_id: str,
                      image: Union[np.ndarray, str],
                      embedding: Optional[List[float]] = None) -> bool:
        """
        Add a face image for a person, optionally with a pre-computed embedding.
        
        Args:
            person_id: Person ID
            image: Face image (numpy array) or path to image file
            embedding: Optional pre-computed embedding
            
        Returns:
            True if successful, False otherwise
        """
        # Check if person exists
        if person_id not in self.database:
            print(f"Person with ID {person_id} does not exist")
            return False
            
        # Create directory for this person's images if it doesn't exist
        person_img_dir = self.image_folder / person_id
        person_img_dir.mkdir(exist_ok=True)
        
        # Generate filename for image
        timestamp = int(time.time())
        image_filename = f"{timestamp}.jpg"
        image_path = person_img_dir / image_filename
        
        # Save image
        if isinstance(image, np.ndarray):
            cv2.imwrite(str(image_path), image)
        elif isinstance(image, str):
            # If image is a file path, copy it
            if os.path.exists(image):
                img = cv2.imread(image)
                cv2.imwrite(str(image_path), img)
            else:
                print(f"Image file {image} does not exist")
                return False
        else:
            print(f"Invalid image type: {type(image)}")
            return False
            
        # Update database record
        self.database[person_id]["image_paths"].append(str(image_path))
        self.database[person_id]["updated"] = datetime.now().isoformat()
        
        # Add embedding if provided
        if embedding is not None:
            self.database[person_id]["embeddings"].append(embedding)
            
        # Save database
        return self._save_database()
    
    def add_embedding(self, person_id: str, embedding: List[float]) -> bool:
        """
        Add a face embedding for a person.
        
        Args:
            person_id: Person ID
            embedding: Face embedding vector
            
        Returns:
            True if successful, False otherwise
        """
        # Check if person exists
        if person_id not in self.database:
            print(f"Person with ID {person_id} does not exist")
            return False
            
        # Add embedding to person record
        self.database[person_id]["embeddings"].append(embedding)
        self.database[person_id]["updated"] = datetime.now().isoformat()
        
        # Save database
        return self._save_database()
    
    def remove_person(self, person_id: str) -> bool:
        """
        Remove a person from the database.
        
        Args:
            person_id: Person ID
            
        Returns:
            True if successful, False otherwise
        """
        # Check if person exists
        if person_id not in self.database:
            print(f"Person with ID {person_id} does not exist")
            return False
            
        # Remove person from database
        del self.database[person_id]
        
        # Save database
        return self._save_database()
    
    def get_person(self, person_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a person's record.
        
        Args:
            person_id: Person ID
            
        Returns:
            Person record dict or None if not found
        """
        return self.database.get(person_id)
    
    def get_all_persons(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all person records.
        
        Returns:
            Dictionary of all person records
        """
        return self.database
    
    def get_database_for_recognition(self) -> Dict[str, Dict[str, Any]]:
        """
        Get a version of the database suitable for face recognition.
        Only includes persons with embeddings.
        
        Returns:
            Dictionary with person data and embeddings
        """
        recognition_db = {}
        
        for person_id, person_data in self.database.items():
            # Only include persons with embeddings
            if "embeddings" in person_data and person_data["embeddings"]:
                recognition_db[person_id] = person_data
                
        return recognition_db 