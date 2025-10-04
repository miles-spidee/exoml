import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function ManualInputPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    koi_period: '',        // Corresponds to Orbital Period
    koi_duration: '',      // Corresponds to Transit Duration
    koi_depth: '',         // New: Transit Depth
    koi_prad: '',          // Corresponds to Planetary Radius
    koi_teq: '',           // New: Equilibrium Temperature (from image koi_teq)
    koi_insol: '',         // New: Insolation Flux (from image koi_insol)
    koi_steff: '',         // Corresponds to Stellar Temperature
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // 1. Create the JSON object in the exact format from your image
    const jsonData = {
      "koi_period": parseFloat(formData.koi_period),
      "koi_duration": parseFloat(formData.koi_duration),
      "koi_depth": parseFloat(formData.koi_depth),
      "koi_prad": parseFloat(formData.koi_prad),
      "koi_teq": parseFloat(formData.koi_teq),
      "koi_insol": parseFloat(formData.koi_insol),
      "koi_steff": parseFloat(formData.koi_steff)
    };

    // 2. Convert JSON object to a nicely formatted string
    const jsonString = JSON.stringify(jsonData, null, 2);

    // 3. Create a "Blob", which is like a file in memory
    const blob = new Blob([jsonString], { type: 'application/json' });

    // 4. Create a temporary download link and trigger the download
    // NOTE: The browser will save this to your default "Downloads" folder.
    // It is not possible to specify a different folder path from here.
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `exoplanet_data_${Date.now()}.json`; // Unique filename
    document.body.appendChild(a); // Append the link to the body
    a.click(); // Programmatically click the link to start the download
    document.body.removeChild(a); // Clean up by removing the link
    URL.revokeObjectURL(url); // Release the URL resource

    console.log("JSON data prepared and downloaded:", jsonData);

    // 5. After downloading, navigate to the loading page for the AI analysis
    navigate('/loading', { state: { formData: jsonData } });
  };

  return (
    <div className="container">
      <h2 className="text-center">Manual Parameter Input</h2>
      <p className="text-center" style={{ marginBottom: '1.5rem', color: '#aaa' }}>
        Enter the parameters for a stellar object. An AI analysis will follow, and your input will be downloaded as a JSON file.
      </p>
      <form onSubmit={handleSubmit} className="input-form">
        <div className="form-group">
          <label>Orbital Period (days) - `koi_period`</label>
          <input type="number" name="koi_period" placeholder="e.g., 12.3" value={formData.koi_period} onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Transit Duration (hours) - `koi_duration`</label>
          <input type="number" name="koi_duration" placeholder="e.g., 5.4" value={formData.koi_duration} onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Transit Depth (ppm) - `koi_depth`</label>
          <input type="number" name="koi_depth" placeholder="e.g., 250.6" value={formData.koi_depth} onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Planetary Radius (Earth radii) - `koi_prad`</label>
          <input type="number" name="koi_prad" placeholder="e.g., 4.5" value={formData.koi_prad} onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Equilibrium Temperature (K) - `koi_teq`</label>
          <input type="number" name="koi_teq" placeholder="e.g., 750" value={formData.koi_teq} onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Insolation Flux (Earth flux) - `koi_insol`</label>
          <input type="number" name="koi_insol" placeholder="e.g., 88.6" value={formData.koi_insol} onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Stellar Effective Temp (K) - `koi_steff`</label>
          <input type="number" name="koi_steff" placeholder="e.g., 5900" value={formData.koi_steff} onChange={handleChange} required step="any"/>
        </div>
        <button type="submit" className="btn btn-primary form-submit-btn">
            Analyze & Download Data
        </button>
      </form>
    </div>
  );
}

export default ManualInputPage;