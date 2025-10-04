import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FaHome, FaArrowLeft } from 'react-icons/fa';

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

  // We don't show the back button on the home page
  const showBackButton = location.pathname !== '/';

  return (
    <nav className="navbar">
      <div className="navbar-left">
        {showBackButton && (
          <button onClick={() => navigate(-1)} className="nav-btn">
            <FaArrowLeft />
            <span>Back</span>
          </button>
        )}
      </div>
      <div className="navbar-center">
        <h1 className="navbar-title">EXOPLANET HUNTER AI</h1>
      </div>
      <div className="navbar-right">
        <button onClick={() => navigate('/')} className="nav-btn">
          <FaHome />
          <span>Home</span>
        </button>
      </div>
    </nav>
  );
}

export default Navbar;