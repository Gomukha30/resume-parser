import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AllResumes = () => {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      const response = await axios.get('http://localhost:8000/resumes');
      setResumes(response.data);
      setLoading(false);
    } catch (err) {
      setError('Error fetching resumes: ' + err.message);
      setLoading(false);
    }
  };

  return (
    <div className="all-resumes">
      <h2>All Resumes</h2>
      {loading && <div>Loading...</div>}
      {error && <div className="error-message">{error}</div>}
      {!loading && !error && (
        <div className="resumes-list">
          {resumes.map((resume, index) => (
            <div key={index} className="resume-card">
              <h3>{resume.name}</h3>
              <p><strong>Email:</strong> {resume.email}</p>
              <p><strong>Phone:</strong> {resume.phone}</p>
              <h4>Skills</h4>
              <ul>
                {resume.skills.map((skill, index) => (
                  <li key={index}>{skill}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AllResumes;
