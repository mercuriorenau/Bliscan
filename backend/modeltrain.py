from ultralytics import YOLO
import torch

def main():
    # Verifica CUDA
    print("🚀 Verificando CUDA...")
    if torch.cuda.is_available():
        print(f"✅ CUDA disponible: {torch.cuda.get_device_name(0)}")
    else:
        print("❌ CUDA no disponible. Se usará CPU")

    # Ruta al dataset
    DATASET_PATH = "E:/DataSet/DrugDetectMerge1234.v1i.yolov8/data.yaml"

    # Carga el modelo base
    model = YOLO("yolov8s.pt")

    # Entrenamiento
    model.train(
        data=DATASET_PATH,
        epochs=50,
        imgsz=640,
        batch=16,
        patience=15,
        name="bliscan-yolov8m"
    )

# Protege el entrypoint para evitar errores en Windows
if __name__ == "__main__":
    main()
