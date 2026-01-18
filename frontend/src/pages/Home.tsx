import React, { useState, useEffect } from 'react'
import { getApiUrl } from '../utils/api'

interface HomeProps {
  onNavigate?: (page: string) => void
}

const Home: React.FC<HomeProps> = ({ onNavigate }) => {
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardStats()
  }, [])

  const loadDashboardStats = async () => {
    try {
      const response = await fetch(getApiUrl('/api/admin/dashboard/overview'))
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (error) {
      console.error('Error loading dashboard stats:', error)
    } finally {
      setLoading(false)
    }
  }

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

      <div className="dashboard-stats">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h4>{stats?.patients_today ?? 0}</h4>
            <p>Patients Today<br/>(Click to view)</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📅</div>
          <div className="stat-content">
            <h4>{stats?.pending_appointments ?? 0}</h4>
            <p>Pending<br/>Appointments<br/>(Click to view)</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🚨</div>
          <div className="stat-content">
            <h4>{stats?.emergency_cases ?? 0}</h4>
            <p>Emergency Cases<br/>(Click to view)</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">👨‍⚕️</div>
          <div className="stat-content">
            <h4>{stats?.available_doctors ?? 0}</h4>
            <p>Available Doctors<br/>(Click to view)</p>
          </div>
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
