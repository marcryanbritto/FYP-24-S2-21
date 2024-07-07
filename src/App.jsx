import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PatientLogin from "./PatientLogin";
import CreatePatientAccount from "./CreatePatientAccount";
import PatientDashboard from "./PatientDashboard";
import DoctorInputGenes from "./DoctorInputGenes";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<PatientLogin />} />
        <Route path="/create-account" element={<CreatePatientAccount />} />
        <Route path="/patient-dashboard" element={<PatientDashboard />} />
        <Route path="/doctor-input-genes" element={<DoctorInputGenes />} />
      </Routes>
    </Router>
  );
};

export default App;
