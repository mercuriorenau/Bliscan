import cv2
from ultralytics import YOLO

# Cargar modelo entrenado
model = YOLO(r'D:\Users\Hackerdude\SCHOOL\pillBlister\Bliscan\backend\runs\detect\bliscan-yolov8m6\weights\best.pt')

# Abrir cámara (puedes poner ruta a un .mp4 también)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

# Nombre de clases según tu .yaml
CLASS_NAMES = ['Empty', 'Full']

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer la cámara.")
        break

    # Realizar predicción con conf=0.57
    results = model(frame, conf=0.57, verbose=False)

    # Obtener clases detectadas
    detections = results[0].boxes
    if detections is not None:
        class_ids = detections.cls.tolist()
    else:
        class_ids = []

    # Contar objetos por clase
    empty_count = class_ids.count(0)
    full_count = class_ids.count(1)

    # Dibujar las detecciones en el frame
    annotated_frame = results[0].plot()

    # Mostrar conteo en la imagen
    cv2.putText(annotated_frame, f'Empty: {empty_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 100), 2)
    cv2.putText(annotated_frame, f'Full: {full_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 100), 2)

    # Mostrar la imagen
    cv2.imshow("Pill Detection - Bliscan", annotated_frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
