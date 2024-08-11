// UserActivityModal.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/UserActivityModal.css';

function UserActivityModal({ show, onClose }) {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (show) {
      fetchUserActivity();
    }
  }, [show]);

  const fetchUserActivity = async () => {
    try {
      const response = await axios.get('https://www.diseaseriskcalculator.com:8000/api/user-activity/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
        }
      });
      setActivities(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch user activity');
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  if (!show) return null;

  return (
    <div className="modal">
      <div className="modal-content">
        <div className="modal-header">
          <h3 className="modal-title">User Activity</h3>
          <button className="close-button" onClick={onClose}>&times;</button>
        </div>
        {loading && <p>Loading...</p>}
        {error && <p>{error}</p>}
        {!loading && !error && (
          <table className="activity-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Action</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {activities.map(activity => (
                <tr key={activity.id}>
                  <td>{activity.user_email}</td>
                  <td>{activity.action}</td>
                  <td>{formatDate(activity.timestamp)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        <button className="close-button" onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

export default UserActivityModal;
