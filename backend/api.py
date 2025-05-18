from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from ultralytics import YOLO
import io
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO('model/modelin.pt') 

@app.post("/detect")
async def detect_pills(file: UploadFile = File(...)):
    # Validar el tipo de archivo
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=422, detail="El archivo debe ser una imagen")
    
    try:
        # Lee la imagen subida
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=422, detail="No se pudo procesar la imagen")
        
        # Realiza la detección
        results = model(img, conf=0.5, verbose=False)
        
        # Obtiene las detecciones
        detections = results[0].boxes
        if detections is not None:
            class_ids = detections.cls.tolist()
            class_names = [model.names[int(id)] for id in class_ids]
        else:
            class_names = []
        
        # Cuenta objetos por clase
        class_counts = {}
        for name in class_names:
            class_counts[name] = class_counts.get(name, 0) + 1
        
        # Dibuja las detecciones en la imagen
        annotated_frame = results[0].plot()
        
        # Convierte la imagen anotada a bytes
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        img_bytes = buffer.tobytes()
        
        # Convierte bytes a base64
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        return {
            "detections": class_counts,
            "image": img_base64
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e)) 