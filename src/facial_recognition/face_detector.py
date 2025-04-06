"""
Face detection module for extracting and localizing faces in images or video streams.
Uses YOLOv8 for efficient real-time face detection.
"""

import os
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
from typing import List, Tuple, Dict, Any, Optional

class FaceDetector:
    """Face detector using YOLOv8 for real-time detection."""
    
    def __init__(self, 
                 model_path: Optional[str] = None,
                 confidence: float = 0.5,
                 device: str = "auto"):
        """
        Initialize the face detector.
        
        Args:
            model_path: Path to the YOLOv8 face detection model.
                        If None, will prioritize using local model.pt in the same directory.
            confidence: Confidence threshold for detections (0.0 to 1.0)
            device: Device to run inference on ('cpu', 'cuda', or 'auto')
        """
        # Always try to use local model.pt first
        local_model_path = os.path.join(os.path.dirname(__file__), 'model.pt')
        
        if os.path.exists(local_model_path):
            print(f"Using local model: {local_model_path}")
            self.model = YOLO(local_model_path)
        elif model_path is not None:
            print(f"Using specified model: {model_path}")
            self.model = YOLO(model_path)
        else:
            # Fall back to default downloaded model if local model is not found
            print("Local model not found. Using default YOLOv8 face detection model.")
            self.model = YOLO('yolov8n-face.pt')
            
        self.confidence = confidence
        self.device = device
        
    def detect_faces(self, 
                    image: np.ndarray, 
                    return_cropped: bool = True) -> Tuple[List[np.ndarray], List[Dict[str, Any]]]:
        """
        Detect faces in an image.
        
        Args:
            image: Input image (BGR format from OpenCV)
            return_cropped: Whether to return cropped face images
            
        Returns:
            Tuple containing:
            - List of cropped face images (if return_cropped=True)
            - List of detection metadata (bounding boxes, confidence, etc.)
        """
        # Run inference with model
        results = self.model(image, conf=self.confidence, verbose=False)
        
        faces = []
        metadata = []
        
        # Process each detection
        for result in results:
            boxes = result.boxes
            
            for i, box in enumerate(boxes):
                # Get bounding box coordinates (convert to integers)
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                
                # Get confidence score
                conf = float(box.conf[0])
                
                # Create metadata dictionary
                face_meta = {
                    "bbox": (x1, y1, x2, y2),
                    "confidence": conf,
                    "center": ((x1 + x2) // 2, (y1 + y2) // 2)
                }
                
                metadata.append(face_meta)
                
                # Crop face if requested
                if return_cropped:
                    # Add some margin to the crop for better recognition
                    margin_x = int((x2 - x1) * 0.1)
                    margin_y = int((y2 - y1) * 0.1)
                    
                    # Ensure we don't go out of image bounds
                    crop_x1 = max(0, x1 - margin_x)
                    crop_y1 = max(0, y1 - margin_y)
                    crop_x2 = min(image.shape[1], x2 + margin_x)
                    crop_y2 = min(image.shape[0], y2 + margin_y)
                    
                    face_img = image[crop_y1:crop_y2, crop_x1:crop_x2]
                    faces.append(face_img)
        
        return faces, metadata
    
    def detect_faces_and_draw(self, 
                             image: np.ndarray, 
                             color: Tuple[int, int, int] = (0, 255, 0),
                             thickness: int = 2,
                             draw_confidence: bool = True) -> np.ndarray:
        """
        Detect faces and draw bounding boxes on the input image.
        
        Args:
            image: Input image (BGR format)
            color: Bounding box color (BGR format)
            thickness: Bounding box thickness
            draw_confidence: Whether to draw confidence scores
            
        Returns:
            Image with drawn bounding boxes
        """
        # Create a copy of the image
        output_img = image.copy()
        
        # Detect faces
        _, metadata = self.detect_faces(image, return_cropped=False)
        
        # Draw bounding boxes
        for face in metadata:
            x1, y1, x2, y2 = face["bbox"]
            conf = face["confidence"]
            
            # Draw rectangle
            cv2.rectangle(output_img, (x1, y1), (x2, y2), color, thickness)
            
            # Draw confidence score
            if draw_confidence:
                conf_text = f"{conf:.2f}"
                cv2.putText(output_img, conf_text, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)
        
        return output_img 