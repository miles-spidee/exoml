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

function App() {
  return (
    <div className="app-grid-container">
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