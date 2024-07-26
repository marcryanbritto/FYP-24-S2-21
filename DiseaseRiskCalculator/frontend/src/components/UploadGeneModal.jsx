// src/components/UploadGeneModal.jsx
import React, { useState, useEffect } from 'react';
import '../styles/UploadGeneModal.css'; // Ensure this is the correct path

function UploadGeneModal({ geneId, onSave, onClose, show, token }) {
  const [name, setName] = useState('');
  const [sequence, setSequence] = useState('');
  const [file, setFile] = useState(null);
  const [isFileUpload, setIsFileUpload] = useState(false);

  useEffect(() => {
    if (show && geneId) {
      // Fetch gene data if editing
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
    } else if (!show) {
      // Reset form when modal is closed
      setName('');
      setSequence('');
      setFile(null);
      setIsFileUpload(false);
    }
  }, [show, geneId, token]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('name', name);
    if (isFileUpload && file) {
      formData.append('file', file);
    } else {
      formData.append('sequence', sequence);
    }
    onSave(formData);
  };

  if (!show) return null;

  return (
    <div className="modal">
      <div className="modal-dialog">
        <div className="modal-header">
          <h5 className="modal-title">{geneId ? 'Edit Gene' : 'Upload Gene'}</h5>
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
              <label>
                <input
                  type="radio"
                  checked={!isFileUpload}
                  onChange={() => setIsFileUpload(false)}
                />
                Enter Sequence
              </label>
              <label>
                <input
                  type="radio"
                  checked={isFileUpload}
                  onChange={() => setIsFileUpload(true)}
                />
                Upload File
              </label>
            </div>
            {!isFileUpload && (
              <div className="input-group">
                <label htmlFor="sequence">Sequence</label>
                <textarea
                  id="sequence"
                  value={sequence}
                  onChange={(e) => setSequence(e.target.value)}
                  required
                ></textarea>
              </div>
            )}
            {isFileUpload && (
              <div className="input-group">
                <label htmlFor="file">File</label>
                <input
                  type="file"
                  id="file"
                  onChange={(e) => setFile(e.target.files[0])}
                  required
                />
              </div>
            )}
            <button type="submit" className="save-button">
              {geneId ? 'Save Changes' : 'Upload Gene'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default UploadGeneModal;
