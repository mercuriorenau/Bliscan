import { Box, Container, Typography } from '@mui/material';
import logo from '../assets/logo.png';

const Camera = () => {
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
            justifyContent: 'center',
            alignItems: 'center',
            borderRadius: 2,
            border: '2px dashed #ccc',
          }}
        >
          <Typography variant="body1" color="text.secondary">
            Cámara en desarrollo...
          </Typography>
        </Box>
      </Box>
    </Container>
  );
};

export default Camera; 