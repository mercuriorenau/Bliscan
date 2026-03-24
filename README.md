<p align="center">
  <img src="README-banner.png" alt="Bliscan" width="720" />
</p>

# Bliscan

Full-stack computer vision system for detecting pills and empty cells in pharmaceutical blister packs. It combines a **YOLOv8** detector trained on custom data with a **Flask** service for live webcam inference, a **FastAPI** API for image uploads, and a **React + Vite** operator interface.

---

## Model performance (validation)

Metrics below correspond to the **final epoch (50)** of the training run recorded under `backend/model/bliscan-yolov8m6/` (Ultralytics validation split).

| Metric | Value |
|--------|-------|
| mAP@0.5 | 96.29% |
| mAP@0.5:0.95 | 78.06% |
| Precision | 98.95% |
| Recall | 93.95% |

**Training configuration (reference):** YOLOv8s, image size 640, batch 16, up to 50 epochs, early stopping patience 15, mixed precision (AMP). Hardware used for that run: NVIDIA RTX 4060.

![Training curves](backend/model/bliscan-yolov8m6/results.png)

---

## What this repository contains

- **Live inspection:** `backend/cameraScript2.py` serves MJPEG video, detection counts, and optional file upload on port **5002** (Flask).
- **REST inference:** `backend/api.py` exposes `POST /detect` for image upload and returns per-class counts plus a base64-annotated frame (FastAPI + Uvicorn).
- **Web UI:** `frontend/vite-project` is a React application that talks to the Flask backend for the camera workflow.

---

## Tech stack

| Layer | Technologies |
|-------|----------------|
| Model | PyTorch, Ultralytics YOLOv8, OpenCV |
| Live backend | Flask, Flask-CORS, threading |
| API | FastAPI, python-multipart, Uvicorn |
| Frontend | React, TypeScript, Vite, Material UI |

---

## Prerequisites

- Python 3.10+ (3.13 works with current dependencies; use a virtual environment).
- Node.js 18+ for the frontend.
- Webcam access for the live demo (`cameraScript2.py`).
- Trained weights at `backend/model/modelin.pt` (included in this repo).

**Note:** PyTorch 2.6+ defaults to safe tensor loading; this project patches `torch.load` where needed so trusted YOLO checkpoints load correctly (see `api.py` and `cameraScript2.py`).

---

## Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run live server (Flask, port 5002)

```bash
python cameraScript2.py
```

### Run REST API (FastAPI)

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

---

## Frontend setup

```bash
cd frontend/vite-project
npm install
npm run dev
```

Open the URL printed by Vite (typically `http://localhost:5173`). The camera page expects the Flask backend at `http://localhost:5002`.

---

## Training and evaluation (YOLO CLI)

Use your own `data.yaml` pointing to train/val images and labels. Example train command (adjust paths and hyperparameters to your hardware):

```bash
yolo task=detect mode=train model=yolov8s.pt data=path/to/data.yaml epochs=50 imgsz=640 batch=16 patience=15
```

Validate a checkpoint:

```bash
yolo task=detect mode=val model=path/to/best.pt data=path/to/data.yaml
```

---

## Project structure

```text
Bliscan/
├── backend/
│   ├── api.py                 # FastAPI inference API
│   ├── cameraScript2.py       # Flask live stream + detections
│   ├── requirements.txt
│   ├── model/
│   │   ├── modelin.pt         # Served weights
│   │   └── bliscan-yolov8m6/  # Training logs, curves, results.csv
│   └── test/
├── frontend/
│   └── vite-project/          # React UI
├── README-banner.png          # Hero image (add your banner here if missing)
└── README.md
```

Place your banner image at the repository root as **`README-banner.png`** so the header renders on GitHub. If the file is not present, add it or update the `src` in the HTML block at the top of this file.

---

## License

Add a license file if you distribute this project publicly.
