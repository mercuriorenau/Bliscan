import React, { useEffect, useState } from "react";
import { Box, Typography, Paper } from "@mui/material";
import logo from "../assets/logo.png";
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

const BACKEND_URL = "http://localhost:5002";

const fontFamily = `'Montserrat', 'Roboto', 'Arial', sans-serif`;

const Camera = () => {
  const [detections, setDetections] = useState<{Empty?: number; Full?: number}>({ Empty: 0, Full: 0 });

  useEffect(() => {
    const fetchDetections = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}/detections`);
        if (response.ok) {
          const data = await response.json();
          setDetections(data);
        }
      } catch (error) {
        console.error("Error fetching detections:", error);
      }
    };

    fetchDetections();
    const interval = setInterval(fetchDetections, 100);
    return () => clearInterval(interval);
  }, []);

  // Determinar si hay alerta o todo bien
  const isAlert = (detections.Empty ?? 0) > 0;

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 4,
        py: 4,
      }}
    >
      {/* Logo más grande */}
      <Box sx={{ mb: 2, display: "flex", justifyContent: "center" }}>
        <img src={logo} alt="BliScan Logo" style={{ height: 130, objectFit: "contain" }} />
      </Box>
      <img
        src={`${BACKEND_URL}/video_feed`}
        alt="Video Stream"
        style={{
          width: 640,
          height: 480,
          borderRadius: 8,
          border: "1.5px dashed #fff",
          objectFit: "cover",
          background: "#000",
          boxShadow: "0 4px 24px rgba(0,0,0,0.15)",
        }}
      />
      <Paper
        elevation={3}
        sx={{
          p: 3,
          backgroundColor: "rgba(0, 180, 216, 0.1)",
          borderRadius: 2,
          width: "100%",
          maxWidth: 640,
        }}
      >
        {/* Ícono de alerta o todo bien */}
        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 1 }}>
          {isAlert ? (
            <ErrorOutlineIcon sx={{ fontSize: 60, color: '#ff1744' }} />
          ) : (
            <CheckCircleIcon sx={{ fontSize: 60, color: '#00e676' }} />
          )}
        </Box>
        {/* Centrar el texto del título */}
        <Typography 
          variant="h6" 
          color="text.primary" 
          gutterBottom 
          sx={{ textAlign: 'center', fontFamily }}
        >
          Estado del Blister
        </Typography>
        <Box sx={{ display: "flex", justifyContent: "space-around", mt: 2 }}>
          <Box sx={{ textAlign: "center" }}>
            <Typography 
              variant="h3" 
              color="success.main" 
              sx={{ fontWeight: 700, fontFamily }}
            >
              {detections.Full || 0}
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ fontFamily }}>
              Píldoras Detectadas
            </Typography>
          </Box>
          <Box sx={{ textAlign: "center" }}>
            <Typography 
              variant="h3" 
              color="error.main" 
              sx={{ fontWeight: 700, fontFamily }}
            >
              {detections.Empty || 0}
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ fontFamily }}>
              Espacios Vacíos
            </Typography>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default Camera; 