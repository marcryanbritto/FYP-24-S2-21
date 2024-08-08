// src/App.js

import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import AdminDashboard from './components/AdminDashboard';
import DoctorDashboard from './components/DoctorDashboard';
import PatientDashboard from './components/PatientDashboard';
import LoginPage from './pages/LoginPage';
import CreateUserPage from './pages/CreateUserPage';
import RegisterPage from './pages/RegisterPage';
import { addUser } from './utils/fakeUsers';

function App() {
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')));

  const handleLogin = (userData) => {
    if (userData && userData.user.is_active) {
      setUser(userData.user);
    } else {
      // alert('asw');
      alert('Invalid credentials or user is not active');
    }
  };
  const handleLogout = async () => {
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');
    try {
      const response = await fetch('http://localhost:8000/api/users/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`, // Use the access token from local storage
        },
        body: JSON.stringify({ refresh: refreshToken }),
      });


      // Assuming the API response doesn't have any additional data you need
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
      setUser(null);
    } catch (error) {
      alert('Logout failed');
      console.error('Logout error:', error);
    }
  };

  const handleCreateUser = (userData) => {
    try {
      addUser(userData);
      alert('User created successfully!');
    } catch (error) {
      alert(error.message);
    }
  };

  // Protected route component
  const ProtectedRoute = ({ children }) => {
    if (!user || user.role !== 'admin') {
      return <Navigate to="/dashboard" />;
    }
    return children;
  };

  return (
    <Router>
      <Routes>
        <Route path="/login" element={
          user ? <Navigate to="/dashboard" /> : <LoginPage onLogin={handleLogin} />
        } />
        <Route path="/register" element={
          user ? <Navigate to="/dashboard" /> : <RegisterPage />
        } />
        <Route path="/dashboard" element={
          user ? (
            <DashboardPage user={user} onLogout={handleLogout}>
              {user.role === 'admin' && <AdminDashboard />}
              {user.role === 'doctor' && <DoctorDashboard />}
              {user.role === 'patient' && <PatientDashboard />}
            </DashboardPage>
          ) : (
            <Navigate to="/login" />
          )
        } />
        <Route path="/admin/create-user" element={
          <ProtectedRoute>
            <CreateUserPage onCreateUser={handleCreateUser} />
          </ProtectedRoute>
        } />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
