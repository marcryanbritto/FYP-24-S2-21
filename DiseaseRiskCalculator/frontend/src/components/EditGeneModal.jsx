import React, { useState, useEffect } from 'react';
import '../styles/EditUserModal.css'; // Ensure this is the correct path

function EditGeneModal({ geneId, onSave, onClose, show, token }) {
  const [name, setName] = useState('');
  const [sequence, setSequence] = useState('');

  useEffect(() => {
    if (show && geneId) {
      // Fetch gene data
      const token = localStorage.getItem('accessToken');
      fetch(`https://165.22.244.125:8000/api/genes/${geneId}/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          setName(data.name);
          setSequence(data.sequence);
        })
        .catch((error) => console.error('Error fetching gene data:', error));
    }
  }, [show, geneId, token]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ id: geneId, name, sequence });
  };

  if (!show) return null;

  return (
    <div className="modal">
      <div className="modal-dialog">
        <div className="modal-header">
          <h5 className="modal-title">Edit Gene</h5>
          <button className="close-button" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-body">
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label htmlFor="name">Name</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <label htmlFor="sequence">Sequence</label>
              <textarea
                id="sequence"
                value={sequence}
                onChange={(e) => setSequence(e.target.value)}
                required
              ></textarea>
            </div>
            <button type="submit" className="save-button">Save Changes</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default EditGeneModal;
