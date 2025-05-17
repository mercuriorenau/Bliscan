import { Box, Container, Typography, Button, CircularProgress } from '@mui/material';
import { useState } from 'react';
import logo from '../assets/logo.png';

const Camera = () => {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [detectionResult, setDetectionResult] = useState<{ detections: Record<string, number>; image: string } | null>(null);
  const [loading, setLoading] = useState(false);

  const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Display the selected image
    const reader = new FileReader();
    reader.onload = (e) => {
      setSelectedImage(e.target?.result as string);
    };
    reader.readAsDataURL(file);

    // Upload and process the image
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/detect', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error processing image');
      }

      const result = await response.json();
      setDetectionResult({
        detections: result.detections,
        image: `data:image/jpeg;base64,${Buffer.from(result.image).toString('base64')}`,
      });
    } catch (error) {
      console.error('Error:', error);
      alert('Error processing image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 4,
          py: 4,
        }}
      >
        <Box
          component="img"
          src={logo}
          alt="Bliscan Logo"
          sx={{
            width: 'auto',
            height: '100px',
            objectFit: 'contain',
          }}
        />
        
        <Box
          sx={{
            width: '100%',
            maxWidth: 800,
            height: 600,
            backgroundColor: '#f5f5f5',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            borderRadius: 2,
            border: '2px dashed #ccc',
            gap: 2,
            position: 'relative',
          }}
        >
          {loading ? (
            <CircularProgress />
          ) : detectionResult ? (
            <>
              <Box
                component="img"
                src={detectionResult.image}
                alt="Detection Result"
                sx={{
                  maxWidth: '100%',
                  maxHeight: '80%',
                  objectFit: 'contain',
                }}
              />
              <Typography variant="h6">
                Detected Objects:
                {Object.entries(detectionResult.detections).map(([name, count]) => (
                  <Box key={name} sx={{ mt: 1 }}>
                    {name}: {count}
                  </Box>
                ))}
              </Typography>
            </>
          ) : selectedImage ? (
            <Box
              component="img"
              src={selectedImage}
              alt="Selected Image"
              sx={{
                maxWidth: '100%',
                maxHeight: '80%',
                objectFit: 'contain',
              }}
            />
          ) : (
            <Typography variant="body1" color="text.secondary">
              Upload an image to detect objects
            </Typography>
          )}

          <Button
            variant="contained"
            component="label"
            sx={{ mt: 2 }}
          >
            Upload Image
            <input
              type="file"
              hidden
              accept="image/*"
              onChange={handleImageUpload}
            />
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default Camera; 