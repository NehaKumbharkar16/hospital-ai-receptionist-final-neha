import { useState } from 'react'
import Chat from './components/Chat'
import Home from './pages/Home'
import PatientRegistration from './pages/PatientRegistration'
import AppointmentBooking from './pages/AppointmentBooking'
import AdminDashboard from './pages/AdminDashboard'
import './App.css'

type Page = 'home' | 'chat' | 'registration' | 'appointments' | 'admin'

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('home')
  const [chatKey, setChatKey] = useState(0)

  const handleNewUser = () => {
    setChatKey(prev => prev + 1)
  }

  return (
    <div className="App">
      {/* Navigation Bar */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="logo" onClick={() => setCurrentPage('home')}>
            <h1>🏥 Hospital Management</h1>
          </div>
          <ul className="nav-menu">
            <li><button onClick={() => setCurrentPage('home')} className={currentPage === 'home' ? 'active' : ''}>Home</button></li>
            <li><button onClick={() => setCurrentPage('registration')} className={currentPage === 'registration' ? 'active' : ''}>Register</button></li>
            <li><button onClick={() => setCurrentPage('appointments')} className={currentPage === 'appointments' ? 'active' : ''}>Appointments</button></li>
            <li><button onClick={() => setCurrentPage('admin')} className={currentPage === 'admin' ? 'active' : ''}>Dashboard</button></li>
            <li><button onClick={() => setCurrentPage('chat')} className={currentPage === 'chat' ? 'active' : ''}>AI Receptionist</button></li>
          </ul>
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        {currentPage === 'home' && <Home onNavigate={setCurrentPage} />}

        {currentPage === 'chat' && (
          <div className="chat-container">
            <div className="chat-header">
              <h2>Hospital AI Receptionist</h2>
              <p>Please describe your symptoms or concerns</p>
              <button onClick={handleNewUser} className="new-user-btn">New User</button>
            </div>
            <Chat key={chatKey} />
          </div>
        )}

        {currentPage === 'registration' && <PatientRegistration />}

        {currentPage === 'appointments' && <AppointmentBooking onNavigate={setCurrentPage} />}

        {currentPage === 'admin' && <AdminDashboard onNavigate={setCurrentPage} />}
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>&copy; 2026 Hospital Management System. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default App