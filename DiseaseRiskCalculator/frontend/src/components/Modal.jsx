// src/components/Modal.jsx
import React from 'react';
import '../styles/Modal.css'; // Import your CSS file

function Modal({ show, handleClose, children }) {
  if (!show) {
    return null;
  }

  return (
    <div className="modal">
      <div className="modal-content">
        <span className="close" onClick={handleClose}>&times;</span>
        {children}
      </div>
    </div>
  );
}

export default Modal;
