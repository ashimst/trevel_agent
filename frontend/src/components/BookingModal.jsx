import { useState } from 'react';
import { X } from 'lucide-react';
import { motion } from 'framer-motion';

export default function BookingModal({ title, details, price, priceUnit, onConfirm, onClose, extraFields }) {
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [extraValues, setExtraValues] = useState({});
  const [error, setError] = useState('');

  const handleConfirm = async () => {
    setLoading(true);
    setError('');
    try {
      await onConfirm({ notes, ...extraValues });
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Booking failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <button className="modal-close" onClick={onClose}><X size={20} /></button>

        <h2 style={{ marginBottom: '0.35rem' }}>Confirm Booking</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '1.5rem' }}>{title}</p>

        {details && details.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1.25rem' }}>
            {details.map((d, i) => (
              <div key={i} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>{d.label}</span>
                <span style={{ fontWeight: 500 }}>{d.value}</span>
              </div>
            ))}
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline',
          padding: '1rem', background: 'var(--accent-muted)', borderRadius: 'var(--radius-md)', marginBottom: '1.25rem' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Total Price</span>
          <span style={{ fontSize: '1.3rem', fontWeight: 700, color: 'var(--accent)' }}>
            ${price}{priceUnit && <span style={{ fontSize: '0.75rem', fontWeight: 400, color: 'var(--text-muted)' }}> {priceUnit}</span>}
          </span>
        </div>

        {extraFields && extraFields.map((field) => (
          <div className="form-group" key={field.name} style={{ marginBottom: '0.75rem' }}>
            <label className="form-label">{field.label}</label>
            <input type={field.type || 'text'} className="input-field"
              value={extraValues[field.name] || ''}
              onChange={(e) => setExtraValues(prev => ({ ...prev, [field.name]: e.target.value }))}
              required={field.required} />
          </div>
        ))}

        <div className="form-group" style={{ marginBottom: '1rem' }}>
          <label className="form-label">Notes (optional)</label>
          <textarea className="input-field" placeholder="Any special requests..."
            value={notes} onChange={(e) => setNotes(e.target.value)} rows={2} />
        </div>

        {error && (
          <div style={{ background: 'var(--error-muted)', color: 'var(--error)', padding: '0.6rem',
            borderRadius: 'var(--radius-sm)', marginBottom: '1rem', fontSize: '0.82rem' }}>
            {error}
          </div>
        )}

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button className="btn" onClick={onClose} style={{ flex: 1 }}>Cancel</button>
          <button className="btn btn-primary" onClick={handleConfirm} disabled={loading} style={{ flex: 1 }}>
            {loading ? 'Booking...' : 'Confirm Booking'}
          </button>
        </div>
      </motion.div>
    </div>
  );
}
