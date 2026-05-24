import { useState, useEffect } from 'react';
import { Map, Plus, Trash2, X as XIcon, ChevronDown, ChevronUp } from 'lucide-react';
import { motion } from 'framer-motion';
import { getMyTrips, createTrip, deleteTrip, addBookingToTrip, removeBookingFromTrip, getMyBookings } from '../api/services.js';
import { useAuth } from '../context/AuthContext.jsx';
import AuthModal from '../components/AuthModal.jsx';

export default function TripsPage() {
  const { user } = useAuth();
  const [trips, setTrips] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [authModal, setAuthModal] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [name, setName] = useState('');
  const [desc, setDesc] = useState('');
  const [creating, setCreating] = useState(false);
  const [expanded, setExpanded] = useState(null);
  const [addBookingTripId, setAddBookingTripId] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [t, b] = await Promise.all([getMyTrips(), getMyBookings()]);
      setTrips(t);
      setBookings(b);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  useEffect(() => { if (user) fetchData(); else setLoading(false); }, [user]);

  const handleCreate = async (e) => {
    e.preventDefault();
    setCreating(true);
    try { await createTrip(name, desc); setName(''); setDesc(''); setShowCreate(false); await fetchData(); }
    catch (e) { alert(e.response?.data?.detail || 'Failed'); }
    setCreating(false);
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this trip?')) return;
    try { await deleteTrip(id); await fetchData(); } catch (e) { alert('Failed'); }
  };

  const handleAddBooking = async (tripId, bookingId) => {
    try { await addBookingToTrip(tripId, bookingId); await fetchData(); setAddBookingTripId(null); }
    catch (e) { alert(e.response?.data?.detail || 'Failed'); }
  };

  const handleRemoveBooking = async (tripId, bookingId) => {
    try { await removeBookingFromTrip(tripId, bookingId); await fetchData(); }
    catch (e) { alert('Failed'); }
  };

  const formatDate = (dt) => new Date(dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

  if (!user) return (
    <div>
      <div className="page-header"><h1>My Trips</h1><p>Organize bookings into trip packages</p></div>
      <div className="empty-state"><Map /><p>Sign in to manage your trips</p>
        <button className="btn btn-primary" onClick={() => setAuthModal(true)}>Sign In</button>
      </div>
      {authModal && <AuthModal onClose={() => setAuthModal(false)} />}
    </div>
  );

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div><h1>My Trips</h1><p>Organize bookings into trip packages</p></div>
        <button className="btn btn-primary" onClick={() => setShowCreate(!showCreate)}>
          <Plus size={18} /> New Trip
        </button>
      </div>

      {showCreate && (
        <motion.form initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
          onSubmit={handleCreate} className="glass-panel"
          style={{ padding: '1.5rem', marginBottom: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div className="form-group">
            <label className="form-label">Trip Name</label>
            <input className="input-field" value={name} onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Summer Europe 2026" required />
          </div>
          <div className="form-group">
            <label className="form-label">Description</label>
            <textarea className="input-field" value={desc} onChange={(e) => setDesc(e.target.value)}
              placeholder="Optional description..." rows={2} />
          </div>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button type="submit" className="btn btn-primary btn-sm" disabled={creating}>
              {creating ? 'Creating...' : 'Create Trip'}
            </button>
            <button type="button" className="btn btn-sm" onClick={() => setShowCreate(false)}>Cancel</button>
          </div>
        </motion.form>
      )}

      {loading ? (
        <div className="page-loading"><div className="spinner" /></div>
      ) : trips.length === 0 ? (
        <div className="empty-state"><Map /><p>No trips yet. Create one to group your bookings!</p></div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {trips.map((trip, i) => (
            <motion.div key={trip.id} className="trip-card" initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <div className="trip-card-header">
                <div style={{ cursor: 'pointer', flex: 1 }} onClick={() => setExpanded(expanded === trip.id ? null : trip.id)}>
                  <h3>{trip.name}</h3>
                  {trip.description && <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>{trip.description}</p>}
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    {trip.booking_ids.length} booking{trip.booking_ids.length !== 1 ? 's' : ''} · Created {formatDate(trip.created_at)}
                  </span>
                </div>
                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                  <button className="btn btn-sm" onClick={() => setAddBookingTripId(addBookingTripId === trip.id ? null : trip.id)}>
                    <Plus size={14} /> Add
                  </button>
                  <button className="btn btn-danger btn-sm btn-icon" onClick={() => handleDelete(trip.id)}>
                    <Trash2 size={14} />
                  </button>
                  {expanded === trip.id ? <ChevronUp size={18} style={{ color: 'var(--text-muted)' }} /> : <ChevronDown size={18} style={{ color: 'var(--text-muted)' }} />}
                </div>
              </div>

              {addBookingTripId === trip.id && (
                <div style={{ padding: '0 1.5rem 1rem', display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {bookings.filter(b => !trip.booking_ids.includes(b.id)).map(b => (
                    <button key={b.id} className="btn btn-sm" onClick={() => handleAddBooking(trip.id, b.id)}>
                      {b.service_type} — ${b.amount.toFixed(0)}
                    </button>
                  ))}
                  {bookings.filter(b => !trip.booking_ids.includes(b.id)).length === 0 && (
                    <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>No bookings to add</span>
                  )}
                </div>
              )}

              {expanded === trip.id && (
                <div className="trip-card-body">
                  {trip.booking_ids.length === 0 ? (
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>No bookings in this trip yet.</p>
                  ) : (
                    trip.booking_ids.map((bid) => {
                      const b = bookings.find(x => x.id === bid);
                      return (
                        <div key={bid} className="trip-booking-item">
                          <span>{b ? `${b.service_type} — $${b.amount.toFixed(2)} (${b.status})` : bid}</span>
                          <button className="btn btn-ghost btn-sm" onClick={() => handleRemoveBooking(trip.id, bid)}>
                            <XIcon size={14} />
                          </button>
                        </div>
                      );
                    })
                  )}
                </div>
              )}
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
