import React from 'react';

interface VideoStreamProps {
  className?: string;
}

const VideoStream: React.FC<VideoStreamProps> = ({ className }) => {
  return (
    <img
      src="http://localhost:5002/video_feed"
      alt="Video Stream"
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
  );
};

export default VideoStream; 