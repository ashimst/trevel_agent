import apiClient from './client.js';

// ── Flights ──────────────────────────────────────────────────────────────
export const getFlights = (skip = 0, limit = 20) =>
  apiClient.get(`/flights/?skip=${skip}&limit=${limit}`).then(r => r.data);

export const getFlight = (id) =>
  apiClient.get(`/flights/${id}`).then(r => r.data);

export const bookFlight = (id, notes = '') =>
  apiClient.post(`/flights/${id}/book`, { notes }).then(r => r.data);

// ── Hotels ───────────────────────────────────────────────────────────────
export const getHotels = (skip = 0, limit = 20) =>
  apiClient.get(`/hotels/?skip=${skip}&limit=${limit}`).then(r => r.data);

export const getHotel = (id) =>
  apiClient.get(`/hotels/${id}`).then(r => r.data);

export const bookHotel = (id, notes = '') =>
  apiClient.post(`/hotels/${id}/book`, { notes }).then(r => r.data);

// ── Buses ────────────────────────────────────────────────────────────────
export const getBuses = (skip = 0, limit = 20) =>
  apiClient.get(`/buses/?skip=${skip}&limit=${limit}`).then(r => r.data);

export const getBus = (id) =>
  apiClient.get(`/buses/${id}`).then(r => r.data);

export const bookBus = (id, notes = '') =>
  apiClient.post(`/buses/${id}/book`, { notes }).then(r => r.data);

// ── Activities ───────────────────────────────────────────────────────────
export const getActivities = (skip = 0, limit = 20) =>
  apiClient.get(`/activities/?skip=${skip}&limit=${limit}`).then(r => r.data);

export const getActivity = (id) =>
  apiClient.get(`/activities/${id}`).then(r => r.data);

export const bookActivity = (id, notes = '') =>
  apiClient.post(`/activities/${id}/book`, { notes }).then(r => r.data);

// ── Guides ───────────────────────────────────────────────────────────────
export const getGuides = (skip = 0, limit = 20) =>
  apiClient.get(`/guides/?skip=${skip}&limit=${limit}`).then(r => r.data);

export const getGuide = (id) =>
  apiClient.get(`/guides/${id}`).then(r => r.data);

export const bookGuide = (id, bookingFrom, bookingTo, notes = '') =>
  apiClient.post(`/guides/${id}/book`, { booking_from: bookingFrom, booking_to: bookingTo, notes }).then(r => r.data);

// ── Car Rentals ──────────────────────────────────────────────────────────
export const getCarRentals = (skip = 0, limit = 20) =>
  apiClient.get(`/car-rentals/?skip=${skip}&limit=${limit}`).then(r => r.data);

export const getCarRental = (id) =>
  apiClient.get(`/car-rentals/${id}`).then(r => r.data);

export const bookCarRental = (id, notes = '') =>
  apiClient.post(`/car-rentals/${id}/book`, { notes }).then(r => r.data);

// ── Bookings ─────────────────────────────────────────────────────────────
export const getMyBookings = (skip = 0, limit = 50) =>
  apiClient.get(`/bookings/me?skip=${skip}&limit=${limit}`).then(r => r.data);

export const getBooking = (id) =>
  apiClient.get(`/bookings/${id}`).then(r => r.data);

export const cancelBooking = (id) =>
  apiClient.delete(`/bookings/${id}`);

// ── Trips ────────────────────────────────────────────────────────────────
export const getMyTrips = () =>
  apiClient.get('/trips/me').then(r => r.data);

export const getTrip = (id) =>
  apiClient.get(`/trips/${id}`).then(r => r.data);

export const createTrip = (name, description = '') =>
  apiClient.post('/trips/', { name, description }).then(r => r.data);

export const addBookingToTrip = (tripId, bookingId) =>
  apiClient.post(`/trips/${tripId}/bookings`, { booking_id: bookingId }).then(r => r.data);

export const removeBookingFromTrip = (tripId, bookingId) =>
  apiClient.delete(`/trips/${tripId}/bookings/${bookingId}`).then(r => r.data);

export const deleteTrip = (id) =>
  apiClient.delete(`/trips/${id}`);

// ── Payments (Demo) ──────────────────────────────────────────────────────
export const payBooking = (bookingId) =>
  apiClient.post(`/payments/pay/${bookingId}`).then(r => r.data);

export const failBooking = (bookingId) =>
  apiClient.post(`/payments/fail/${bookingId}`).then(r => r.data);

export const completeBooking = (bookingId) =>
  apiClient.post(`/payments/complete/${bookingId}`).then(r => r.data);

// ── Chat ─────────────────────────────────────────────────────────────────
export const sendChatMessage = (message, threadId = null) =>
  apiClient.post('/chat/', { message, thread_id: threadId }).then(r => r.data);
