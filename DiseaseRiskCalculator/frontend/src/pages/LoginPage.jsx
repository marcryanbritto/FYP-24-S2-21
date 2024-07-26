// src/pages/LoginPage.js
import React, { useState } from 'react';
import Login from '../components/Login';
import Modal from '../components/Modal';
import { useNavigate } from 'react-router-dom';

function LoginPage({ onLogin }) {
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (email, password) => {
    try {
      const response = await fetch('https://165.22.244.125:8000/api/users/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      if (data && data.user) {
        // Save tokens in local storage
        localStorage.setItem('accessToken', data.access);
        localStorage.setItem('refreshToken', data.refresh);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        onLogin(data);
        navigate('/dashboard');
      } else {
        setError('Invalid credentials');
      }
    } catch (error) {
      setError('Invalid credentials or server error');
    }
  };

  const handleCloseModal = () => {
    setError('');
  };

  return (
    <div>
      <Modal show={!!error} handleClose={handleCloseModal}>
        <p>{error}</p>
      </Modal>
      <Login onSubmit={handleLogin} />
    </div>
  );
}

export default LoginPage;
