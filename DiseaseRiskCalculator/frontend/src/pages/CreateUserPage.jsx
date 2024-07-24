import React from 'react';
import { useNavigate } from 'react-router-dom';
import CreateUser from '../components/CreateUser.jsx';
import '../styles/CreateUserPage.css'; // Import the CSS file

function CreateUserPage({ onCreateUser }) {
  const navigate = useNavigate();

  const handleCreateUser = (userData) => {
    onCreateUser(userData);
    navigate('/dashboard');
  };

  return (
    <div className="page-container">
      <div className="button-container">
        <button className="back-button" onClick={() => navigate('/dashboard')}>
          Back to Dashboard
        </button>
      </div>
      <CreateUser onCreateUser={handleCreateUser} />
    </div>
  );
}

export default CreateUserPage;
