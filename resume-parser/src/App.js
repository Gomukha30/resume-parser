import React from 'react';
import ResumeUpload from './components/ResumeUpload';
import AllResumes from './components/AllResumes';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <h1>Resume Parser</h1>
      <div className="main-content">
        <ResumeUpload />
        <AllResumes />
      </div>
    </div>
  );
}

export default App;
