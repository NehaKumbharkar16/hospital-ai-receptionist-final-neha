import React from 'react'

interface HomeProps {
  onNavigate?: (page: string) => void
}

const Home: React.FC<HomeProps> = ({ onNavigate }) => {
  return (
    <section className="home-page">
      <div className="hero">
        <h2>Welcome to Our Hospital Management System</h2>
        <p>Streamlined healthcare services powered by AI</p>
      </div>

      <div className="features">
        <div className="feature-card">
          <div className="icon">🤖</div>
          <h3>AI Receptionist</h3>
          <p>Automated patient intake and symptom analysis</p>
          <button onClick={() => onNavigate?.('chat')}>Start Chat</button>
        </div>

        <div className="feature-card">
          <div className="icon">📋</div>
          <h3>Patient Registration</h3>
          <p>Easy and secure patient registration process</p>
          <button onClick={() => onNavigate?.('registration')}>Register</button>
        </div>

        <div className="feature-card">
          <div className="icon">📅</div>
          <h3>Appointment Booking</h3>
          <p>Schedule appointments with available doctors</p>
          <button onClick={() => onNavigate?.('appointments')}>Book Now</button>
        </div>

        <div className="feature-card">
          <div className="icon">📊</div>
          <h3>Admin Dashboard</h3>
          <p>Hospital statistics and management tools</p>
          <button onClick={() => onNavigate?.('admin')}>View Dashboard</button>
        </div>
      </div>

      <div className="services">
        <h3>Our Services</h3>
        <ul>
          <li>✅ 24/7 AI Powered Patient Support</li>
          <li>✅ Instant Doctor Recommendations</li>
          <li>✅ Real-time Appointment Management</li>
          <li>✅ Emergency Case Prioritization</li>
          <li>✅ Comprehensive Patient Records</li>
          <li>✅ Doctor Feedback & Ratings</li>
        </ul>
      </div>
    </section>
  )
}

export default Home
