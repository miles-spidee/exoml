import React from 'react';
import { useNavigate } from 'react-router-dom';

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="container text-center">
      <div className="landing-content">
        <h2>Discover Worlds Beyond Our Own</h2>
        <p>
          Our AI model is trained on public NASA datasets to detect exoplanets using the <strong>transit method</strong>. When a planet passes in front of its star from our point of view, it causes a tiny, periodic dip in the star's brightness. Our AI analyzes this light data to distinguish potential planets from other cosmic phenomena.
        </p>
        [Image of the transit method for exoplanet detection]
        <p>
            Ready to contribute to the search for new worlds? Provide your data and let our AI begin the hunt.
        </p>
      </div>
      <button onClick={() => navigate('/select')} className="btn btn-primary pulse">
        Begin Analysis
      </button>
    </div>
  );
}

export default LandingPage;