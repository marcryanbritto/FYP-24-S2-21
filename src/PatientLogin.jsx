import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/PatientLogin.css";

const PatientLogin = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Login data submitted:", formData);
    navigate("/patient-dashboard");
  };

  return (
    <div className="title-container">
      Disease Risk Calulator
      <div className="login-container-wrapper">
        <div className="login-container">
          <h2>Login</h2>
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
            <div className="button-group">
              <button type="submit">Login</button>
              <div className="button-spacing"></div>
              <button
                type="button"
                onClick={() => navigate("/forgot-password")}
              >
                Forgot Password?
              </button>
              <div className="button-spacing"></div>
              <button type="button" onClick={() => navigate("/create-account")}>
                Create Account
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default PatientLogin;
