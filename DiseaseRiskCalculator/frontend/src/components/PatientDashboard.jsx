import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/DoctorDashboard.css'; 
import EditGeneModal from './EditGeneModal';
import UploadGeneModal from './UploadGeneModal';
import ConfirmationModal from './ConfirmationModal'; 
import UpdateFormulaModal from './UpdateFormulaModal'; 
import ViewSimilarityGeneModal from './ViewSimilarityGeneModal';

function PatientDashboard() {
  const [genes, setGenes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showEditGeneModal, setShowEditGeneModal] = useState(false);
  const [selectedGeneId, setSelectedGeneId] = useState(null);
  const [showUploadGeneModal, setShowUploadGeneModal] = useState(false);
  const [showConfirmationModal, setShowConfirmationModal] = useState(false);
  const [geneToDelete, setGeneToDelete] = useState(null);
  const [formula, setFormula] = useState(null);
  const [showUpdateFormulaModal, setShowUpdateFormulaModal] = useState(false);
  const [showViewSimilarityGeneModal, setShowViewSimilarityGeneModal] = useState(false);

  useEffect(() => {
    fetchGenes();
  }, []);

  const fetchGenes = async () => {
    try {
      const response = await axios.get('http://165.22.244.125:8000/api/genes/my_genes/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}` // Assume the token is stored in localStorage
        }
      });
      setGenes(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch genes');
      setLoading(false);
    }
  };

  useEffect(() => {
    const fetchFormula = async () => {
      try {
        const response = await axios.get('http://165.22.244.125:8000/api/formulas/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.data && response.data.length > 0) {
          setFormula(response.data[0].formula);
        } else {
          setFormula('No formula found');
        }
      } catch (error) {
        console.error('Error fetching formula:', error);
        setFormula('Error fetching formula');
      }
    };
    fetchFormula();
  }, []);

  // Refresh access token
  useEffect(() => {
    const refreshAccessToken = async () => {
      try {
        const response = await axios.post('http://165.22.244.125:8000/api/token/refresh/', {
          refresh: localStorage.getItem('refreshToken')
        });
        localStorage.setItem('accessToken', response.data.access);
      } catch (error) {
        console.error('Error refreshing access token:', error);
      }
    };

    refreshAccessToken();
  }
  , []);


  const handleViewGene = (geneId) => {
    setSelectedGeneId(geneId);
    setShowViewSimilarityGeneModal(true);
  }

  const handleEditGene = (geneId) => {
    setSelectedGeneId(geneId);
    setShowEditGeneModal(true);
  };

  const handleSaveGene = async (geneData) => {
    try {
      await axios.post(`http://165.22.244.125:8000/api/genes/edit_gene/`, {
        gene_id: geneData.id,
        name: geneData.name,
        sequence: geneData.sequence,
      },
        {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
        },
      });
      setShowEditGeneModal(false);
      fetchGenes(); // Refresh the gene list
    } catch (error) {
      console.error('Error updating gene:', error);
    }
  };

  const handleUploadGene = async (formData) => {
    try {
      await axios.post('http://165.22.244.125:8000/api/genes/upload/', formData, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          'Content-Type': 'multipart/form-data',
        }
      });
      setShowUploadGeneModal(false);
      fetchGenes(); // Refresh the gene list
    } catch (error) {
      console.error('Error uploading gene:', error);
    }
  };

  const handleDeleteGene = async () => {
    try {
      await axios.delete(`http://165.22.244.125:8000/api/genes/delete_gene/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          'Content-Type': 'application/json',
        },
        data: { gene_id: geneToDelete },
      });
      setShowConfirmationModal(false);
      fetchGenes(); // Refresh the gene list
    } catch (error) {
      console.error('Error deleting gene:', error);
    }
  };

  const handleSaveFormula = async (newFormula) => {
    try {
      await axios.post('http://165.22.244.125:8000/api/formulas/', {
        formula: newFormula,
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          'Content-Type': 'application/json',
        }
      });
      setFormula(newFormula);
      setShowUpdateFormulaModal(false);

    } catch (error) {
      console.error('Error updating formula:', error);
  }
};

  const confirmDelete = (geneId) => {
    setGeneToDelete(geneId);
    setShowConfirmationModal(true);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  return (
    <div className="doctor-dashboard">
      <h2 className="mb-3">Patient Dashboard</h2>
      <button className="upload-btn" onClick={() => setShowUploadGeneModal(true)}>Upload Gene</button>
      
      <h3>Genes Data</h3>
      <div className="genes-table-container">
        <table className="genes-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Sequence</th>
              <th>Date Added</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {genes.map(gene => (
              <tr key={gene.id}>
                <td>{gene.name}</td>
                <td>{gene.sequence}</td>
                <td>{new Date(gene.date_added).toLocaleString()}</td>
                <td>
                  <button
                    className="view-gene-button"
                    onClick={() => handleViewGene(gene.id)}
                  >
                    View
                  </button>
                  <button 
                    className="edit-gene-button" 
                    onClick={() => handleEditGene(gene.id)}
                  >
                    Edit
                  </button>
                  <button 
                    className="delete-button" 
                    onClick={() => confirmDelete(gene.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <EditGeneModal
        geneId={selectedGeneId}
        onSave={handleSaveGene}
        onClose={() => setShowEditGeneModal(false)}
        show={showEditGeneModal}
        token={localStorage.getItem('accessToken')}
      />
      <UploadGeneModal
        onSave={handleUploadGene}
        onClose={() => setShowUploadGeneModal(false)}
        show={showUploadGeneModal}
      />
      <ConfirmationModal
        show={showConfirmationModal}
        onConfirm={handleDeleteGene}
        onClose={() => setShowConfirmationModal(false)}
      />
      <UpdateFormulaModal
        formula={formula}
        onSave={handleSaveFormula}
        onClose={() => setShowUpdateFormulaModal(false)}
        show={showUpdateFormulaModal}
      />
      <ViewSimilarityGeneModal
        geneId={selectedGeneId}
        onClose={() => setShowViewSimilarityGeneModal(false)}
        show={showViewSimilarityGeneModal}
      />
    </div>
  );
}

export default PatientDashboard;
