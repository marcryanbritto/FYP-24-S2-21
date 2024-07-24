import React from 'react';
import '../styles/ConfirmationModal.css'; // Add your styles here

function ConfirmationModal({ show, onConfirm, onClose }) {
  if (!show) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>Confirm Deletion</h3>
        <p>Are you sure you want to delete this gene?</p>
        <button onClick={onConfirm} className="delete-button">Delete</button>
        <button onClick={onClose} className="cancel-button">Cancel</button>
      </div>
    </div>
  );
}

export default ConfirmationModal;
