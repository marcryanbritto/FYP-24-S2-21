// src/PatientDashboard.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/PatientDashboard.css';

const PatientDashboard = () => {
  const [inputText, setInputText] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitted text:', inputText);
    // Replace with your submit logic
  };

  const handleLogout = () => {
    console.log('Logout clicked');
    // Replace with your logout logic
    navigate('/'); // Navigate to the login page upon logout
  };

  const handleDeactivateAccount = () => {
    console.log('Deactivate account clicked');
    // Replace with your deactivate account logic
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    console.log('File uploaded:', file);
    // Add your file upload logic here
  };

  return (
    <div className="patient-dashboard">
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <textarea
            value={inputText}
            onChange={handleChange}
            placeholder=""
            required
          />
          <input 
            type="file" 
            onChange={handleFileUpload} 
            className="upload-button" 
          />
        </div>
        <button type="submit" className="dashboard-button">
          Submit
        </button>
      </form>
      <div className="dashboard-footer">
        <button onClick={handleLogout} className="dashboard-button">
          Logout
        </button>
        <button onClick={handleDeactivateAccount} className="dashboard-button">
          Deactivate Account
        </button>
      </div>
    </div>
  );
};

export default PatientDashboard;
