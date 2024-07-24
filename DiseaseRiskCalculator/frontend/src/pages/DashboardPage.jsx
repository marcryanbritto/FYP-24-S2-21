import React from 'react';
import '../styles/DashboardPage.css'; // Import your CSS file

function DashboardPage({ user, onLogout, children }) {
  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Welcome to your Dashboard, {user.email}</h1>
      <button className="logout-button" onClick={onLogout}>Logout</button>
      <div className="card">
        <div className="card-body">
          {children}
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;
