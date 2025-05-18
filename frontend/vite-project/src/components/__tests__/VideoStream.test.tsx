import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import VideoStream from '../VideoStream';
import '@testing-library/jest-dom';

// Mock de la API de la cámara
const mockStream = new MediaStream();
const mockGetUserMedia = jest.fn().mockResolvedValue(mockStream);

// Mock de fetch
const mockFetch = jest.fn();

// Mock de canvas
const mockToBlob = jest.fn((callback) => callback(new Blob(['test'], { type: 'image/jpeg' })));

describe('VideoStream Integration Tests', () => {
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

  test('should connect to camera on mount', async () => {
    render(<VideoStream />);
    await waitFor(() => {
      expect(mockGetUserMedia).toHaveBeenCalledWith({ video: true });
    });
  });

  test('should handle camera access error', async () => {
    mockGetUserMedia.mockRejectedValueOnce(new Error('Camera access denied'));
    render(<VideoStream />);
    await waitFor(() => {
      expect(screen.getByText('Error accediendo a la cámara')).toBeInTheDocument();
    });
  });

  test('should send image to backend and display detections', async () => {
    // Mock de la respuesta del backend
    const mockDetections = { objects: ['person', 'car'] }; // Verdadermanete manda un json diferente con info de pastillas
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ detections: mockDetections }),
    });

    render(<VideoStream />);
    
    // Simular clic en el botón de detección
    const detectButton = screen.getByText('Detectar');
    fireEvent.click(detectButton);

    // Verificar que se muestra el estado de carga
    expect(screen.getByText('Detectando...')).toBeInTheDocument();

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

  test('should handle backend error', async () => {
    // Mock de error en la respuesta del backend
    mockFetch.mockRejectedValueOnce(new Error('Backend error'));

    render(<VideoStream />);
    
    // Simular clic en el botón de detección
    const detectButton = screen.getByText('Detectar');
    fireEvent.click(detectButton);

    // Verificar que se muestra el mensaje de error
    await waitFor(() => {
      expect(screen.getByText('Error enviando la imagen al backend')).toBeInTheDocument();
    });
  });
}); 