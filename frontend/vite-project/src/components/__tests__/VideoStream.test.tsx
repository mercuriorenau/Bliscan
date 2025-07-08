import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import VideoStream from '../VideoStream';
import '@testing-library/jest-dom';

const mockStream = new MediaStream();
const mockGetUserMedia = jest.fn().mockResolvedValue(mockStream);

const mockFetch = jest.fn();

const mockToBlob = jest.fn((callback) => callback(new Blob(['test'], { type: 'image/jpeg' })));

describe('VideoStream integration tests', () => {
  beforeEach(() => {
    Object.defineProperty(global.navigator, 'mediaDevices', {
      value: {
        getUserMedia: mockGetUserMedia,
      },
      writable: true
    });
    global.fetch = mockFetch as any;
    global.URL.createObjectURL = jest.fn();
    global.URL.revokeObjectURL = jest.fn();

    HTMLCanvasElement.prototype.toBlob = mockToBlob;
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('connects to the camera on mount', async () => {
    await act(async () => {
      render(<VideoStream />);
    });

    await waitFor(() => {
      expect(mockGetUserMedia).toHaveBeenCalledWith({ video: true });
    });
  });

  test('handles camera access errors', async () => {
    mockGetUserMedia.mockRejectedValueOnce(new Error('Camera access denied'));

    await act(async () => {
      render(<VideoStream />);
    });

    await waitFor(() => {
      expect(screen.getByText('Error accessing the camera')).toBeInTheDocument();
    });
  });

  test('sends image to backend and displays detections', async () => {
    const mockDetections = { objects: ['person', 'car'] };
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ detections: mockDetections }),
    });

    await act(async () => {
      render(<VideoStream />);
    });

    const detectButton = screen.getByText('Detect');

    await act(async () => {
      fireEvent.click(detectButton);
    });

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:5002/detect',
        expect.objectContaining({
          method: 'POST',
          body: expect.any(FormData),
        })
      );
    });

    await waitFor(() => {
      expect(screen.getByText('Detection results:')).toBeInTheDocument();
      expect(screen.getByText(/person/)).toBeInTheDocument();
      expect(screen.getByText(/car/)).toBeInTheDocument();
    });
  });
});
