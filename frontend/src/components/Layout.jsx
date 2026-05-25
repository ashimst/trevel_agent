import { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  Plane, Hotel, Bus, Compass, Users, Car,
  ClipboardList, Map, MessageSquare, LogOut, Menu, X, Sparkles,
  Sun, Moon
} from 'lucide-react';
import { useAuth } from '../context/AuthContext.jsx';
import AuthModal from './AuthModal.jsx';

const navItems = [
  { label: 'Explore', items: [
    { to: '/', icon: Compass, text: 'Dashboard' },
    { to: '/flights', icon: Plane, text: 'Flights' },
    { to: '/hotels', icon: Hotel, text: 'Hotels' },
    { to: '/buses', icon: Bus, text: 'Buses' },
    { to: '/activities', icon: Sparkles, text: 'Activities' },
    { to: '/guides', icon: Users, text: 'Guides' },
    { to: '/car-rentals', icon: Car, text: 'Car Rentals' },
  ]},
  { label: 'Manage', items: [
    { to: '/bookings', icon: ClipboardList, text: 'My Bookings' },
    { to: '/trips', icon: Map, text: 'My Trips' },
  ]},
  { label: 'AI Agent', items: [
    { to: '/chat', icon: MessageSquare, text: 'Ask Yatra' },
  ]},
];

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const navigate = useNavigate();

  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('theme');
    if (saved) return saved === 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  const getInitials = (name) => name ? name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) : '??';

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <Plane size={22} className="logo-icon" />
          <h1>YATRA</h1>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((section) => (
            <div key={section.label}>
              <div className="sidebar-section-label">{section.label}</div>
              {section.items.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.to === '/'}
                  className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                  onClick={() => setSidebarOpen(false)}
                >
                  <item.icon size={20} className="nav-icon" />
                  <span>{item.text}</span>
                </NavLink>
              ))}
            </div>
          ))}
        </nav>

        <div className="sidebar-footer">
          {user ? (
            <>
              <div className="user-card">
                <div className="user-avatar">{getInitials(user.full_name)}</div>
                <div className="user-info">
                  <div className="user-name">{user.full_name}</div>
                  <div className="user-email">{user.email}</div>
                </div>
              </div>
              <button className="btn btn-ghost btn-sm" onClick={logout} style={{ justifyContent: 'flex-start' }}>
                <LogOut size={16} /> Sign Out
              </button>
            </>
          ) : (
            <button className="btn btn-primary" onClick={() => setAuthModalOpen(true)} style={{ width: '100%' }}>
              Sign In
            </button>
          )}
        </div>
      </aside>

      {/* Mobile overlay */}
      <div className={`sidebar-overlay ${sidebarOpen ? 'open' : ''}`} onClick={() => setSidebarOpen(false)} />

      {/* Main */}
      <div className="main-content">
        <div className="top-bar">
          <button className="mobile-toggle" onClick={() => setSidebarOpen(true)}>
            <Menu size={24} />
          </button>
          <div style={{ flex: 1 }} />
          <button 
            className="btn btn-ghost btn-icon" 
            onClick={() => setDarkMode(!darkMode)} 
            title="Toggle theme"
            style={{ marginRight: '0.5rem', display: 'flex', alignItems: 'center', padding: '6px' }}
          >
            {darkMode ? <Sun size={20} /> : <Moon size={20} />}
          </button>
          {user && (
            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              Welcome, {user.full_name}
            </span>
          )}
        </div>

        <div className="page-content">
          {children}
        </div>
      </div>

      {authModalOpen && <AuthModal onClose={() => setAuthModalOpen(false)} />}
    </div>
  );
}
