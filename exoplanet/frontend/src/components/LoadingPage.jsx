import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css'; 

function LoadingPage() {
  const navigate = useNavigate();

  useEffect(() => {
    // This effect runs only ONCE when the component mounts.
    const timer = setTimeout(() => {
      // --- AI Prediction Logic (Simulation) ---
      const isExoplanet = Math.random() > 0.5;
      const confidence = Math.random() * (99 - 80) + 80;
      
      // Navigate to the result page after the timer is done
      navigate('/result', {
        replace: true, // This removes the loading page from browser history
        state: { prediction: isExoplanet, confidence: confidence.toFixed(2) }
      });

    }, 3500); // 3.5-second processing time

    // This cleanup function will run if the page is exited prematurely
    return () => clearTimeout(timer);
  }, []); // The empty array [] ensures this effect runs only once.

  return (
    <div className="container text-center">
      <div className="loading-animation">
        <div className="scanner"></div>
        <h2>ANALYZING STELLAR DATA</h2>
        <p>Our AI is processing the light curve and transit parameters... Please wait.</p>
      </div>
    </div>
  );
}

export default LoadingPage;