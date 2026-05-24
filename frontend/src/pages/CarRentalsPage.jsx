import { useState, useEffect } from 'react';
import { Car, MapPin, Calendar, CheckCircle, XCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { getCarRentals, bookCarRental } from '../api/services.js';
import { useAuth } from '../context/AuthContext.jsx';
import BookingModal from '../components/BookingModal.jsx';
import AuthModal from '../components/AuthModal.jsx';

export default function CarRentalsPage() {
  const { user } = useAuth();
  const [rentals, setRentals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [authModal, setAuthModal] = useState(false);

  useEffect(() => { getCarRentals().then(setRentals).catch(console.error).finally(() => setLoading(false)); }, []);

  const handleBook = (r) => { user ? setSelected(r) : setAuthModal(true); };
  const formatDate = (dt) => new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });

  return (
    <div>
      <div className="page-header"><h1>Car Rentals</h1><p>Rent the perfect vehicle for your journey</p></div>

      {loading ? (
        <div className="page-loading"><div className="spinner" /></div>
      ) : rentals.length === 0 ? (
        <div className="empty-state"><Car /><p>No cars available right now.</p></div>
      ) : (
        <div className="card-grid">
          {rentals.map((r, i) => (
            <motion.div key={r.id} className="service-card" initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <div className="card-header">
                <div>
                  <div className="card-title">{r.vehicle_name}</div>
                  <div className="card-subtitle">{r.vehicle_type} · {r.pickup_location}</div>
                </div>
                <div className="card-price">${r.price_per_day}<span className="card-price-unit">/day</span></div>
              </div>
              <div className="card-details">
                <span className="card-detail"><Calendar size={14} />{formatDate(r.pickup_dt)} – {formatDate(r.dropoff_dt)}</span>
                {r.available ? (
                  <span className="badge badge-available"><CheckCircle size={12} /> Available</span>
                ) : (
                  <span className="badge badge-unavailable"><XCircle size={12} /> Unavailable</span>
                )}
              </div>
              <div className="card-actions">
                <button className="btn btn-primary btn-sm" onClick={() => handleBook(r)}
                  disabled={!r.available}>
                  {r.available ? 'Rent Now' : 'Unavailable'}
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {selected && (
        <BookingModal title={selected.vehicle_name}
          details={[
            { label: 'Type', value: selected.vehicle_type },
            { label: 'Pickup', value: `${selected.pickup_location} — ${formatDate(selected.pickup_dt)}` },
            { label: 'Dropoff', value: formatDate(selected.dropoff_dt) },
          ]}
          price={selected.price_per_day} priceUnit="/day"
          onConfirm={async ({ notes }) => { await bookCarRental(selected.id, notes); setRentals(await getCarRentals()); }}
          onClose={() => setSelected(null)} />
      )}
      {authModal && <AuthModal onClose={() => setAuthModal(false)} />}
    </div>
  );
}
