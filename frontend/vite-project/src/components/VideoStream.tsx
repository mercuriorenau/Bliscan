import React, { useEffect, useRef, useState } from 'react';

interface VideoStreamProps {
  className?: string;
}

const VideoStream: React.FC<VideoStreamProps> = ({ className }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [error, setError] = useState<string | null>(null);
  const [isDetecting, setIsDetecting] = useState(false);
  const [detections, setDetections] = useState<string[]>([]);

  useEffect(() => {
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        setError('Error accediendo a la cámara');
      }
    };

    startCamera();
  }, []);

  const handleDetect = async () => {
    if (!videoRef.current) return;

    setIsDetecting(true);
    setDetections([]);

    try {
      const canvas = document.createElement('canvas');
      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      ctx.drawImage(videoRef.current, 0, 0);
      
      canvas.toBlob(async (blob) => {
        if (!blob) return;

        const formData = new FormData();
        formData.append('image', blob);

        const response = await fetch('http://localhost:5002/detect', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) throw new Error('Error del backend');

        const data = await response.json();
        setDetections(data.detections.objects);
      }, 'image/jpeg');
    } catch (err) {
      setError('Error enviando la imagen al backend');
    } finally {
      setIsDetecting(false);
    }
  };

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <video
        ref={videoRef}
        autoPlay
        playsInline
        className={className}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          borderRadius: '16px',
          boxShadow: '0 4px 24px rgba(0,0,0,0.15)',
          background: '#000',
          display: 'block',
        }}
      />
      <button onClick={handleDetect} disabled={isDetecting}>
        {isDetecting ? 'Detectando...' : 'Detectar'}
      </button>
      {detections.length > 0 && (
        <div>
          <h3>Resultados de la detección:</h3>
          {detections.map((detection, index) => (
            <div key={index}>{detection}</div>
          ))}
        </div>
      )}
    </div>
  );
};

export default VideoStream; 