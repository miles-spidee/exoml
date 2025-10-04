import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaFileUpload } from 'react-icons/fa';

function CsvUploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('No file chosen');

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0]);
      setFileName(e.target.files[0].name);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!file) {
      alert('Please upload a CSV file first.');
      return;
    }
    navigate('/loading', { state: { fileInfo: { name: file.name, size: file.size } } });
  };

  return (
    <div className="container text-center">
      <h2>Upload CSV File</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="csv-upload" className="file-upload-wrapper">
          <FaFileUpload className="card-icon" />
          <span>Click to browse or drag & drop your file here</span>
          <span className="file-name">{fileName}</span>
          <input type="file" id="csv-upload" accept=".csv" onChange={handleFileChange} hidden />
        </label>
        <button type="submit" className="btn btn-primary" style={{ marginTop: '20px' }}>
            Analyze Data
        </button>
      </form>
    </div>
  );
}

export default CsvUploadPage;