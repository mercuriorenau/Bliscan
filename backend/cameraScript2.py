import cv2
import torch

# PyTorch 2.6+ defaults to weights_only=True; YOLO .pt checkpoints need full pickle loading.
_original_torch_load = torch.load

def _torch_load_trusted_weights(*args, **kwargs):
    kwargs.setdefault("weights_only", False)
    return _original_torch_load(*args, **kwargs)

torch.load = _torch_load_trusted_weights

from ultralytics import YOLO
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import threading
import os
import time
import numpy as np

# Balanced stream rate (30 FPS). Set BLISCAN_STREAM_FPS=0 to uncap.
STREAM_FPS = int(os.environ.get("BLISCAN_STREAM_FPS", "30"))
STREAM_INTERVAL = 0.0 if STREAM_FPS <= 0 else 1.0 / STREAM_FPS

# Capture at HD when the webcam supports it.
CAMERA_WIDTH = int(os.environ.get("BLISCAN_CAMERA_WIDTH", "1280"))
CAMERA_HEIGHT = int(os.environ.get("BLISCAN_CAMERA_HEIGHT", "720"))
CAMERA_FPS = int(os.environ.get("BLISCAN_CAMERA_FPS", "30"))

# High JPEG quality for the clearest MJPEG stream.
JPEG_QUALITY = int(os.environ.get("BLISCAN_JPEG_QUALITY", "95"))

# Match training image size for best detection quality.
INFERENCE_IMGSZ = int(os.environ.get("BLISCAN_INFERENCE_IMGSZ", "640"))

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'modelin.pt')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

frame_lock = threading.Lock()
latest_frame = None
current_detections = None
overlay_boxes = []
model = None
inference_lock = threading.Lock()


def load_model():
    global model
    model = YOLO(MODEL_PATH)
    print("YOLO model loaded successfully.")


def _box_color(label: str):
    if label.lower() == "empty":
        return (0, 0, 255)
    if label.lower() == "full":
        return (0, 255, 0)
    return (0, 180, 255)


def overlay_boxes_on_frame(frame, boxes):
    if not boxes:
        return frame
    out = frame.copy()
    for x1, y1, x2, y2, label, color in boxes:
        cv2.rectangle(out, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            out,
            label,
            (x1, max(y1 - 8, 16)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color,
            2,
            cv2.LINE_AA,
        )
    return out


def _parse_detections(results):
    detections = results[0].boxes
    class_counts = {}
    boxes = []

    if detections is None:
        return class_counts, boxes

    class_ids = detections.cls.tolist()
    class_names = [model.names[int(cls_id)] for cls_id in class_ids]

    for name in class_names:
        class_counts[name] = class_counts.get(name, 0) + 1

    for box, cls_id in zip(detections.xyxy.tolist(), class_ids):
        x1, y1, x2, y2 = map(int, box)
        label = model.names[int(cls_id)]
        boxes.append((x1, y1, x2, y2, label, _box_color(label)))

    return class_counts, boxes


def capture_loop():
    """Read webcam frames as fast as possible; always keep only the latest frame."""
    global latest_frame

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)

    print(
        f"Opening webcam (device 0) at {CAMERA_WIDTH}x{CAMERA_HEIGHT} "
        f"target {CAMERA_FPS} FPS"
    )

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read from webcam.")
            time.sleep(0.01)
            continue

        with frame_lock:
            latest_frame = frame

    cap.release()


def inference_loop():
    """Run YOLO in a dedicated thread so capture/streaming are not blocked."""
    global current_detections, overlay_boxes

    while model is None:
        time.sleep(0.05)

    while True:
        if not inference_lock.acquire(blocking=False):
            time.sleep(0.001)
            continue

        try:
            with frame_lock:
                frame = None if latest_frame is None else latest_frame.copy()

            if frame is None:
                continue

            results = model(
                frame,
                conf=0.5,
                verbose=False,
                imgsz=INFERENCE_IMGSZ,
            )
            class_counts, boxes = _parse_detections(results)

            with frame_lock:
                current_detections = class_counts
                overlay_boxes = boxes
        finally:
            inference_lock.release()


def generate_frames():
    """Stream MJPEG at STREAM_FPS using the latest frame + most recent detections."""
    encode_params = [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY]

    while True:
        loop_start = time.perf_counter()

        with frame_lock:
            frame = None if latest_frame is None else latest_frame.copy()
            boxes = list(overlay_boxes)

        if frame is not None:
            display = overlay_boxes_on_frame(frame, boxes)
            ok, buffer = cv2.imencode('.jpg', display, encode_params)
            if ok:
                payload = buffer.tobytes()
                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + payload + b'\r\n'
                )

        elapsed = time.perf_counter() - loop_start
        time.sleep(max(0.0, STREAM_INTERVAL - elapsed))


@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame',
    )


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

    results = model(img, conf=0.5, verbose=False)

    class_counts, _ = _parse_detections(results)
    return jsonify(class_counts)


if __name__ == '__main__':
    load_model()

    threading.Thread(target=capture_loop, daemon=True).start()
    threading.Thread(target=inference_loop, daemon=True).start()

    print(
        f"Streaming at {STREAM_FPS if STREAM_FPS > 0 else 'uncapped'} FPS | "
        f"inference imgsz={INFERENCE_IMGSZ} | JPEG quality={JPEG_QUALITY}"
    )
    app.run(host='0.0.0.0', port=5002, debug=False, threaded=True)
