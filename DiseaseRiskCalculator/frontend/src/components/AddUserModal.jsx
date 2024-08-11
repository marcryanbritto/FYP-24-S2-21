import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Modal from './Modal';
import '../styles/EditUserModal.css'; // Ensure this is the correct path

function AddUserModal({ onClose, show }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState('patient');
  const [active, setActive] = useState(true);
  const [message, setMessage] = useState('');
  const [showMessageModal, setShowMessageModal] = useState(false);

  useEffect(() => {
    if (!show) {
      setEmail('');
      setPassword('');
      setConfirmPassword('');
      setRole('patient');
      setActive(true);
    }
  }, [show]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setMessage('Passwords do not match');
      setShowMessageModal(true);
      return;
    }

    if (password.length < 8) {
        setMessage('Passwords must be longer than 8 characters');
        setShowMessageModal(true);
        return;
    }

    const userData = { email, password, role };

    try {
      let endpoint;
      if (role === 'patient') {
        endpoint = 'https://www.diseaseriskcalculator.com:8000/api/patient-registration/';
      } else if (role === 'doctor' || role === 'admin') {
        endpoint = 'https://www.diseaseriskcalculator.com:8000/api/users/';
      } else {
        setMessage('Invalid role selected');
        setShowMessageModal(true);
        return;
      }

      await axios.post(endpoint, userData, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
        },
      });

      setMessage('User created successfully');
      setShowMessageModal(true);
    } catch (error) {
      setMessage(`Error creating user: ${error.response ? error.response.data : error.message}`);
      setShowMessageModal(true);
    }
  };

  const closeMessageModal = () => {
    setShowMessageModal(false);
    if (message === 'User created successfully') {
      onClose(); // Close the modal only if the user was created successfully
    }
  };

  if (!show) return null;

  return (
    <div className="modal">
      <div className="modal-dialog">
        <div className="modal-header">
          <h5 className="modal-title">Create User</h5>
          <button className="close-button" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-body">
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
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <label htmlFor="role">Role</label>
              <select
                id="role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              >
                <option value="patient">Patient</option>
                <option value="doctor">Doctor</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div className="checkbox-group">
              <input
                type="checkbox"
                id="active"
                checked={active}
                onChange={(e) => setActive(e.target.checked)}
              />
              <label htmlFor="active">Active</label>
            </div>
            <button type="submit" className="save-button">Create User</button>
          </form>
        </div>
      </div>
      {showMessageModal && (
        <Modal show={showMessageModal} handleClose={closeMessageModal}>
          <p>{message}</p>
        </Modal>
      )}
    </div>
  );
}

export default AddUserModal;
