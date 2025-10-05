import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function ManualInputPage() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    const backendBase = 'http://localhost:3001';

    const probeEndpoints = [
      '/api/health',
      '/health',
      '/api',
      '/'
    ].map(p => `${backendBase}${p}`);

    const probe = async (url) => {
      try {
        const resp = await fetch(url, { method: 'GET' });
        let text = '';
        try { text = await resp.text(); } catch (_) { text = '<no-text>'; }
        return { url, ok: resp.ok, status: resp.status, text: text.substring(0, 1000) };
      } catch (err) {
        return { url, ok: false, status: null, text: err.message };
      }
    };

    try {
      // 1. Create JSON
      const jsonData = {
        "koi_period": parseFloat(formData.koi_period),
        "koi_duration": parseFloat(formData.koi_duration),
        "koi_depth": parseFloat(formData.koi_depth),
        "koi_prad": parseFloat(formData.koi_prad),
        "koi_teq": parseFloat(formData.koi_teq),
        "koi_insol": parseFloat(formData.koi_insol),
        "koi_steff": parseFloat(formData.koi_steff)
      };

      console.log("Submitting data for analysis:", jsonData);

      // 2. Probe backend endpoints and collect diagnostics
      const probeResults = [];
      for (const url of probeEndpoints) {
        const r = await probe(url);
        probeResults.push(r);
        console.log('Probe', r);
        if (r.ok) break; // at least one OK is enough
      }

      const anyOk = probeResults.some(p => p.ok);
      if (!anyOk) {
        // try model-health too (best-effort)
        let modelHealthProbe;
        try {
          modelHealthProbe = await probe(`${backendBase}/api/model-health`);
          probeResults.push(modelHealthProbe);
          console.log('Model-health probe', modelHealthProbe);
        } catch (_) {}
        const summary = probeResults.map(p => `${p.url} -> ok:${p.ok} status:${p.status} text:${p.text.substring(0,200)}`).join('\n\n');
        throw new Error(`Backend health probes failed. Results:\n\n${summary}`);
      }

      // 3. Send predict request
      console.log("Sending prediction request to backend...");
      const response = await fetch(`${backendBase}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(jsonData),
      });

      let result;
      try {
        result = await response.json();
      } catch (jsonError) {
        const text = await response.text().catch(() => '<no-text>');
        throw new Error(`Backend returned non-JSON response (status ${response.status}): ${text.substring(0,1000)}`);
      }

      if (!response.ok) {
        const detail = result && result.error ? result.error : JSON.stringify(result);
        throw new Error(`Backend error (status ${response.status}): ${detail}`);
      }

      if (!result.success) {
        throw new Error(result.error || 'Prediction failed (no error message returned)');
      }

      // 4. Navigate to results
      navigate('/results', { state: { inputData: jsonData, analysisResult: result }});

    } catch (error) {
      console.error('Full error details:', error);
      // show concise actionable message
      alert(`Error analyzing data:\n${error.message}\n\nChecks to run:\n- Is backend running? cd /home/aki/Desktop/Projects/exoml/backend && node server.js\n- Is backend bound to localhost:3001 (not another host/port)?\n- If backend returns 404 on /api/health, restart backend after adding the health endpoint.`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h2 className="text-center">Manual Parameter Input</h2>
      <p className="text-center" style={{ marginBottom: '1.5rem', color: '#aaa' }}>
        Enter the parameters for a stellar object. 
      </p>
      <form onSubmit={handleSubmit} className="input-form">
        <div className="form-group">
          <label>Orbital Period (days) </label>
          <input type="number" name="koi_period" placeholder="e.g., 12.3" value={formData.koi_period} onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Transit Duration (hours) </label>
          <input type="number" name="koi_duration" placeholder="e.g., 5.4" value={formData.koi_duration} onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Transit Depth (ppm) </label>
          <input type="number" name="koi_depth" placeholder="e.g., 250.6" value={formData.koi_depth} onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Planetary Radius (Earth radii) </label>
          <input type="number" name="koi_prad" placeholder="e.g., 4.5" value={formData.koi_prad} onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Equilibrium Temperature (K) </label>
          <input type="number" name="koi_teq" placeholder="e.g., 750" value={formData.koi_teq} onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Insolation Flux (Earth flux) </label>
          <input type="number" name="koi_insol" placeholder="e.g., 88.6" value={formData.koi_insol} onChange={handleChange} required step="any"/>
        </div>
        <div className="form-group">
          <label>Stellar Effective Temp (K) </label>
          <input type="number" name="koi_steff" placeholder="e.g., 5900" value={formData.koi_steff} onChange={handleChange} required step="any"/>
        </div>
        <button type="submit" className="btn btn-primary form-submit-btn" disabled={isLoading}>
          {isLoading ? 'Analyzing...' : 'Analyze & Download Data'}
        </button>
      </form>
    </div>
  );
}

export default ManualInputPage;