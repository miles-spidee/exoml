import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function ManualInputPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    orbitalPeriod: '',
    transitDuration: '',
    planetaryRadius: '',
    stellarRadius: '',
    stellarTemp: '',
    transitDepth: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/loading', { state: { formData } });
  };

  return (
    <div className="container">
      <h2 className="text-center">Manual Parameter Input</h2>
      <form onSubmit={handleSubmit} className="input-form">
        <div className="form-group">
          <label>Orbital Period (days)</label>
          <input type="number" name="orbitalPeriod" placeholder="e.g., 365.25" onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Transit Duration (hours)</label>
          <input type="number" name="transitDuration" placeholder="e.g., 5.3" onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Planetary Radius (Earth radii)</label>
          <input type="number" name="planetaryRadius" placeholder="e.g., 1.0" onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Stellar Radius (Solar radii)</label>
          <input type="number" name="stellarRadius" placeholder="e.g., 1.0" onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Stellar Temperature (K)</label>
          <input type="number" name="stellarTemp" placeholder="e.g., 5778" onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Transit Depth (ppm)</label>
          <input type="number" name="transitDepth" placeholder="e.g., 84" onChange={handleChange} required step="any"/>
        </div>
        <button type="submit" className="btn btn-primary form-submit-btn">
            Analyze
        </button>
      </form>
    </div>
  );
}

export default ManualInputPage;