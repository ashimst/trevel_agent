import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext.jsx';
import Layout from './components/Layout.jsx';
import DashboardPage from './pages/DashboardPage.jsx';
import FlightsPage from './pages/FlightsPage.jsx';
import HotelsPage from './pages/HotelsPage.jsx';
import BusesPage from './pages/BusesPage.jsx';
import ActivitiesPage from './pages/ActivitiesPage.jsx';
import GuidesPage from './pages/GuidesPage.jsx';
import CarRentalsPage from './pages/CarRentalsPage.jsx';
import BookingsPage from './pages/BookingsPage.jsx';
import TripsPage from './pages/TripsPage.jsx';
import ChatPage from './pages/ChatPage.jsx';

function App() {
  return (
    <AuthProvider>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/flights" element={<FlightsPage />} />
          <Route path="/hotels" element={<HotelsPage />} />
          <Route path="/buses" element={<BusesPage />} />
          <Route path="/activities" element={<ActivitiesPage />} />
          <Route path="/guides" element={<GuidesPage />} />
          <Route path="/car-rentals" element={<CarRentalsPage />} />
          <Route path="/bookings" element={<BookingsPage />} />
          <Route path="/trips" element={<TripsPage />} />
          <Route path="/chat" element={<ChatPage />} />
        </Routes>
      </Layout>
    </AuthProvider>
  );
}

export default App;
