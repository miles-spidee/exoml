import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaDatabase, FaBrain, FaGlobeAmericas } from 'react-icons/fa';

function LandingPage() {
  const navigate = useNavigate();

  return (
    // We use a different container class to allow for a wider, more epic layout
    <div className="landing-container">

      {/* Section 1: The Hero */}
      <section className="hero-section text-center">
        <h1 className="hero-title">Become an Exoplanet Hunter</h1>
        <p className="hero-subtitle">
          Thousands of hidden worlds lie dormant in NASA's deep space data. Our AI platform puts the tools of discovery in your hands. Sift through the light of distant stars and join the search for the next Earth.
        </p>
        <button onClick={() => navigate('/select')} className="btn btn-primary pulse" style={{ marginTop: '2rem', transform: 'scale(1.2)' }}>
          Launch Analysis
        </button>
      </section>

      {/* Section 2: How It Works */}
      <section className="features-section">
        <h2 className="text-center">From Data to Discovery in Three Steps</h2>
        <div className="features-grid">
          <div className="feature-card">
            <FaDatabase className="feature-icon" />
            <h3>1. Provide Data</h3>
            <p>Start with stellar transit data. Input parameters for a single object or upload a CSV file with thousands of candidates from NASA missions like Kepler, K2, and TESS.</p>
          </div>
          <div className="feature-card">
            <FaBrain className="feature-icon" />
            <h3>2. AI Analysis</h3>
            <p>Our machine learning model analyzes the subtle dips in starlight—the tell-tale signature of a transiting planet—to distinguish them from stellar noise and other phenomena.</p>
          </div>
          <div className="feature-card">
            <FaGlobeAmericas className="feature-icon" />
            <h3>3. Unveil New Worlds</h3>
            <p>Receive a near-instant classification of your candidate. Your input today could be humanity's next great discovery tomorrow. What will you find?</p>
          </div>
        </div>
      </section>
      
      {/* Section 3: The Impact */}
      <section className="impact-section text-center">
        <h2>Why Your Search Matters</h2>
        <p>
          Every exoplanet we identify brings us one step closer to answering the ultimate question: Are we alone in the universe? By participating in this search, you're not just processing data—you're joining one of the most profound scientific endeavors of our time.
          
        </p>
      </section>

    </div>
  );
}

export default LandingPage;