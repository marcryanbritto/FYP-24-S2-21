import React, { useState, useEffect } from 'react';
import '../styles/EditUserModal.css'; // Ensure this is the correct path
import axios from 'axios';

function ViewSimilarityGeneModal({ geneId, onSave, onClose, show, token }) {
  const [name, setName] = useState('');
  const [sequence, setSequence] = useState('');
  const [similarityResults, setSimilarityResults] = useState([]);

  useEffect(() => {
    if (show && geneId) {
      const token = localStorage.getItem('accessToken');
      // Fetch gene data
      fetch(`https://165.22.244.125:8000/api/genes/${geneId}/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          setName(data.name);
          setSequence(data.sequence);
          fetchSimilarityResult(data.id);
        })
        .catch((error) => console.error('Error fetching gene data:', error));
    }
  }, [show, geneId, token]);

  const fetchSimilarityResult = async (id) => {
    const token = localStorage.getItem('accessToken');
    try {
      const response = await axios.post('https://165.22.244.125:8000/api/genes/calculate_similarity/', {
        patient_gene_id: id,
      }, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      setSimilarityResults(response.data); // Assuming response.data is an array of similarity results
    } catch (error) {
      console.error('Error fetching similarity result:', error);
      setSimilarityResults([]);
    }
  };

  if (!show) return null;

  return (
    <div className="modal">
      <div className="modal-dialog">
        <div className="modal-header">
          <h5 className="modal-title">View Gene Results</h5>
          <button className="close-button" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-body">
          {/* Show gene details and the similarity results */}
          <div className='gene-details'>
            <div className='gene-details-title'>Gene Name</div>
            <div className='gene-details-value'>{name}</div>
          </div>
          <div className='gene-details'>
            <div className='gene-details-title'>Gene Sequence</div>
            <div className='gene-details-value'>{sequence}</div>
          </div>
          <div className="similarity-results">
            {similarityResults.length === 0 && <div>No similarity results found</div>}
            {similarityResults.map((result, index) => (
              <div key={index} className='similarity-result'>
                <div className='similarity-result-title'>Similarity Result {index + 1}</div>
                <div className='similarity-result-content'>
                  <div><strong>Gene Name:</strong> {result.gene_name}</div>
                  <div><strong>Similarity:</strong> {result.similarity}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ViewSimilarityGeneModal;
