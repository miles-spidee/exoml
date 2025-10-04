import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaKeyboard, FaFileUpload } from 'react-icons/fa';

function InputSelectPage() {
  const navigate = useNavigate();

  return (
    <div className="container text-center">
      <h2>Choose Your Data Source</h2>
      <p>How will you provide the stellar transit data for analysis?</p>
      <div className="card-container">
        <div className="card" onClick={() => navigate('/manual')}>
          <FaKeyboard className="card-icon" />
          <h3>Manual Input</h3>
          <p>Enter parameters for a single celestial object directly.</p>
        </div>
        <div className="card" onClick={() => navigate('/csv')}>
          <FaFileUpload className="card-icon" />
          <h3>Upload CSV</h3>
          <p>Upload a file containing multiple data points for batch processing.</p>
        </div>
      </div>
    </div>
  );
}

export default InputSelectPage;