# PARA CORRER PREUBAS:
# python -m pytest test_api.py -v
import pytest
from fastapi.testclient import TestClient
from api import app
import os
import io
from PIL import Image
import numpy as np

client = TestClient(app)

def create_test_image():
    # Crear una imagen de prueba simple
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

def test_detect_endpoint():
    # Crear una imagen de prueba
    test_image = create_test_image()
    
    # Realizar la petición POST al endpoint /detect
    response = client.post(
        "/detect",
        files={"file": ("test_image.jpg", test_image, "image/jpeg")}
    )
    
    # Verificar que la respuesta es exitosa
    assert response.status_code == 200
    
    # Verificar la estructura de la respuesta
    data = response.json()
    assert "detections" in data
    assert "image" in data
    assert isinstance(data["detections"], dict)
    assert isinstance(data["image"], str)

def test_detect_endpoint_invalid_file():
    # Crear un archivo de texto en lugar de una imagen
    test_file = io.BytesIO(b"this is not an image")
    
    # Realizar la petición POST al endpoint /detect
    response = client.post(
        "/detect",
        files={"file": ("test.txt", test_file, "text/plain")}
    )
    
    # Verificar que la respuesta es un error
    assert response.status_code == 422

def test_detect_endpoint_no_file():
    # Realizar la petición POST sin archivo
    response = client.post("/detect")
    
    # Verificar que la respuesta es un error
    assert response.status_code == 422 
