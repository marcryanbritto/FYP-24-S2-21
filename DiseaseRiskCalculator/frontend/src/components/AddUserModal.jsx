import React, { useState, useEffect } from 'react';
import '../styles/EditUserModal.css'; // Ensure this is the correct path

function AddUserModal({ onSave, onClose, show }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('patient');
  const [active, setActive] = useState(true);
  
  useEffect(() => {
    if (!show) {
      setEmail('');
      setPassword('');
      setRole('patient');
      setActive(true);
    }
  }, [show]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ email, password, role, active });
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
              <label htmlFor="password">Confirm Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
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
    </div>
  );
}

export default AddUserModal;
