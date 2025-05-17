from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from ultralytics import YOLO
import io
import base64

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO('model/modelin.pt') 

@app.post("/detect")
async def detect_pills(file: UploadFile = File(...)):
    # Read the uploaded image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Perform detection
    results = model(img, conf=0.5, verbose=False)
    
    # Get detections
    detections = results[0].boxes
    if detections is not None:
        class_ids = detections.cls.tolist()
        class_names = [model.names[int(id)] for id in class_ids]
    else:
        class_names = []
    
    # Count objects by class
    class_counts = {}
    for name in class_names:
        class_counts[name] = class_counts.get(name, 0) + 1
    
    # Draw detections on image
    annotated_frame = results[0].plot()
    
    # Convert the annotated image to bytes
    _, buffer = cv2.imencode('.jpg', annotated_frame)
    img_bytes = buffer.tobytes()
    
    # Convert bytes to base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return {
        "detections": class_counts,
        "image": img_base64
    } 