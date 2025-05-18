from ultralytics import YOLO
import torch

def main():
    print("Checking CUDA...")
    if torch.cuda.is_available():
        print(f"CUDA available: {torch.cuda.get_device_name(0)}")
    else:
        print("CUDA not available. Using CPU.")

    DATASET_PATH = "E:/DataSet/DrugDetectMerge1234.v1i.yolov8/data.yaml"

    model = YOLO("yolov8s.pt")

    model.train(
        data=DATASET_PATH,
        epochs=50,
        imgsz=640,
        batch=16,
        patience=15,
        name="bliscan-yolov8m"
    )

if __name__ == "__main__":
    main()
