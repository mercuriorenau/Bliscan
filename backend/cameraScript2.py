import cv2
from ultralytics import YOLO
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import threading
import time
import os
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

current_frame = None
current_detections = None
frame_lock = threading.Lock()

# Ruta al modelo YOLO personalizado
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'best.pt')
model = None

def load_model():
    global model
    model = YOLO('model/modelin.pt')
    print("Modelo YOLO cargado correctamente.")

def generate_frames():
    global current_frame, current_detections
    while True:
        with frame_lock:
            if current_frame is not None:
                ret, buffer = cv2.imencode('.jpg', current_frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)

def process_camera():
    global current_frame, current_detections
    cap = cv2.VideoCapture(0)
    print("Intentando abrir la webcam (device 0)")
    if not cap.isOpened():
        print("Error: No se pudo abrir la webcam.")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer la webcam.")
            continue

        # --- Detección YOLO ---
        results = model(frame)
        annotated_frame = results[0].plot()  # Dibuja las cajas y clases sobre el frame

        # Contar detecciones
        detections = results[0].boxes
        if detections is not None:
            class_ids = detections.cls.tolist()
            class_names = [model.names[int(id)] for id in class_ids]
            class_counts = {}
            for name in class_names:
                class_counts[name] = class_counts.get(name, 0) + 1
        else:
            class_counts = {}

        with frame_lock:
            current_frame = annotated_frame
            current_detections = class_counts
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detections')
def get_detections():
    with frame_lock:
        if current_detections is None:
            return jsonify({"pill": 0, "empty": 0})
        return jsonify(current_detections)

@app.route('/detect', methods=['POST'])
def detect_pills():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    contents = file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is not None:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # Perform detection
    results = model(img, conf=0.5, verbose=True)
    
    # Get detections
    detections = results[0].boxes
    if detections is not None:
        class_ids = detections.cls.tolist()
        class_names = [model.names[int(id)] for id in class_ids]
        class_counts = {}
        for name in class_names:
            class_counts[name] = class_counts.get(name, 0) + 1
    else:
        class_counts = {}
    
    return jsonify(class_counts)

if __name__ == '__main__':
    load_model()  # Cargar el modelo YOLO al iniciar
    camera_thread = threading.Thread(target=process_camera)
    camera_thread.daemon = True
    camera_thread.start()
    app.run(host='0.0.0.0', port=5002, debug=True)
