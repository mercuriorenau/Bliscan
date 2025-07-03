# Run tests with:
# python -m pytest test/test_api.py -v
import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import app
import io
from PIL import Image

client = TestClient(app)

def create_test_image():
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

def test_detect_endpoint():
    test_image = create_test_image()

    response = client.post(
        "/detect",
        files={"file": ("test_image.jpg", test_image, "image/jpeg")}
    )

    assert response.status_code == 200

    data = response.json()
    assert "detections" in data
    assert "image" in data
    assert isinstance(data["detections"], dict)
    assert isinstance(data["image"], str)

def test_detect_endpoint_invalid_file():
    test_file = io.BytesIO(b"this is not an image")

    response = client.post(
        "/detect",
        files={"file": ("test.txt", test_file, "text/plain")}
    )

    assert response.status_code == 422

def test_detect_endpoint_no_file():
    response = client.post("/detect")

    assert response.status_code == 422
