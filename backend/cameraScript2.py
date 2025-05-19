import cv2
from ultralytics import YOLO
import tkinter as tk

# Obtener resolución de pantalla con tkinter
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

# Cargar modelo entrenado
model = YOLO(r"C:\Users\tokad\OneDrive\Escritorio\Bliscan\best.pt")

# Abrir cámara
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

# Nombre de clases según tu .yaml
CLASS_NAMES = ['Empty', 'Full']

# Crear ventana en modo pantalla completa
window_name = "Pill Detection - Bliscan"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer la cámara.")
        break

    # Realizar predicción con conf=0.57
    results = model(frame, conf=0.57, verbose=False)

    # Obtener clases detectadas
    detections = results[0].boxes
    class_ids = detections.cls.tolist() if detections is not None else []

    # Contar objetos por clase
    empty_count = class_ids.count(0)
    full_count = class_ids.count(1)

    # Dibujar las detecciones en el frame
    annotated_frame = results[0].plot()

    # Mostrar conteo en la imagen
    cv2.putText(annotated_frame, f'Empty: {empty_count}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 100), 2)
    cv2.putText(annotated_frame, f'Full: {full_count}', (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 100), 2)

    # Redimensionar a pantalla completa
    annotated_frame = cv2.resize(annotated_frame, (screen_width, screen_height))

    # Mostrar la imagen
    cv2.imshow(window_name, annotated_frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
