import React, { useState } from 'react';
import axios from 'axios';
import './ResumeUpload.css';

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [resumeData, setResumeData] = useState(null);
  const [error, setError] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (!selectedFile.type.includes('pdf')) {
        setError('Please select a PDF file');
        setFile(null);
        return;
      }
      setError('');
      setFile(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setIsUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
      const response = await axios.post(`${apiUrl}/upload-resume`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResumeData(response.data);
      setIsUploading(false);
    } catch (err) {
      setError(`Error uploading resume: ${err.message}`);
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Resume</h2>
      <div className="upload-form">
        <input
          type="file"
          onChange={handleFileChange}
          accept=".pdf"
          className="file-input"
          disabled={isUploading}
        />
        <button 
          onClick={handleUpload} 
          className="upload-button"
          disabled={isUploading || !file}
        >
          {isUploading ? 'Uploading...' : 'Upload'}
        </button>
        {error && <div className="error-message">{error}</div>}
      </div>
      {resumeData && (
        <div className="resume-summary">
          <h3>Resume Summary</h3>
          <p><strong>Name:</strong> {resumeData.name}</p>
          <p><strong>Email:</strong> {resumeData.email}</p>
          <p><strong>Phone:</strong> {resumeData.phone}</p>
          <h4>Skills</h4>
          <ul>
            {resumeData.skills.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>
          <h4>Experience</h4>
          <ul>
            {resumeData.experience.map((exp, index) => (
              <li key={index}>{exp}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;
