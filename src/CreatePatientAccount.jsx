import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/CreatePatientAccount.css";

const CreatePatientAccount = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const navigate = useNavigate(); // Hook for navigation

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Form data submitted:", formData);
    // Add your form submission logic here

    // Navigate back to the login page
    navigate("/");
  };

  const handleBack = () => {
    console.log("Back clicked");
    // Replace with your back logic, e.g., navigating back to a previous page
    navigate("/"); // Example navigation back to the main dashboard
  };

  return (
    <div className="input-container">
      <h2>Create Account</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username :</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="email">Email :</label>
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
          <label htmlFor="password">Password :</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="confirmPassword">Re-enter Password :</label>
          <input
            type="password"
            id="confirmPassword"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />
        </div>
        <div className="button-container">
          <button type="submit">Create</button>
        </div>
        <button onClick={handleBack} className="dashboard-button">
          Back
        </button>
      </form>
    </div>
  );
};

export default CreatePatientAccount;
