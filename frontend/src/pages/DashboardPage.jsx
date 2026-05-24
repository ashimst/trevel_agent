import { Link } from 'react-router-dom';
import { Plane, Hotel, Bus, Sparkles, Users, Car, MessageSquare, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

const services = [
  { to: '/flights', icon: Plane, label: 'Flights', desc: 'Search & book flights worldwide' },
  { to: '/hotels', icon: Hotel, label: 'Hotels', desc: 'Find the perfect stay' },
  { to: '/buses', icon: Bus, label: 'Buses', desc: 'Affordable bus travel' },
  { to: '/activities', icon: Sparkles, label: 'Activities', desc: 'Tours & experiences' },
  { to: '/guides', icon: Users, label: 'Guides', desc: 'Expert local guides' },
  { to: '/car-rentals', icon: Car, label: 'Car Rentals', desc: 'Rent your ride' },
];

const fadeUp = { hidden: { opacity: 0, y: 20 }, visible: (i) => ({ opacity: 1, y: 0, transition: { delay: i * 0.08, duration: 0.4 } }) };

export default function DashboardPage() {
  return (
    <div>
      {/* Hero */}
      <motion.div className="hero-section" initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
        <h1 className="hero-title">Travel smarter with <span>Yatra</span></h1>
        <p className="hero-subtitle">
          Book flights, hotels, buses, activities, guides, and car rentals — all in one place.
          Or let our AI concierge plan everything for you.
        </p>
        <Link to="/chat" className="btn btn-primary">
          <MessageSquare size={18} /> Ask Yatra AI
          <ArrowRight size={16} />
        </Link>
      </motion.div>

      {/* Quick Access Grid */}
      <h2 style={{ marginBottom: '1.25rem' }}>Explore Services</h2>
      <div className="quick-grid">
        {services.map((svc, i) => (
          <motion.div key={svc.to} custom={i} initial="hidden" animate="visible" variants={fadeUp}>
            <Link to={svc.to} className="quick-card">
              <div className="quick-card-icon"><svc.icon size={24} /></div>
              <div className="quick-card-label">{svc.label}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{svc.desc}</div>
            </Link>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
