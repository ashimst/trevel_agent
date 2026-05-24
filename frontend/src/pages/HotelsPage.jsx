import { useState, useEffect } from 'react';
import { Hotel, MapPin, Calendar, BedDouble } from 'lucide-react';
import { motion } from 'framer-motion';
import { getHotels, bookHotel } from '../api/services.js';
import { useAuth } from '../context/AuthContext.jsx';
import BookingModal from '../components/BookingModal.jsx';
import AuthModal from '../components/AuthModal.jsx';

export default function HotelsPage() {
  const { user } = useAuth();
  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [authModal, setAuthModal] = useState(false);

  useEffect(() => { getHotels().then(setHotels).catch(console.error).finally(() => setLoading(false)); }, []);

  const handleBook = (h) => { user ? setSelected(h) : setAuthModal(true); };
  const formatDate = (dt) => new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

  return (
    <div>
      <div className="page-header"><h1>Hotels</h1><p>Find the perfect place to stay</p></div>

      {loading ? (
        <div className="page-loading"><div className="spinner" /></div>
      ) : hotels.length === 0 ? (
        <div className="empty-state"><Hotel /><p>No hotels available right now.</p></div>
      ) : (
        <div className="card-grid">
          {hotels.map((h, i) => (
            <motion.div key={h.id} className="service-card" initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <div className="card-header">
                <div>
                  <div className="card-title">{h.property_name}</div>
                  <div className="card-subtitle">{h.location}</div>
                </div>
                <div className="card-price">${h.price_per_night}<span className="card-price-unit">/night</span></div>
              </div>
              <div className="card-details">
                <span className="card-detail"><BedDouble size={14} />{h.room_type}</span>
                <span className="card-detail"><Calendar size={14} />{formatDate(h.check_in)} – {formatDate(h.check_out)}</span>
                <span className="card-detail">{h.available_rooms} rooms left</span>
              </div>
              <div className="card-actions">
                <button className="btn btn-primary btn-sm" onClick={() => handleBook(h)}
                  disabled={h.available_rooms < 1}>
                  {h.available_rooms < 1 ? 'Fully Booked' : 'Book Now'}
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {selected && (
        <BookingModal title={selected.property_name}
          details={[
            { label: 'Location', value: selected.location },
            { label: 'Room Type', value: selected.room_type },
            { label: 'Check-in', value: formatDate(selected.check_in) },
            { label: 'Check-out', value: formatDate(selected.check_out) },
          ]}
          price={selected.price_per_night} priceUnit="/night"
          onConfirm={async ({ notes }) => { await bookHotel(selected.id, notes); setHotels(await getHotels()); }}
          onClose={() => setSelected(null)} />
      )}
      {authModal && <AuthModal onClose={() => setAuthModal(false)} />}
    </div>
  );
}
