import '@testing-library/jest-dom';

// Mock de MediaStream
class MockMediaStream {
  active = true;
  id = 'mock-stream-id';
  tracks = [];
}

global.MediaStream = MockMediaStream as any;

// Mock de canvas
const mockContext = {
  drawImage: jest.fn(),
  getImageData: jest.fn(),
  putImageData: jest.fn(),
};

HTMLCanvasElement.prototype.getContext = jest.fn(() => mockContext as any); 