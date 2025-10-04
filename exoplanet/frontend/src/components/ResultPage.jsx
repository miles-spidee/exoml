import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { FaCheckCircle, FaTimesCircle } from 'react-icons/fa';

function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  // Provide default values to prevent errors if state is missing
  const { prediction, confidence } = location.state || { prediction: false, confidence: 0 };

  const resultText = prediction ? "Potential Exoplanet Detected" : "Candidate Unlikely to be Exoplanet";
  const resultClass = prediction ? "result-positive" : "result-negative";
  const ResultIcon = prediction ? FaCheckCircle : FaTimesCircle;

  return (
    <div className="container text-center">
      <h2>Analysis Complete</h2>
      <div className={`result-display ${resultClass}`}>
        <ResultIcon className="result-icon" />
        <h3>{resultText}</h3>
        {confidence > 0 && (
            <p className="confidence-score">
                AI Confidence: <span>{confidence}%</span>
            </p>
        )}
      </div>
      <button onClick={() => navigate('/select')} className="btn">
        Run New Analysis
      </button>
    </div>
  );
}

export default ResultPage;