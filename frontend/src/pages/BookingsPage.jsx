import { useState, useEffect } from 'react';
import { Plane, Hotel, Bus, Sparkles, Users, Car, ClipboardList, CreditCard, XCircle, CheckCircle2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { getMyBookings, cancelBooking, payBooking, completeBooking } from '../api/services.js';
import { useAuth } from '../context/AuthContext.jsx';
import AuthModal from '../components/AuthModal.jsx';

const typeIcons = { flight: Plane, hotel: Hotel, bus: Bus, activity: Sparkles, guide: Users, car_rental: Car };

export default function BookingsPage() {
  const { user } = useAuth();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(null);
  const [authModal, setAuthModal] = useState(false);

  const fetchBookings = async () => {
    setLoading(true);
    try { setBookings(await getMyBookings()); } catch (e) { console.error(e); }
    setLoading(false);
  };

  useEffect(() => { if (user) fetchBookings(); else setLoading(false); }, [user]);

  const handleAction = async (id, action) => {
    setActionLoading(id);
    try {
      if (action === 'pay') await payBooking(id);
      else if (action === 'cancel') await cancelBooking(id);
      else if (action === 'complete') await completeBooking(id);
      await fetchBookings();
    } catch (e) { alert(e.response?.data?.detail || 'Action failed'); }
    setActionLoading(null);
  };

  const formatDate = (dt) => new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });

  if (!user) return (
    <div>
      <div className="page-header"><h1>My Bookings</h1><p>View and manage your reservations</p></div>
      <div className="empty-state">
        <ClipboardList />
        <p>Sign in to view your bookings</p>
        <button className="btn btn-primary" onClick={() => setAuthModal(true)}>Sign In</button>
      </div>
      {authModal && <AuthModal onClose={() => setAuthModal(false)} />}
    </div>
  );

  return (
    <div>
      <div className="page-header"><h1>My Bookings</h1><p>View and manage your reservations</p></div>

      {loading ? (
        <div className="page-loading"><div className="spinner" /></div>
      ) : bookings.length === 0 ? (
        <div className="empty-state"><ClipboardList /><p>No bookings yet. Start exploring!</p></div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {bookings.map((b, i) => {
            const Icon = typeIcons[b.service_type] || ClipboardList;
            return (
              <motion.div key={b.id} className="booking-card" initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.04 }}>
                <div className="booking-icon"><Icon size={22} /></div>
                <div className="booking-info">
                  <div className="booking-type">{b.service_type.replace('_', ' ')}</div>
                  <div className="booking-id">ID: {b.id}</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{formatDate(b.created_at)}</div>
                </div>
                <div className="booking-amount">${b.amount.toFixed(2)}</div>
                <span className={`badge badge-${b.status}`}>{b.status}</span>
                <div className="booking-actions">
                  {b.status === 'pending' && (
                    <>
                      <button className="btn btn-primary btn-sm" disabled={actionLoading === b.id}
                        onClick={() => handleAction(b.id, 'pay')}>
                        <CreditCard size={14} /> Pay
                      </button>
                      <button className="btn btn-danger btn-sm" disabled={actionLoading === b.id}
                        onClick={() => handleAction(b.id, 'cancel')}>
                        <XCircle size={14} /> Cancel
                      </button>
                    </>
                  )}
                  {b.status === 'confirmed' && (
                    <button className="btn btn-sm" disabled={actionLoading === b.id}
                      onClick={() => handleAction(b.id, 'complete')}
                      style={{ background: 'var(--success-muted)', color: 'var(--success)', borderColor: 'transparent' }}>
                      <CheckCircle2 size={14} /> Complete
                    </button>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
}
