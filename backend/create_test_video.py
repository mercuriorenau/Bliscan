import cv2
import numpy as np

def create_test_video():
    # Configuración del video
    width, height = 640, 480
    fps = 30
    duration = 10  # segundos
    
    # Crear objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('test_video.mp4', fourcc, fps, (width, height))
    
    # Crear frames
    for i in range(fps * duration):
        # Crear frame negro
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Dibujar círculos que se mueven
        x1 = int(width/2 + 100 * np.sin(i/10))
        y1 = int(height/2 + 100 * np.cos(i/10))
        x2 = int(width/2 + 100 * np.sin(i/10 + np.pi))
        y2 = int(height/2 + 100 * np.cos(i/10 + np.pi))
        
        # Dibujar círculos
        cv2.circle(frame, (x1, y1), 30, (0, 255, 0), -1)  # Círculo verde
        cv2.circle(frame, (x2, y2), 30, (0, 0, 255), -1)  # Círculo rojo
        
        # Escribir frame
        out.write(frame)
    
    # Liberar recursos
    out.release()
    print("Video de prueba creado exitosamente.")

if __name__ == '__main__':
    create_test_video() 