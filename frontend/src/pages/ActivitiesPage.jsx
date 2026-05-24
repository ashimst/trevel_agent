import { useState, useEffect } from 'react';
import { Sparkles, MapPin, Clock, Users } from 'lucide-react';
import { motion } from 'framer-motion';
import { getActivities, bookActivity } from '../api/services.js';
import { useAuth } from '../context/AuthContext.jsx';
import BookingModal from '../components/BookingModal.jsx';
import AuthModal from '../components/AuthModal.jsx';

export default function ActivitiesPage() {
  const { user } = useAuth();
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [authModal, setAuthModal] = useState(false);

  useEffect(() => { getActivities().then(setActivities).catch(console.error).finally(() => setLoading(false)); }, []);

  const handleBook = (a) => { user ? setSelected(a) : setAuthModal(true); };
  const formatDate = (dt) => new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

  return (
    <div>
      <div className="page-header"><h1>Activities</h1><p>Discover exciting tours and experiences</p></div>

      {loading ? (
        <div className="page-loading"><div className="spinner" /></div>
      ) : activities.length === 0 ? (
        <div className="empty-state"><Sparkles /><p>No activities available right now.</p></div>
      ) : (
        <div className="card-grid">
          {activities.map((a, i) => (
            <motion.div key={a.id} className="service-card" initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <div className="card-header">
                <div>
                  <div className="card-title">{a.name}</div>
                  <div className="card-subtitle">{a.location}</div>
                </div>
                <div className="card-price">${a.price}</div>
              </div>
              <div className="card-details">
                <span className="card-detail"><Clock size={14} />{a.duration_hours}h</span>
                <span className="card-detail"><Users size={14} />{a.max_participants} spots</span>
                <span className="card-detail">{formatDate(a.date)}</span>
              </div>
              <div className="card-actions">
                <button className="btn btn-primary btn-sm" onClick={() => handleBook(a)}
                  disabled={a.max_participants < 1}>
                  {a.max_participants < 1 ? 'Fully Booked' : 'Book Now'}
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {selected && (
        <BookingModal title={selected.name}
          details={[
            { label: 'Location', value: selected.location },
            { label: 'Date', value: formatDate(selected.date) },
            { label: 'Duration', value: `${selected.duration_hours} hours` },
          ]}
          price={selected.price}
          onConfirm={async ({ notes }) => { await bookActivity(selected.id, notes); setActivities(await getActivities()); }}
          onClose={() => setSelected(null)} />
      )}
      {authModal && <AuthModal onClose={() => setAuthModal(false)} />}
    </div>
  );
}
