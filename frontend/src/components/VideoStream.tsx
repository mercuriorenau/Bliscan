import React, { useEffect, useRef, useState } from 'react';

const VideoStream: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [detections, setDetections] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Solicita acceso a la cámara web
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch((err) => {
        setError('Error accediendo a la cámara');
        console.error('Error accediendo a la cámara:', err);
      });
  }, []);

  const handleDetect = async () => {
    setLoading(true);
    setError(null);
    setDetections(null);
    if (!videoRef.current || !canvasRef.current) return;
    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(async (blob) => {
      if (!blob) return;
      const formData = new FormData();
      formData.append('file', blob, 'capture.jpg');
      try {
        const response = await fetch('http://localhost:5002/detect', {
          method: 'POST',
          body: formData,
        });
        if (!response.ok) throw new Error('Error en la detección');
        const data = await response.json();
        setDetections(data.detections);
      } catch (err) {
        setError('Error enviando la imagen al backend');
      } finally {
        setLoading(false);
      }
    }, 'image/jpeg');
  };

  return (
    <div className="video-container">
      <video
        ref={videoRef}
        autoPlay
        playsInline
        style={{ width: '100%', maxWidth: '800px' }}
      />
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      <button onClick={handleDetect} disabled={loading} style={{ marginTop: 16 }}>
        {loading ? 'Detectando...' : 'Detectar'}
      </button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {detections && (
        <div style={{ marginTop: 16 }}>
          <h3>Resultados de la detección:</h3>
          <pre>{JSON.stringify(detections, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default VideoStream; 