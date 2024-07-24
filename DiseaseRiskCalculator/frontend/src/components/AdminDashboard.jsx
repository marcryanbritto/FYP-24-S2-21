import React, { useState } from 'react';
import ManageUsers from './ManageUsers';
import AddUserModal from './AddUserModal';
import UserActivityModal from './UserActivityModal';
import '../styles/AdminDashboard.css';

function AdminDashboard() {
  const [showAddUserModal, setShowAddUserModal] = useState(false);
  const [showActivityModal, setShowActivityModal] = useState(false);

  const handleCreateUser = (userData) => {
    // Handle user creation logic
    setShowAddUserModal(false);
  };

  return (
    <div className="admin-dashboard">
      <h2 className="dashboard-title">Admin Dashboard</h2>
      <ul className="dashboard-list">
        <li className="dashboard-item">
          <button className='create-user-button' onClick={() => setShowAddUserModal(true)}>Create New User</button>
        </li>
        <li className="dashboard-item">
          <button className='view-activity-button' onClick={() => setShowActivityModal(true)}>View User Activity</button>
        </li>
      </ul>
      <ManageUsers />
      <AddUserModal
        onSave={handleCreateUser}
        onClose={() => setShowAddUserModal(false)}
        show={showAddUserModal}
      />
      <UserActivityModal
        show={showActivityModal}
        onClose={() => setShowActivityModal(false)}
      />
    </div>
  );
}

export default AdminDashboard;