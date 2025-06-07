from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from ultralytics import YOLO
import base64
import torch

# PyTorch 2.6+ defaults to weights_only=True; YOLO .pt checkpoints need full pickle loading.
original_torch_load = torch.load

def custom_torch_load(*args, **kwargs):
    kwargs.setdefault('weights_only', False)
    return original_torch_load(*args, **kwargs)

torch.load = custom_torch_load

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
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=422, detail="File must be an image")

    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=422, detail="Could not process image")

        results = model(img, conf=0.5, verbose=False)

        detections = results[0].boxes
        if detections is not None:
            class_ids = detections.cls.tolist()
            class_names = [model.names[int(id)] for id in class_ids]
        else:
            class_names = []

        class_counts = {}
        for name in class_names:
            class_counts[name] = class_counts.get(name, 0) + 1

        annotated_frame = results[0].plot()

        _, buffer = cv2.imencode('.jpg', annotated_frame)
        img_bytes = buffer.tobytes()

        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        return {
            "detections": class_counts,
            "image": img_base64
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
