import cv2
from ultralytics import YOLO

# Ruta al modelo entrenado
model = YOLO('D:/Users/Hackerdude/SCHOOL/pillBlister/Bliscan/backend/runs/detect/bliscan-yolov8m6/weights/best.pt')


# Inicializar cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer la cámara.")
        break

    # Realizar predicción
    results = model(frame, conf=0.5, verbose=False)

    # Dibujar las predicciones en el frame
    annotated_frame = results[0].plot()

    # Mostrar el frame
    cv2.imshow("Detección de pastillas - Bliscan", annotated_frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()