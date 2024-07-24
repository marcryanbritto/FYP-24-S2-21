import React, { useState, useEffect } from 'react';
import '../styles/EditUserModal.css'; // Import your CSS file

function EditUserModal({ user, onSave, onClose }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('');
  const [active, setActive] = useState(false);

  useEffect(() => {
    if (user) {
      setEmail(user.email);
      setPassword('');
      setRole(user.role);
      setActive(user.active);
    }
  }, [user]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      id: user.id,
      email,
      password: password || undefined,
      role,
      active,
    });
  };

  return (
    <div className="modal" style={{ display: 'block', backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Edit User</h5>
            <button type="button" className="close-button" onClick={onClose}>X</button>
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
                <label htmlFor="password">Password (leave blank to keep current)</label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              <div className="input-group">
                <label htmlFor="role">Role</label>
                <select
                  id="role"
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  required
                >
                  <option value="admin">Admin</option>
                  <option value="doctor">Doctor</option>
                  <option value="patient">Patient</option>
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
              <button type="submit" className="save-button">Save changes</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default EditUserModal;
