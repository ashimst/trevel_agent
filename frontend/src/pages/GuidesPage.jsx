import { useState, useEffect } from 'react';
import { Users, Globe, Calendar, Star } from 'lucide-react';
import { motion } from 'framer-motion';
import { getGuides, bookGuide } from '../api/services.js';
import { useAuth } from '../context/AuthContext.jsx';
import BookingModal from '../components/BookingModal.jsx';
import AuthModal from '../components/AuthModal.jsx';

export default function GuidesPage() {
  const { user } = useAuth();
  const [guides, setGuides] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [authModal, setAuthModal] = useState(false);

  useEffect(() => { getGuides().then(setGuides).catch(console.error).finally(() => setLoading(false)); }, []);

  const handleBook = (g) => { user ? setSelected(g) : setAuthModal(true); };
  const formatDate = (dt) => new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

  return (
    <div>
      <div className="page-header"><h1>Travel Guides</h1><p>Book expert local guides for your trip</p></div>

      {loading ? (
        <div className="page-loading"><div className="spinner" /></div>
      ) : guides.length === 0 ? (
        <div className="empty-state"><Users /><p>No guides available right now.</p></div>
      ) : (
        <div className="card-grid">
          {guides.map((g, i) => (
            <motion.div key={g.id} className="service-card" initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <div className="card-header">
                <div>
                  <div className="card-title">{g.name}</div>
                  <div className="card-subtitle">{g.speciality}</div>
                </div>
                <div className="card-price">${g.daily_rate}<span className="card-price-unit">/day</span></div>
              </div>
              <div className="card-details">
                <span className="card-detail"><Globe size={14} />{g.languages.join(', ')}</span>
                <span className="card-detail"><Calendar size={14} />{formatDate(g.available_from)} – {formatDate(g.available_to)}</span>
              </div>
              {g.bio && <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>{g.bio}</p>}
              <div className="card-actions">
                <button className="btn btn-primary btn-sm" onClick={() => handleBook(g)}>Book Guide</button>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {selected && (
        <BookingModal title={`Guide: ${selected.name}`}
          details={[
            { label: 'Speciality', value: selected.speciality },
            { label: 'Languages', value: selected.languages.join(', ') },
            { label: 'Available', value: `${formatDate(selected.available_from)} – ${formatDate(selected.available_to)}` },
          ]}
          price={selected.daily_rate} priceUnit="/day"
          extraFields={[
            { name: 'booking_from', label: 'Start Date', type: 'datetime-local', required: true },
            { name: 'booking_to', label: 'End Date', type: 'datetime-local', required: true },
          ]}
          onConfirm={async ({ notes, booking_from, booking_to }) => {
            await bookGuide(selected.id, booking_from, booking_to, notes);
            setGuides(await getGuides());
          }}
          onClose={() => setSelected(null)} />
      )}
      {authModal && <AuthModal onClose={() => setAuthModal(false)} />}
    </div>
  );
}
