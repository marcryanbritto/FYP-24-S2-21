import React, { useState, useEffect } from 'react';
import '../styles/UpdateFormulaModal.css'; // Ensure this is the correct path

function UpdateFormulaModal({ formula, onSave, onClose, show }) {
    const [newFormula, setNewFormula] = useState('');
    
    useEffect(() => {
        if (show) {
        setNewFormula(formula);
        }
    }, [show, formula]);
    
    const handleSubmit = (e) => {
        e.preventDefault();
        onSave(newFormula);
    };

    // Send to endpoint to update formula

    
    if (!show) return null;
    return (
        <div className="modal">
        <div className="modal-dialog">
            <div className="modal-header">
            <h5 className="modal-title">Update Formula</h5>
            <button className="close-button" onClick={onClose}>&times;</button>
            </div>
            <div className="modal-body">
            <form onSubmit={handleSubmit}>
                <div className="input-group">
                <label htmlFor="formula">Formula</label>
                <textarea
                    id="formula"
                    value={newFormula}
                    className="formula-textarea"
                    onChange={(e) => setNewFormula(e.target.value)}
                    required
                />
                </div>
                <div className="modal-footer">
                <button type="submit" className="save-button">Save</button>
                </div>
            </form>
            </div>
        </div>
        </div>
    );    
}

export default UpdateFormulaModal;