import React, { useState, useEffect } from 'react'
import { getApiUrl } from '../utils/api'

interface AdminDashboardProps {
  onNavigate?: (page: string) => void
}

const AdminDashboard: React.FC<AdminDashboardProps> = ({ onNavigate }) => {
  const [stats, setStats] = useState<any>(null)
  const [emergencyCases, setEmergencyCases] = useState<any[]>([])
  const [patientsToday, setPatientsToday] = useState<any[]>([])
  const [allPatients, setAllPatients] = useState<any[]>([])
  const [pendingAppointments, setPendingAppointments] = useState<any[]>([])
  const [availableDoctorsList, setAvailableDoctorsList] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [successMessage, setSuccessMessage] = useState('')
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    setLoading(true)
    try {
      // Load dashboard overview
      const overviewResponse = await fetch(getApiUrl('/api/admin/dashboard/overview'))
      if (overviewResponse.ok) {
        const overviewData = await overviewResponse.json()
        setStats(overviewData)
      }

      // Load emergency cases
      const emergencyResponse = await fetch(getApiUrl('/api/admin/emergency-cases?days=7'))
      if (emergencyResponse.ok) {
        const emergencyData = await emergencyResponse.json()
        setEmergencyCases(emergencyData.cases || [])
      }
      setSuccessMessage('✅ Dashboard data refreshed successfully!')
      setTimeout(() => setSuccessMessage(''), 4000)
    } catch (error) {
      console.error('Error loading dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadPatientToday = async () => {
    setLoading(true)
    try {
      const response = await fetch(getApiUrl('/api/admin/patients/today'))
      if (response.ok) {
        const data = await response.json()
        setPatientsToday(data.patients || [])
        setActiveTab('todays-patients')
        setSuccessMessage(`✅ Loaded ${data.total} patients from today`)
        setTimeout(() => setSuccessMessage(''), 4000)
      } else {
        alert('Failed to load patients from today')
      }
    } catch (error) {
      console.error('Error loading patients today:', error)
      alert('Error loading patients from today')
    } finally {
      setLoading(false)
    }
  }

  const loadAllPatients = async () => {
    setLoading(true)
    try {
      const response = await fetch(getApiUrl('/api/admin/patients/all'))
      if (response.ok) {
        const data = await response.json()
        setAllPatients(data.patients || [])
        setActiveTab('all-patients')
        setSuccessMessage(`✅ Loaded ${data.total} total patients`)
        setTimeout(() => setSuccessMessage(''), 4000)
      } else {
        alert('Failed to load all patients')
      }
    } catch (error) {
      console.error('Error loading all patients:', error)
      alert('Error loading all patients')
    } finally {
      setLoading(false)
    }
  }

  const loadPendingAppointments = async () => {
    setLoading(true)
    try {
      const response = await fetch(getApiUrl('/api/appointments?status=scheduled'))
      if (response.ok) {
        const data = await response.json()
        setPendingAppointments(data)
        setActiveTab('pending-appointments')
        setSuccessMessage(`✅ Loaded ${data.length} pending appointments`)
        setTimeout(() => setSuccessMessage(''), 4000)
      } else {
        alert('Failed to load pending appointments')
      }
    } catch (error) {
      console.error('Error loading pending appointments:', error)
      alert('Error loading pending appointments')
    } finally {
      setLoading(false)
    }
  }

  const loadAvailableDoctors = async () => {
    setLoading(true)
    try {
      const response = await fetch(getApiUrl('/api/doctors'))
      if (response.ok) {
        const data = await response.json()
        const availableDocs = data.filter((doc: any) => !doc.is_on_leave)
        setAvailableDoctorsList(availableDocs)
        setActiveTab('available-doctors')
        setSuccessMessage(`✅ Loaded ${availableDocs.length} available doctors`)
        setTimeout(() => setSuccessMessage(''), 4000)
      } else {
        alert('Failed to load available doctors')
      }
    } catch (error) {
      console.error('Error loading available doctors:', error)
      alert('Error loading available doctors')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="admin-container">
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        }}>
          <div style={{
            background: 'white',
            padding: '40px 60px',
            borderRadius: '15px',
            textAlign: 'center',
            boxShadow: '0 20px 60px rgba(0,0,0,0.3)'
          }}>
            <div style={{
              fontSize: '3rem',
              marginBottom: '20px',
              animation: 'spin 2s linear infinite'
            }}>⚙️</div>
            <p style={{ fontSize: '1.1rem', color: '#333', margin: '0' }}>Loading dashboard...</p>
          </div>
        </div>
        <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
      </div>
    )
  }

  return (
    <div className="admin-container">
      {/* Success Message Alert */}
      {successMessage && (
        <div className="success-alert">
          {successMessage}
        </div>
      )}

      {/* Header Section */}
      <div className="dashboard-header">
        <div className="header-content">
          <h1>🏥 Hospital Admin Dashboard</h1>
          <p>Comprehensive hospital management and real-time statistics</p>
        </div>
        <button 
          className="refresh-button"
          onClick={() => loadDashboardData()}
        >
          🔄 Refresh Data
        </button>
      </div>

      {/* Tab Navigation */}
      <div className="tab-navigation">
        <button 
          className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button 
          className={`tab-button ${activeTab === 'emergency' ? 'active' : ''}`}
          onClick={() => setActiveTab('emergency')}
        >
          🚨 Emergency Cases
        </button>
        <button 
          className={`tab-button ${activeTab === 'patients' ? 'active' : ''}`}
          onClick={() => setActiveTab('patients')}
        >
          👥 Recent Patients
        </button>
        <button 
          className={`tab-button ${activeTab === 'todays-patients' ? 'active' : ''}`}
          onClick={() => loadPatientToday()}
        >
          📆 Today's Patients
        </button>
        <button 
          className={`tab-button ${activeTab === 'all-patients' ? 'active' : ''}`}
          onClick={() => loadAllPatients()}
        >
          📋 All Patients
        </button>
        <button 
          className={`tab-button ${activeTab === 'pending-appointments' ? 'active' : ''}`}
          onClick={() => loadPendingAppointments()}
        >
          📅 Pending Appointments
        </button>
        <button 
          className={`tab-button ${activeTab === 'available-doctors' ? 'active' : ''}`}
          onClick={() => loadAvailableDoctors()}
        >
          👨‍⚕️ Available Doctors
        </button>
      </div>

      {stats && (
        <>
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="tab-content">
              {/* Key Metrics */}
              <div className="metrics-grid">
                <div 
                  className="metric-card"
                  onClick={() => loadPatientToday()}
                  style={{ cursor: 'pointer', transition: 'transform 0.2s, box-shadow 0.2s' }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-5px)'
                    e.currentTarget.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)'
                    e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)'
                  }}
                >
                  <div className="metric-icon">👥</div>
                  <div className="metric-content">
                    <div className="metric-value">{stats.statistics?.total_patients_today || 0}</div>
                    <div className="metric-label">Patients Today (Click to view)</div>
                  </div>
                </div>

                <div 
                  className="metric-card"
                  onClick={() => loadPendingAppointments()}
                  style={{ cursor: 'pointer', transition: 'transform 0.2s, box-shadow 0.2s' }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-5px)'
                    e.currentTarget.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)'
                    e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)'
                  }}
                >
                  <div className="metric-icon">📅</div>
                  <div className="metric-content">
                    <div className="metric-value">{stats.pending_appointments || 0}</div>
                    <div className="metric-label">Pending Appointments (Click to view)</div>
                  </div>
                </div>

                <div className="metric-card">
                  <div className="metric-icon">🚨</div>
                  <div className="metric-content">
                    <div className="metric-value">{stats.statistics?.emergency_cases || 0}</div>
                    <div className="metric-label">Emergency Cases</div>
                  </div>
                </div>

                <div 
                  className="metric-card"
                  onClick={() => loadAvailableDoctors()}
                  style={{ cursor: 'pointer', transition: 'transform 0.2s, box-shadow 0.2s' }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-5px)'
                    e.currentTarget.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)'
                    e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)'
                  }}
                >
                  <div className="metric-icon">👨‍⚕️</div>
                  <div className="metric-content">
                    <div className="metric-value">{stats.available_doctors || 0}</div>
                    <div className="metric-label">Available Doctors (Click to view)</div>
                  </div>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="dashboard-section">
                <h2 className="section-header">⚡ Quick Actions</h2>
                <div className="action-buttons">
                  <button 
                    className="action-button view-patients"
                    onClick={() => loadAllPatients()}
                  >
                    <span className="button-icon">👥</span>
                    <span>View All Patients</span>
                  </button>
                  <button 
                    className="action-button manage-appointments"
                    onClick={() => onNavigate?.('appointments')}
                  >
                    <span className="button-icon">📅</span>
                    <span>Manage Appointments</span>
                  </button>
                  <button 
                    className="action-button refresh-data"
                    onClick={() => loadDashboardData()}
                  >
                    <span className="button-icon">🔄</span>
                    <span>Refresh Data</span>
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Emergency Cases Tab */}
          {activeTab === 'emergency' && (
            <div className="tab-content">
              {emergencyCases.length > 0 ? (
                <div className="dashboard-section">
                  <h2 className="section-header">🚨 Recent Emergency Cases (Last 7 Days)</h2>
                  <div className="cases-list">
                    {emergencyCases.slice(0, 10).map((caseItem: any) => (
                      <div key={caseItem.id} className="case-item emergency">
                        <div className="case-header">
                          <span className="case-id">Case #{caseItem.appointment_number}</span>
                          <span className="case-priority">🚨 {caseItem.priority.toUpperCase()}</span>
                        </div>
                        <div className="case-content">
                          <p className="case-reason"><strong>Reason:</strong> {caseItem.reason_for_visit}</p>
                          <p className="case-date"><strong>📅 Date:</strong> {new Date(caseItem.appointment_date).toLocaleString()}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="empty-state">
                  <p className="empty-icon">✅</p>
                  <p className="empty-text">No emergency cases in the last 7 days</p>
                </div>
              )}
            </div>
          )}

          {/* Recent Patients Tab */}
          {activeTab === 'patients' && (
            <div className="tab-content">
              {stats.recent_patients && stats.recent_patients.length > 0 ? (
                <div className="dashboard-section">
                  <h2 className="section-header">👥 Recently Registered Patients</h2>
                  <div className="patients-list">
                    {stats.recent_patients.slice(0, 10).map((patient: any) => (
                      <div key={patient.id} className="patient-card">
                        <div className="patient-header">
                          <div className="patient-avatar">{patient.first_name.charAt(0)}</div>
                          <div className="patient-info">
                            <p className="patient-name">{patient.first_name} {patient.last_name}</p>
                            <p className="patient-id">ID: {patient.patient_id}</p>
                          </div>
                        </div>
                        <div className="patient-details">
                          <p><strong>📧 Email:</strong> {patient.email}</p>
                          <p><strong>📞 Phone:</strong> {patient.phone}</p>
                          <p className="patient-registered"><strong>📅 Registered:</strong> {new Date(patient.registration_date).toLocaleDateString()}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="empty-state">
                  <p className="empty-icon">🔍</p>
                  <p className="empty-text">No recently registered patients</p>
                </div>
              )}
            </div>
          )}

          {/* Today's Patients Tab */}
          {activeTab === 'todays-patients' && (
            <div className="tab-content">
              {patientsToday.length > 0 ? (
                <div className="dashboard-section">
                  <h2 className="section-header">📆 Patients Registered Today ({patientsToday.length})</h2>
                  <div className="patients-list">
                    {patientsToday.map((patient: any) => (
                      <div key={patient.id} className="patient-card">
                        <div className="patient-header">
                          <div className="patient-avatar">{patient.first_name.charAt(0)}</div>
                          <div className="patient-info">
                            <p className="patient-name">{patient.first_name} {patient.last_name}</p>
                            <p className="patient-id">ID: {patient.patient_id}</p>
                          </div>
                        </div>
                        <div className="patient-details">
                          <p><strong>📧 Email:</strong> {patient.email}</p>
                          <p><strong>📞 Phone:</strong> {patient.phone}</p>
                          <p><strong>🎂 Age:</strong> {patient.age}</p>
                          <p><strong>⚕️ Blood Group:</strong> {patient.blood_group || 'N/A'}</p>
                          <p className="patient-registered"><strong>⏰ Registered At:</strong> {new Date(patient.registration_date).toLocaleTimeString()}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="empty-state">
                  <p className="empty-icon">📭</p>
                  <p className="empty-text">No patients registered today</p>
                </div>
              )}
            </div>
          )}

          {/* All Patients Tab */}
          {activeTab === 'all-patients' && (
            <div className="tab-content">
              {allPatients.length > 0 ? (
                <div className="dashboard-section">
                  <h2 className="section-header">📋 All Patients ({allPatients.length})</h2>
                  <div className="patients-list">
                    {allPatients.map((patient: any) => (
                      <div key={patient.id} className="patient-card">
                        <div className="patient-header">
                          <div className="patient-avatar">{patient.first_name.charAt(0)}</div>
                          <div className="patient-info">
                            <p className="patient-name">{patient.first_name} {patient.last_name}</p>
                            <p className="patient-id">ID: {patient.patient_id}</p>
                          </div>
                        </div>
                        <div className="patient-details">
                          <p><strong>📧 Email:</strong> {patient.email}</p>
                          <p><strong>📞 Phone:</strong> {patient.phone}</p>
                          <p><strong>🎂 Age:</strong> {patient.age}</p>
                          <p><strong>⚕️ Blood Group:</strong> {patient.blood_group || 'N/A'}</p>
                          <p className="patient-registered"><strong>📅 Registered:</strong> {new Date(patient.registration_date).toLocaleDateString()}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="empty-state">
                  <p className="empty-icon">🔍</p>
                  <p className="empty-text">No patients found</p>
                </div>
              )}
            </div>
          )}

          {/* Pending Appointments Tab */}
          {activeTab === 'pending-appointments' && (
            <div className="tab-content">
              {pendingAppointments.length > 0 ? (
                <div className="dashboard-section">
                  <h2 className="section-header">📅 Pending Appointments ({pendingAppointments.length})</h2>
                  <div className="appointments-list">
                    {pendingAppointments.map((appointment: any) => (
                      <div key={appointment.id} className="appointment-card">
                        <div className="appointment-header">
                          <span className="apt-number">APT #{appointment.appointment_number}</span>
                          <span className={`status-badge status-${appointment.status}`}>
                            {appointment.status?.toUpperCase() || 'SCHEDULED'}
                          </span>
                        </div>
                        <div className="appointment-details">
                          <p><strong>📅 Date & Time:</strong> {new Date(appointment.appointment_date).toLocaleString()}</p>
                          <p><strong>📝 Reason:</strong> {appointment.reason_for_visit || 'N/A'}</p>
                          <p><strong>⚠️ Priority:</strong> {appointment.priority?.toUpperCase() || 'NORMAL'}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="empty-state">
                  <p className="empty-icon">✅</p>
                  <p className="empty-text">No pending appointments</p>
                </div>
              )}
            </div>
          )}

          {/* Available Doctors Tab */}
          {activeTab === 'available-doctors' && (
            <div className="tab-content">
              {availableDoctorsList.length > 0 ? (
                <div className="dashboard-section">
                  <h2 className="section-header">👨‍⚕️ Available Doctors ({availableDoctorsList.length})</h2>
                  <div className="doctors-list">
                    {availableDoctorsList.map((doctor: any) => (
                      <div key={doctor.id} className="doctor-card">
                        <div className="doctor-header">
                          <div className="doctor-avatar">{doctor.name.charAt(0)}</div>
                          <div className="doctor-info">
                            <p className="doctor-name">Dr. {doctor.name}</p>
                            <p className="doctor-qualification">{doctor.qualification || 'MD'}</p>
                          </div>
                        </div>
                        <div className="doctor-details">
                          <p><strong>📧 Email:</strong> {doctor.email}</p>
                          <p><strong>📞 Phone:</strong> {doctor.phone}</p>
                          <p><strong>⏱️ Experience:</strong> {doctor.experience_years || 0} years</p>
                          <p><strong>💰 Consultation Fee:</strong> ₹{doctor.consultation_fee || 'N/A'}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="empty-state">
                  <p className="empty-icon">🔍</p>
                  <p className="empty-text">No available doctors at the moment</p>
                </div>
              )}
            </div>
          )}
        </>
      )}

      <style>{`
        .admin-container {
          max-width: 1400px;
          margin: 0 auto;
          padding: 30px 20px;
          background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
          min-height: 100vh;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .success-alert {
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          color: white;
          padding: 15px 20px;
          border-radius: 8px;
          margin-bottom: 20px;
          font-weight: 600;
          animation: slideIn 0.5s ease-out;
          box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
          display: flex;
          align-items: center;
        }

        @keyframes slideIn {
          from {
            transform: translateY(-20px);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }

        .dashboard-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 40px 30px;
          border-radius: 15px;
          margin-bottom: 30px;
          box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
          flex-wrap: wrap;
          gap: 20px;
        }

        .header-content h1 {
          margin: 0 0 10px 0;
          font-size: 2.5rem;
          font-weight: 700;
          letter-spacing: -0.5px;
        }

        .header-content p {
          margin: 0;
          font-size: 1.1rem;
          opacity: 0.95;
          color: #f0f0f0;
        }

        .refresh-button {
          background: rgba(255, 255, 255, 0.2);
          color: white;
          border: 2px solid white;
          padding: 12px 25px;
          border-radius: 8px;
          cursor: pointer;
          font-weight: 600;
          transition: all 0.3s ease;
          font-size: 1rem;
        }

        .refresh-button:hover {
          background: white;
          color: #667eea;
          transform: translateY(-2px);
          box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }

        .tab-navigation {
          display: flex;
          gap: 15px;
          margin-bottom: 30px;
          flex-wrap: wrap;
        }

        .tab-button {
          background: white;
          color: #667eea;
          border: 2px solid #e0e0e0;
          padding: 12px 25px;
          border-radius: 8px;
          cursor: pointer;
          font-weight: 600;
          font-size: 1rem;
          transition: all 0.3s ease;
        }

        .tab-button:hover {
          border-color: #667eea;
          background: #f5f7fa;
        }

        .tab-button.active {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-color: transparent;
          box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }

        .tab-content {
          animation: fadeIn 0.4s ease-out;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 20px;
          margin-bottom: 30px;
        }

        .metric-card {
          background: white;
          border-radius: 12px;
          padding: 25px;
          display: flex;
          align-items: center;
          gap: 20px;
          box-shadow: 0 4px 15px rgba(0,0,0,0.08);
          border: 2px solid #f0f0f0;
          transition: all 0.3s ease;
          cursor: pointer;
          position: relative;
          overflow: hidden;
        }

        .metric-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
          border-color: #667eea;
        }

        .metric-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }

        .metric-icon {
          font-size: 3rem;
          min-width: 70px;
          text-align: center;
        }

        .metric-content {
          flex: 1;
        }

        .metric-value {
          font-size: 2.5rem;
          font-weight: 700;
          color: #333;
          margin: 0;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .metric-label {
          color: #666;
          font-size: 0.95rem;
          margin-top: 8px;
          font-weight: 500;
        }

        .dashboard-section {
          background: white;
          border-radius: 12px;
          padding: 30px;
          margin-bottom: 25px;
          box-shadow: 0 4px 15px rgba(0,0,0,0.08);
          border: 1px solid #f0f0f0;
          transition: all 0.3s ease;
        }

        .dashboard-section:hover {
          box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        }

        .section-header {
          margin: 0 0 25px 0;
          color: #333;
          font-size: 1.5rem;
          font-weight: 700;
          border-bottom: 3px solid #667eea;
          padding-bottom: 12px;
        }

        .cases-list,
        .patients-list {
          display: grid;
          gap: 15px;
        }

        .case-item {
          background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%);
          border-left: 5px solid #ff6b6b;
          border-radius: 8px;
          padding: 20px;
          transition: all 0.3s ease;
          position: relative;
        }

        .case-item:hover {
          transform: translateX(5px);
          box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);
        }

        .case-item.emergency {
          border-left-color: #ff6b6b;
        }

        .case-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 12px;
          flex-wrap: wrap;
          gap: 10px;
        }

        .case-id {
          font-weight: 700;
          color: #333;
          font-size: 1.05rem;
        }

        .case-priority {
          font-weight: 700;
          color: #ff6b6b;
          background: rgba(255, 107, 107, 0.1);
          padding: 4px 12px;
          border-radius: 6px;
        }

        .case-content {
          margin: 0;
        }

        .case-content p {
          margin: 8px 0;
          color: #555;
          font-size: 0.95rem;
        }

        .case-reason {
          font-weight: 500;
        }

        .patient-card {
          background: linear-gradient(135deg, #f5f7fa 0%, #f0f3f7 100%);
          border-radius: 10px;
          padding: 20px;
          border-left: 5px solid #667eea;
          transition: all 0.3s ease;
        }

        .patient-card:hover {
          transform: translateX(5px);
          box-shadow: 0 6px 20px rgba(102, 126, 234, 0.15);
        }

        .patient-header {
          display: flex;
          align-items: center;
          gap: 15px;
          margin-bottom: 15px;
        }

        .patient-avatar {
          width: 50px;
          height: 50px;
          border-radius: 50%;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 700;
          font-size: 1.3rem;
          flex-shrink: 0;
        }

        .patient-info p {
          margin: 0;
        }

        .patient-name {
          font-weight: 700;
          color: #333;
          font-size: 1.1rem;
        }

        .patient-id {
          color: #666;
          font-size: 0.9rem;
          margin-top: 4px;
        }

        .patient-details {
          padding-left: 65px;
        }

        .patient-details p {
          margin: 6px 0;
          color: #555;
          font-size: 0.95rem;
        }

        .patient-registered {
          color: #666;
          font-size: 0.9rem;
          margin-top: 8px;
          padding-top: 8px;
          border-top: 1px solid rgba(102, 126, 234, 0.2);
        }

        .action-buttons {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
          gap: 15px;
          margin-top: 20px;
        }

        .action-button {
          background: white;
          border: 2px solid #e0e0e0;
          padding: 16px 20px;
          border-radius: 10px;
          cursor: pointer;
          font-weight: 600;
          font-size: 1rem;
          transition: all 0.3s ease;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 8px;
        }

        .action-button:hover {
          transform: translateY(-5px);
          box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }

        .action-button.view-patients {
          border-color: #667eea;
          color: #667eea;
        }

        .action-button.view-patients:hover {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-color: transparent;
        }

        .action-button.manage-appointments {
          border-color: #10b981;
          color: #10b981;
        }

        .action-button.manage-appointments:hover {
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          color: white;
          border-color: transparent;
        }

        .action-button.refresh-data {
          border-color: #f59e0b;
          color: #f59e0b;
        }

        .action-button.refresh-data:hover {
          background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
          color: white;
          border-color: transparent;
        }

        .button-icon {
          font-size: 1.5rem;
        }

        .empty-state {
          text-align: center;
          padding: 60px 40px;
          background: linear-gradient(135deg, #f5f7fa 0%, #f0f3f7 100%);
          border-radius: 12px;
          border: 2px dashed #e0e0e0;
        }

        .empty-icon {
          font-size: 4rem;
          margin: 0 0 20px 0;
          display: block;
        }

        .empty-text {
          margin: 0;
          color: #666;
          font-size: 1.1rem;
          font-weight: 500;
        }

        @media (max-width: 768px) {
          .admin-container {
            padding: 15px;
          }

          .dashboard-header {
            flex-direction: column;
            text-align: center;
            padding: 25px 20px;
          }

          .header-content h1 {
            font-size: 1.8rem;
          }

          .header-content p {
            font-size: 0.95rem;
          }

          .metrics-grid {
            grid-template-columns: 1fr;
          }

          .metric-card {
            flex-direction: column;
            text-align: center;
            padding: 20px;
          }

          .metric-icon {
            font-size: 2.5rem;
          }

          .metric-value {
            font-size: 2rem;
          }

          .tab-navigation {
            flex-direction: column;
          }

          .tab-button {
            width: 100%;
          }

          .dashboard-section {
            padding: 20px;
          }

          .patient-header {
            flex-wrap: wrap;
          }

          .patient-details {
            padding-left: 0;
            margin-top: 10px;
          }

          .action-buttons {
            grid-template-columns: 1fr;
          }

          .action-button {
            flex-direction: row;
          }

          .section-header {
            font-size: 1.2rem;
          }
        }

        /* Appointment and Doctor Cards */
        .appointments-list,
        .doctors-list {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
          gap: 20px;
          margin-top: 20px;
        }

        .appointment-card,
        .doctor-card {
          background: linear-gradient(135deg, #f5f7fa 0%, #f0f3f7 100%);
          border-radius: 10px;
          padding: 20px;
          border-left: 5px solid #667eea;
          transition: all 0.3s ease;
        }

        .appointment-card:hover,
        .doctor-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
          border-left-color: #764ba2;
        }

        .appointment-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 15px;
          padding-bottom: 10px;
          border-bottom: 1px solid #ddd;
        }

        .apt-number {
          font-weight: 700;
          color: #667eea;
          font-size: 1.05rem;
        }

        .appointment-details,
        .doctor-details {
          font-size: 0.9rem;
          color: #555;
        }

        .appointment-details p,
        .doctor-details p {
          margin: 8px 0;
          line-height: 1.4;
        }

        .doctor-header {
          display: flex;
          align-items: center;
          gap: 15px;
          margin-bottom: 15px;
          padding-bottom: 15px;
          border-bottom: 1px solid #ddd;
        }

        .doctor-avatar {
          width: 45px;
          height: 45px;
          border-radius: 50%;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 700;
          font-size: 1.2rem;
        }

        .doctor-info {
          flex: 1;
        }

        .doctor-name {
          margin: 0;
          font-weight: 700;
          font-size: 1.05rem;
          color: #333;
        }

        .doctor-qualification {
          margin: 4px 0 0 0;
          font-size: 0.85rem;
          color: #999;
        }

        .status-badge {
          padding: 6px 14px;
          border-radius: 20px;
          font-size: 0.8rem;
          font-weight: 600;
          text-transform: uppercase;
        }

        .status-badge.status-scheduled {
          background: #e3f2fd;
          color: #1976d2;
        }

        .status-badge.status-completed {
          background: #c8e6c9;
          color: #388e3c;
        }

        .status-badge.status-cancelled {
          background: #ffcdd2;
          color: #d32f2f;
        }
      `}</style>
    </div>
  )
}

export default AdminDashboard
