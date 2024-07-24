import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // Import axios
import Modal from '../components/Modal'; // Import the Modal component
import '../styles/RegisterPage.css'; // Import the CSS

function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalMessage, setModalMessage] = useState('');
  const [isSuccess, setIsSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Basic validation
    if (!email || !password || !confirmPassword) {
      setError('Please fill in all fields');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      const response = await axios.post('http://165.22.244.125:8000/api/patient-registration/', {
        email,
        password,
        role: 'patient'
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      setIsSuccess(true);
      setModalMessage('Your registration was successful.');
      setIsModalOpen(true);
      // navigate('/login'); // For example, navigate to login page
    } catch (error) {
      setIsSuccess(false);
      setModalMessage(error.response?.data?.email );
      setIsModalOpen(true);
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <button className="back-button" onClick={() => navigate(-1)}>Back</button>
        <h2 className="register-title">Register</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="confirm-password">Confirm Password</label>
            <input
              type="password"
              id="confirm-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="register-button">Register</button>
        </form>
      </div>
      <Modal
        show={isModalOpen}
        handleClose={handleCloseModal}
      >
        <h2 className={isSuccess ? 'modal-success' : 'modal-error'}>
          {isSuccess ? 'Registration Successful' : 'Registration Failed'}
        </h2>
        <p>{modalMessage}</p>
        <button className="modal-button" onClick={handleCloseModal}>OK</button>
      </Modal>
    </div>
  );
}

export default RegisterPage;
