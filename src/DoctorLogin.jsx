import React, { useState } from 'react';
import './styles/DoctorLogin.css';

const DoctorLogin = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form data submitted:', formData); 
  };

  return (
    <div className="doctor-login">
      <h2>Doctor Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
      <div className="additional-options">
        {/* Changed <a> tags to buttons */}
        <button onClick={() => console.log('Forgot Password clicked')}>Forgot Password?</button>
        <span> </span>
        <button onClick={() => console.log('Create Account clicked')}>Create Account</button>
      </div>
    </div>
  );
};

export default DoctorLogin;
