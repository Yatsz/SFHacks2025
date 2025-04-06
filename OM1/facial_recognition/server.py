from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import json
import base64
from io import BytesIO
from PIL import Image

from face_detector import FaceDetector
from face_recognizer import FaceRecognizer

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize face detection and recognition
detector = FaceDetector(confidence=0.5)
recognizer = FaceRecognizer(recognition_threshold=0.6)

# Load face database
try:
    with open('data/face_database.json', 'r') as f:
        face_database = json.load(f)
    print(f"Loaded face database with {len(face_database)} entries")
except Exception as e:
    print(f"Error loading face database: {e}")
    face_database = {}

class ImageRequest(BaseModel):
    image: str  # Base64 encoded image

def process_base64_image(base64_string: str):
    # Remove data URL prefix if present
    if 'base64,' in base64_string:
        base64_string = base64_string.split('base64,')[1]
    
    # Decode base64 string to bytes
    image_bytes = base64.b64decode(base64_string)
    
    # Convert to PIL Image
    image = Image.open(BytesIO(image_bytes))
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert to numpy array
    return np.array(image)

@app.post("/detect")
async def detect_faces(request: ImageRequest):
    try:
        # Convert base64 to numpy array
        image = process_base64_image(request.image)
        
        # Detect faces
        faces, metadata = detector.detect_faces(image)
        
        # List to store detected persons
        detected_persons = []
        
        # Process each detected face
        for face_img in faces:
            # Recognize face
            person_id, similarity, person_data = recognizer.recognize_face_image(
                face_img, 
                face_database
            )
            
            # Always add the person to the list, even if unknown
            person_info = {
                "name": person_data.get("name", person_id) if person_id != "unknown" else "unknown",
                "similarity": float(similarity) if person_id != "unknown" else 0.0,
                "relation": person_data.get("relation", "Unknown") if person_id != "unknown" else "Unknown"
            }
            detected_persons.append(person_info)
        
        return {"persons": detected_persons}
    
    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database_loaded": len(face_database) > 0,
        "database_size": len(face_database)
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting facial recognition API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 