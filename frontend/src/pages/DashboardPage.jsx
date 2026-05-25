import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plane, Hotel, Bus, Sparkles, Users, Car, MessageSquare, ArrowRight, Award, MapPin, Smile } from 'lucide-react';
import { motion } from 'framer-motion';

const services = [
  { to: '/flights', icon: Plane, label: 'Flights', desc: 'Search & book flights worldwide' },
  { to: '/hotels', icon: Hotel, label: 'Hotels', desc: 'Find the perfect stay' },
  { to: '/buses', icon: Bus, label: 'Buses', desc: 'Affordable bus travel' },
  { to: '/activities', icon: Sparkles, label: 'Activities', desc: 'Tours & experiences' },
  { to: '/guides', icon: Users, label: 'Guides', desc: 'Expert local guides' },
  { to: '/car-rentals', icon: Car, label: 'Car Rentals', desc: 'Rent your ride' },
];

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.08, duration: 0.4 }
  })
};

// Smooth animatable counter using requestAnimationFrame
function Counter({ end, duration = 1.5 }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTimestamp = null;
    const endVal = parseInt(end.replace(/\D/g, ''));
    if (isNaN(endVal)) return;

    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / (duration * 1000), 1);
      setCount(Math.floor(progress * endVal));
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };

    window.requestAnimationFrame(step);
  }, [end, duration]);

  const suffix = end.replace(/[0-9]/g, '');
  return <span>{count.toLocaleString()}{suffix}</span>;
}

export default function DashboardPage() {
  return (
    <div>
      {/* Hero Section with polished look */}
      <motion.div 
        className="hero-section" 
        initial={{ opacity: 0, y: 30 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ duration: 0.5 }}
      >
        <h1 className="hero-title">Travel smarter with <span>Yatra</span></h1>
        <p className="hero-subtitle">
          Book flights, hotels, buses, activities, guides, and car rentals — all in one place.
          Or let our AI concierge plan your complete travel itinerary.
        </p>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <Link to="/chat" className="btn btn-primary" style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <MessageSquare size={18} /> Ask Yatra AI
            <ArrowRight size={16} />
          </Link>
        </div>
      </motion.div>

      {/* Stats Counter Row */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', 
        gap: '1.25rem', 
        marginBottom: '2.5rem' 
      }}>
        <motion.div 
          className="glass-panel" 
          style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
        >
          <div style={{ padding: '10px', background: 'var(--accent-muted)', borderRadius: 'var(--radius-md)', color: 'var(--accent)' }}>
            <Smile size={24} />
          </div>
          <div>
            <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--accent)', lineHeight: 1.2 }}>
              <Counter end="12850+" />
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Happy Travelers</div>
          </div>
        </motion.div>

        <motion.div 
          className="glass-panel" 
          style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div style={{ padding: '10px', background: 'rgba(16, 185, 129, 0.1)', borderRadius: 'var(--radius-md)', color: 'var(--success)' }}>
            <MapPin size={24} />
          </div>
          <div>
            <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--success)', lineHeight: 1.2 }}>
              <Counter end="450+" />
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Active Destinations</div>
          </div>
        </motion.div>

        <motion.div 
          className="glass-panel" 
          style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
        >
          <div style={{ padding: '10px', background: 'rgba(245, 158, 11, 0.1)', borderRadius: 'var(--radius-md)', color: 'var(--warning)' }}>
            <Award size={24} />
          </div>
          <div>
            <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--warning)', lineHeight: 1.2 }}>
              <Counter end="99.2%" />
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Customer Satisfaction</div>
          </div>
        </motion.div>
      </div>

      {/* Quick Access Grid */}
      <h2 style={{ marginBottom: '1.25rem', fontWeight: 600 }}>Explore Services</h2>
      <div className="quick-grid">
        {services.map((svc, i) => (
          <motion.div key={svc.to} custom={i} initial="hidden" animate="visible" variants={fadeUp}>
            <Link to={svc.to} className="quick-card">
              <div className="quick-card-icon"><svc.icon size={24} /></div>
              <div className="quick-card-label" style={{ fontWeight: 600 }}>{svc.label}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{svc.desc}</div>
            </Link>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
