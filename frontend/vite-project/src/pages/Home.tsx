import { Box, Button, Container, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png';

const Home = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          textAlign: 'center',
          gap: 5,
          color: 'text.primary',
        }}
      >
        <Box
          component="img"
          src={logo}
          alt="Bliscan Logo"
          sx={{
            width: 'auto',
            height: '300px',
            objectFit: 'contain',
          }}
        />
        <Typography variant="h5" component="h2" gutterBottom color="text.primary">
          Detección Inteligente de Pastillas
        </Typography>
        <Typography variant="body1" paragraph color="text.secondary">
          Bliscan es una solución innovadora que utiliza tecnología de visión por computadora
          para detectar automáticamente pastillas faltantes en blisters, asegurando la
          integridad de los medicamentos y mejorando la calidad del control de calidad.
        </Typography>
        <Button
          variant="contained"
          size="large"
          onClick={() => navigate('/camera')}
          sx={{ 
            mt: 2,
            color: '#ffffff',
            fontWeight: 'bold',
          }}
        >
          Iniciar Detección
        </Button>
      </Box>
    </Container>
  );
};

export default Home; 