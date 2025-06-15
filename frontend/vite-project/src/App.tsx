import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import Home from './pages/Home';
import Camera from './pages/Camera';

const theme = createTheme({
  palette: {
    primary: {
      main: '#00B4D8',
    },
    background: {
      default: '#071725',
      paper: '#071725',
    },
    text: {
      primary: '#ffffff',
      secondary: '#E2E8F0',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          backgroundColor: '#0085d7',
          '&:hover': {
            backgroundColor: '#098fd5',
          },
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/camera" element={<Camera />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
