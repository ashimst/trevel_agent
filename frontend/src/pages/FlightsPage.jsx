import { useState, useEffect } from 'react';
import { Plane, MapPin, Clock, DollarSign, Armchair } from 'lucide-react';
import { motion } from 'framer-motion';
import { getFlights, bookFlight } from '../api/services.js';
import { useAuth } from '../context/AuthContext.jsx';
import BookingModal from '../components/BookingModal.jsx';
import AuthModal from '../components/AuthModal.jsx';

export default function FlightsPage() {
  const { user } = useAuth();
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [authModal, setAuthModal] = useState(false);

  useEffect(() => { getFlights().then(setFlights).catch(console.error).finally(() => setLoading(false)); }, []);

  const handleBook = (flight) => { user ? setSelected(flight) : setAuthModal(true); };

  const formatDate = (dt) => new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' });

  return (
    <div>
      <div className="page-header">
        <h1>Flights</h1>
        <p>Browse available flights and book your next journey</p>
      </div>

      {loading ? (
        <div className="page-loading"><div className="spinner" /></div>
      ) : flights.length === 0 ? (
        <div className="empty-state"><Plane /><p>No flights available right now.</p></div>
      ) : (
        <div className="card-grid">
          {flights.map((f, i) => (
            <motion.div key={f.id} className="service-card" initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <div className="card-header">
                <div>
                  <div className="card-title">{f.origin} → {f.destination}</div>
                  <div className="card-subtitle">{f.airline} · {f.seat_class}</div>
                </div>
                <div className="card-price">${f.price}</div>
              </div>
              <div className="card-details">
                <span className="card-detail"><Clock size={14} />{formatDate(f.departure_dt)}</span>
                <span className="card-detail"><Armchair size={14} />{f.available_seats} seats</span>
              </div>
              <div className="card-actions">
                <button className="btn btn-primary btn-sm" onClick={() => handleBook(f)}
                  disabled={f.available_seats < 1}>
                  {f.available_seats < 1 ? 'Sold Out' : 'Book Now'}
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {selected && (
        <BookingModal title={`${selected.origin} → ${selected.destination}`}
          details={[
            { label: 'Airline', value: selected.airline },
            { label: 'Class', value: selected.seat_class },
            { label: 'Departure', value: formatDate(selected.departure_dt) },
          ]}
          price={selected.price}
          onConfirm={async ({ notes }) => { await bookFlight(selected.id, notes); setFlights(await getFlights()); }}
          onClose={() => setSelected(null)} />
      )}
      {authModal && <AuthModal onClose={() => setAuthModal(false)} />}
    </div>
  );
}
