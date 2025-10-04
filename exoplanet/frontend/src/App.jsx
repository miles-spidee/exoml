import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar.jsx';
import Footer from './components/Footer.jsx';
import LandingPage from './components/LandingPage.jsx';
import InputSelectPage from './components/InputSelectPage.jsx';
import ManualInputPage from './components/ManualInputPage.jsx';
import CsvUploadPage from './components/CsvUploadPage.jsx';
import ResultPage from './components/ResultPage.jsx';
import LoadingPage from './components/LoadingPage.jsx';
import './App.css';

// This function programmatically creates our starfield
const generateStars = (numStars) => {
  const stars = [];
  for (let i = 0; i < numStars; i++) {
    const style = {
      top: `${Math.random() * 100}%`,
      // --- THIS LINE IS THE ONLY CHANGE ---
      left: `${Math.random() * 100}%`, // Changed from 50% to 100% for full width
      // ------------------------------------
      animationDuration: `${Math.random() * 5 + 3}s`, // 3s to 8s
      animationDelay: `-${Math.random() * 8}s`,     // Start immediately
    };
    stars.push(<div key={`star-${i}`} className="twinkling-star" style={style}></div>);
  }
  return stars;
};


function App() {
  return (
    <div className="app-grid-container">
      <div className="background-animations">
        <div className="moon"></div>
        <div className="comet"></div>
        <div className="comet"></div>
        <div className="comet"></div>
        <div className="comet"></div>
        <div className="comet"></div>
        
        {/* We now call the function to generate 100 stars */}
        {generateStars(100)}
      </div>

      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/select" element={<InputSelectPage />} />
          <Route path="/manual" element={<ManualInputPage />} />
          <Route path="/csv" element={<CsvUploadPage />} />
          <Route path="/loading" element={<LoadingPage />} />
          <Route path="/result" element={<ResultPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;