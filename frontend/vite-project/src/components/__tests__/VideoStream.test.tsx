import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import VideoStream from '../VideoStream';
import '@testing-library/jest-dom';

// Mock de la API de la cámara
const mockStream = new MediaStream();
const mockGetUserMedia = jest.fn().mockResolvedValue(mockStream);

// Mock de fetch
const mockFetch = jest.fn();

// Mock de canvas
const mockToBlob = jest.fn((callback) => callback(new Blob(['test'], { type: 'image/jpeg' })));

describe('Pruebas de integración de VideoStream', () => {
  beforeEach(() => {
    // Configurar los mocks
    Object.defineProperty(global.navigator, 'mediaDevices', {
      value: {
        getUserMedia: mockGetUserMedia,
      },
      writable: true
    });
    global.fetch = mockFetch as any;
    global.URL.createObjectURL = jest.fn();
    global.URL.revokeObjectURL = jest.fn();

    // Mock del canvas
    HTMLCanvasElement.prototype.toBlob = mockToBlob;
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('debe conectarse a la cámara al iniciar', async () => {
    await act(async () => {
      render(<VideoStream />);
    });
    
    await waitFor(() => {
      expect(mockGetUserMedia).toHaveBeenCalledWith({ video: true });
    });
  });

  test('debe manejar el error de acceso a la cámara', async () => {
    mockGetUserMedia.mockRejectedValueOnce(new Error('Acceso a la cámara denegado'));
    
    await act(async () => {
      render(<VideoStream />);
    });

    await waitFor(() => {
      expect(screen.getByText('Error accediendo a la cámara')).toBeInTheDocument();
    });
  });

  test('debe enviar imagen al backend y mostrar detecciones', async () => {
    // Mock de la respuesta del backend
    const mockDetections = { objects: ['person', 'car'] };
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ detections: mockDetections }),
    });

    await act(async () => {
      render(<VideoStream />);
    });
    
    // Simular clic en el botón de detección
    const detectButton = screen.getByText('Detectar');
    
    await act(async () => {
      fireEvent.click(detectButton);
    });

    // Verificar que se hizo la petición al backend
    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:5002/detect',
        expect.objectContaining({
          method: 'POST',
          body: expect.any(FormData),
        })
      );
    });

    // Verificar que se muestran las detecciones
    await waitFor(() => {
      expect(screen.getByText('Resultados de la detección:')).toBeInTheDocument();
      expect(screen.getByText(/person/)).toBeInTheDocument();
      expect(screen.getByText(/car/)).toBeInTheDocument();
    });
  });
}); 