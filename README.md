# 💊 Pill Blister Detector

A full-stack application for detecting individual pills in pharmaceutical blister packs using a YOLOv8 deep learning model and a modern frontend built with Vite + React.

---

## 🚀 Project Overview

This project aims to:
- Train a YOLOv8 model to detect pills in blister packs.
- Provide a RESTful API for image inference using FastAPI.
- Present an intuitive frontend where users can upload images and visualize detected pills.

---

## 🗂️ Project Structure

```bash
pill-blister-detector/
├── backend/      # FastAPI app serving the trained model
├── dataset/      # Images and annotations (if public)
├── frontend/     # Vite + React web interface
├── training/     # YOLOv8 training scripts and configs
├── README.md
├── .gitignore
└── requirements.txt
```
---
# Instala OpenCV
Esto instala la versión principal de OpenCV (cv2) para usar con Python.
```bash
pip install opencv-python
```

---
# Crea tu entorno con Anaconda
1. Ve a: https://www.anaconda.com/products/distribution
2. Descarga e instala Anaconda para Windows (64-bit, Python 3.x)
!!! Durante la instalación:
    ✅Marca la opción "Add Anaconda to my PATH environment variable" si se te ofrece. [Asegurate de que este en tus variables de entorno].
    ✅Instala para ti solamente (recomendado).
3. Abre el menú de inicio → busca Anaconda Prompt → clic derecho → Ejecutar como administrador
4. Crea entorno para YOLOv8
```bash
conda create -n nombre_de_entorno python=3.10 -y
conda activate nombre_de_entorno
```
5. Instala PyTorch con soporte para CUDA
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
```
6. Instala ultralytics
```bash
pip install ultralytics
```
7. Verifica que PyTorch detecte tu GPU
```bash
python -c "import torch; print('CUDA disponible:', torch.cuda.is_available())"
```
8. Cada vez que entrenes abre Anaconda Prompt y activa tu entorno
```bash
conda activate nombre_de_entorno
```
---
# YOLOv8 model
El entrenamiento se realizo con una NVIDIA RTX 4060
---
## Train
```bash
yolo task=detect mode=train model=yolov8m.pt data=data.yaml epochs=100 imgsz=640 batch=16 patience=18
```
!!! LEE CON ATENCIÓN !!!
- model= modelo_a_entrenar (secomienda modelo "nano" o "small". Solo usar modelos "medium" o mayor cuando se tiene gran potencia en ordenador).
- epochs= Veces que el modelo ve todas las imágenes del dataset una vez.
- batch= Es la cantidad de imágenes que el modelo procesa al mismo tiempo antes de actualizar sus pesos.
- patience= Es cuántas épocas seguidas sin mejora en el rendimiento del modelo (en validación) se permiten antes de detener el entrenamiento automáticamente (early stopping).

[TODOS ESTOS PARAMETROS DEPENDERAN DE POTENCIA DE PC, TENER CUIDADO AL ENTRENAR CON PARAMETROS Y MODELOS ALTOS]

---
## Evaluate
Este comando evalúa el rendimiento de tu modelo YOLOv8 entrenado usando el conjunto de validación que definiste en tu archivo data.yaml.
```bash
yolo task=detect mode=val model=runs/detect/blister_model/weights/best.pt data=data.yaml
```