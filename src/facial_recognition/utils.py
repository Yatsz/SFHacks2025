"""
Utility functions for image augmentation and processing.
"""

import cv2
import numpy as np
from typing import List, Tuple
import random

def augment_face_image(image: np.ndarray, 
                      num_augmentations: int = 4) -> List[np.ndarray]:
    """
    Create augmented versions of a face image.
    
    Args:
        image: Original face image (BGR format)
        num_augmentations: Number of augmented images to generate
        
    Returns:
        List of augmented images
    """
    augmented_images = []
    
    # Original image is always included
    augmented_images.append(image.copy())
    
    # Generate augmentations
    for i in range(num_augmentations):
        # Choose random augmentation techniques for this image
        flip = random.choice([True, False])
        brightness = random.uniform(0.7, 1.3)
        rotation = random.uniform(-10, 10)
        crop_percent = random.uniform(0.85, 0.95)
        
        # Start with original image
        aug_img = image.copy()
        
        # Apply horizontal flip
        if flip:
            aug_img = cv2.flip(aug_img, 1)
            
        # Apply brightness adjustment
        aug_img = adjust_brightness(aug_img, brightness)
        
        # Apply rotation
        aug_img = rotate_image(aug_img, rotation)
        
        # Apply random crop
        aug_img = random_crop(aug_img, crop_percent)
        
        # Resize back to original dimensions
        aug_img = cv2.resize(aug_img, (image.shape[1], image.shape[0]))
        
        augmented_images.append(aug_img)
    
    return augmented_images

def adjust_brightness(image: np.ndarray, factor: float) -> np.ndarray:
    """
    Adjust the brightness of an image.
    
    Args:
        image: Input image (BGR format)
        factor: Brightness factor (1.0 = original, >1 = brighter, <1 = darker)
        
    Returns:
        Brightness-adjusted image
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv = hsv.astype(np.float32)
    
    # Adjust V channel (brightness)
    hsv[:, :, 2] = hsv[:, :, 2] * factor
    hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
    
    hsv = hsv.astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    """
    Rotate an image by a specified angle.
    
    Args:
        image: Input image (BGR format)
        angle: Rotation angle in degrees
        
    Returns:
        Rotated image
    """
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    
    # Get rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Apply rotation
    rotated = cv2.warpAffine(image, rotation_matrix, (width, height), 
                            flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    
    return rotated

def random_crop(image: np.ndarray, crop_percent: float) -> np.ndarray:
    """
    Perform a random crop of an image.
    
    Args:
        image: Input image (BGR format)
        crop_percent: Percentage of original image size to keep (0.0 to 1.0)
        
    Returns:
        Cropped image
    """
    height, width = image.shape[:2]
    
    # Calculate crop dimensions
    crop_height = int(height * crop_percent)
    crop_width = int(width * crop_percent)
    
    # Calculate maximum allowable offsets
    max_x = width - crop_width
    max_y = height - crop_height
    
    # Generate random crop position
    x = random.randint(0, max(0, max_x))
    y = random.randint(0, max(0, max_y))
    
    # Perform crop
    cropped = image[y:y+crop_height, x:x+crop_width]
    
    return cropped

def preprocess_image_for_recognition(image: np.ndarray) -> np.ndarray:
    """
    Preprocess an image for better face recognition.
    
    Args:
        image: Input image (BGR format)
        
    Returns:
        Preprocessed image
    """
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    if len(image.shape) == 3:
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        
        # Merge channels
        limg = cv2.merge((cl, a, b))
        
        # Convert back to BGR
        processed = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    else:
        # For grayscale images
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        processed = clahe.apply(image)
    
    return processed 