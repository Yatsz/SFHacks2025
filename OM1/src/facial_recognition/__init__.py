"""
Facial Recognition Module for Alzheimer's Patient Assistant.

This module provides functionality for real-time person recognition
using computer vision and deep learning techniques.
"""

from .face_detector import FaceDetector
from .face_recognizer import FaceRecognizer
from .database import PersonDatabase

__all__ = ["FaceDetector", "FaceRecognizer", "PersonDatabase"] 