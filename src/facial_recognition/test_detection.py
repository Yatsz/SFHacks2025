"""
Test script for facial detection only.

This script demonstrates the facial detection capabilities
without the full recognition system.
"""

import cv2
import argparse
import time
from pathlib import Path

# Fix the import to use a relative import within the same package
from .face_detector import FaceDetector

def test_webcam_detection(camera_id=0, confidence=0.5, display_fps=True):
    """
    Test facial detection using webcam feed.
    
    Args:
        camera_id: Camera device ID
        confidence: Detection confidence threshold
        display_fps: Whether to display frames per second
    """
    # Initialize detector
    print("Initializing face detector...")
    detector = FaceDetector(confidence=confidence)
    
    # Open webcam
    print(f"Opening camera {camera_id}...")
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_id}")
        return
    
    print("Face detection test started. Press 'q' to quit.")
    
    # Variables for FPS calculation
    frame_count = 0
    start_time = time.time()
    fps = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture image")
            break
        
        # Detect faces
        detection_start = time.time()
        faces, metadata = detector.detect_faces(frame)
        detection_time = (time.time() - detection_start) * 1000  # Convert to ms
        
        # Draw detection on frame
        display_frame = detector.detect_faces_and_draw(frame)
        
        # Update FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1.0:  # Update FPS every second
            fps = frame_count / elapsed_time
            frame_count = 0
            start_time = time.time()
        
        # Display info
        if display_fps:
            cv2.putText(display_frame, f"FPS: {fps:.1f}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(display_frame, f"Detection: {detection_time:.1f} ms", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(display_frame, f"Faces found: {len(faces)}", 
                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
        # Display faces found
        for i, (face_img, face_meta) in enumerate(zip(faces, metadata)):
            # Create a separate window for each detected face
            face_window_name = f"Face {i+1}"
            cv2.imshow(face_window_name, face_img)
            
            # Position the windows in a logical way
            cv2.moveWindow(face_window_name, 800, i * 200)
        
        # Display the main frame
        cv2.imshow("Face Detection Test", display_frame)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    print("Test completed.")

def test_image_detection(image_path, confidence=0.5):
    """
    Test facial detection on a single image.
    
    Args:
        image_path: Path to image file
        confidence: Detection confidence threshold
    """
    # Initialize detector
    print("Initializing face detector...")
    detector = FaceDetector(confidence=confidence)
    
    # Load image
    print(f"Loading image: {image_path}")
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Could not load image {image_path}")
        return
    
    # Detect faces
    detection_start = time.time()
    faces, metadata = detector.detect_faces(image)
    detection_time = (time.time() - detection_start) * 1000  # Convert to ms
    
    # Draw detection on image
    display_image = detector.detect_faces_and_draw(image)
    
    # Display info
    print(f"Detection time: {detection_time:.1f} ms")
    print(f"Faces found: {len(faces)}")
    
    # Display faces found
    for i, (face_img, face_meta) in enumerate(zip(faces, metadata)):
        # Create a separate window for each detected face
        face_window_name = f"Face {i+1}"
        cv2.imshow(face_window_name, face_img)
        
        # Position the windows in a logical way
        cv2.moveWindow(face_window_name, 800, i * 200)
        
        # Print face metadata
        print(f"Face {i+1}:")
        print(f"  Confidence: {face_meta['confidence']:.4f}")
        print(f"  Bounding box: {face_meta['bbox']}")
    
    # Display the main image
    cv2.imshow("Face Detection Test", display_image)
    print("Press any key to exit...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Test completed.")

def main():
    """Main function for test script."""
    parser = argparse.ArgumentParser(description="Test facial detection")
    parser.add_argument("--mode", choices=["webcam", "image"], default="webcam",
                      help="Test mode: use webcam or single image")
    parser.add_argument("--camera", type=int, default=0, 
                      help="Camera device ID (for webcam mode)")
    parser.add_argument("--image", help="Path to image file (for image mode)")
    parser.add_argument("--confidence", type=float, default=0.5, 
                      help="Detection confidence threshold")
    parser.add_argument("--no-fps", action="store_false", dest="display_fps", 
                      help="Hide FPS display")
    
    args = parser.parse_args()
    
    if args.mode == "webcam":
        test_webcam_detection(args.camera, args.confidence, args.display_fps)
    else:  # image mode
        if not args.image:
            parser.error("--image is required for image mode")
        test_image_detection(args.image, args.confidence)

if __name__ == "__main__":
    main() 