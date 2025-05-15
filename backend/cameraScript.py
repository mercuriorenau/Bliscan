import cv2
from ultralytics import YOLO

# Cargar el modelo YOLOv8 preentrenado
model = YOLO('yolov8n.pt')  # Usar el modelo nano preentrenado de YOLOv8

#ID Camara
cap = cv2.VideoCapture(0) 

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer la camara.")
        break

    results = model(frame, verbose=False)

    # Dibujar las detecciones en el cuadro
    annotated_frame = results[0].plot()  # plot() devuelve la imagen con etiquetas

    # Mostrar el cuadro con detecciones
    cv2.imshow("YOLOv8", annotated_frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
