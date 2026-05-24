import { useState, useEffect } from 'react';
import { Bus, Clock, Armchair } from 'lucide-react';
import { motion } from 'framer-motion';
import { getBuses, bookBus } from '../api/services.js';
import { useAuth } from '../context/AuthContext.jsx';
import BookingModal from '../components/BookingModal.jsx';
import AuthModal from '../components/AuthModal.jsx';

export default function BusesPage() {
  const { user } = useAuth();
  const [buses, setBuses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [authModal, setAuthModal] = useState(false);

  useEffect(() => { getBuses().then(setBuses).catch(console.error).finally(() => setLoading(false)); }, []);

  const handleBook = (b) => { user ? setSelected(b) : setAuthModal(true); };
  const formatDate = (dt) => new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });

  return (
    <div>
      <div className="page-header"><h1>Buses</h1><p>Affordable bus travel options</p></div>

      {loading ? (
        <div className="page-loading"><div className="spinner" /></div>
      ) : buses.length === 0 ? (
        <div className="empty-state"><Bus /><p>No buses available right now.</p></div>
      ) : (
        <div className="card-grid">
          {buses.map((b, i) => (
            <motion.div key={b.id} className="service-card" initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <div className="card-header">
                <div>
                  <div className="card-title">{b.origin} → {b.destination}</div>
                  <div className="card-subtitle">{b.operator} · Seat {b.seat_number}</div>
                </div>
                <div className="card-price">${b.price}</div>
              </div>
              <div className="card-details">
                <span className="card-detail"><Clock size={14} />{formatDate(b.departure_dt)}</span>
                <span className="card-detail"><Armchair size={14} />{b.available_seats} seats</span>
              </div>
              <div className="card-actions">
                <button className="btn btn-primary btn-sm" onClick={() => handleBook(b)}
                  disabled={b.available_seats < 1}>
                  {b.available_seats < 1 ? 'Sold Out' : 'Book Now'}
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {selected && (
        <BookingModal title={`${selected.origin} → ${selected.destination}`}
          details={[
            { label: 'Operator', value: selected.operator },
            { label: 'Seat', value: selected.seat_number },
            { label: 'Departure', value: formatDate(selected.departure_dt) },
          ]}
          price={selected.price}
          onConfirm={async ({ notes }) => { await bookBus(selected.id, notes); setBuses(await getBuses()); }}
          onClose={() => setSelected(null)} />
      )}
      {authModal && <AuthModal onClose={() => setAuthModal(false)} />}
    </div>
  );
}
