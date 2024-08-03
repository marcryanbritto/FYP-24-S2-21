import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/ManageUsers.css';

function ManageUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      // const response = await axios.get('http://165.22.244.125:8000/api/users/', {
        const response = await axios.get('http://127.0.0.1:8000/api/users/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}` // Assume the token is stored in localStorage
        }
      });
      setUsers(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch users');
      setLoading(false);
    }
  };

  const handleToggleStatus = async (userId) => {
    try {
      const user = users.find(u => u.id === userId);
      const newStatus = !user.is_active;
      
      // await axios.patch(`http://165.22.244.125:8000/api/users/${userId}/`, 
      await axios.patch(`http://127.0.0.1:8000/api/users/${userId}/`, 
        { is_active: newStatus },
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
          }
        }
      );

      setUsers(users.map(u => u.id === userId ? { ...u, is_active: newStatus } : u));
    } catch (err) {
      alert('Failed to update user status');
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="manage-users">
      <h3>Manage Users</h3>
      <div className="user-table-container">
        <table className="user-table">
          <thead>
            <tr>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id}>
                <td>{user.email}</td>
                <td>{user.role}</td>
                <td>{user.is_active ? 'Active' : 'Inactive'}</td>
                <td>
                  <button 
                    className={`user-button ${user.is_active ? 'deactivate-button' : 'activate-button'}`}
                    onClick={() => handleToggleStatus(user.id)}
                  >
                    {user.is_active ? 'Deactivate' : 'Activate'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ManageUsers;
