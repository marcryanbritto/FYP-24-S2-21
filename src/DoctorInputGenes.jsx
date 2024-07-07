import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/DoctorInputGenes.css";

const DoctorInputGenes = () => {
  const [inputText, setInputText] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Submitted text:", inputText);
    // Replace with your submit logic for gene discoveries
  };

  const handleBack = () => {
    console.log("Back clicked");
    // Replace with your back logic, e.g., navigating back to a previous page
    navigate("/"); // Example navigation back to the main dashboard
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    console.log("File uploaded:", file);
    // Add your file upload logic here
  };

  return (
    <div className="doctor-dashboard">
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <textarea
            value={inputText}
            onChange={handleChange}
            placeholder="Input gene discoveries here..."
            required
          />
          <input
            type="file"
            onChange={handleFileUpload}
            className="upload-button"
          />
        </div>
        <div className="dashboard-footer">
          <button onClick={handleBack} className="dashboard-button">
            Back
          </button>
          <button type="submit" className="dashboard-button">
            Submit
          </button>
        </div>
      </form>
    </div>
  );
};

export default DoctorInputGenes;
