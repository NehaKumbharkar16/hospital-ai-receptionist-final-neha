import React, { useState, useEffect } from 'react'
import { getApiUrl } from '../utils/api'

interface AppointmentBookingProps {
  onNavigate?: (page: string) => void
  selectedPatient?: any
}

const AppointmentBooking: React.FC<AppointmentBookingProps> = ({ selectedPatient }) => {
  const [loading, setLoading] = useState(false)
  const [doctors, setDoctors] = useState([])
  const [appointments, setAppointments] = useState([])
  const [allScheduledAppointments, setAllScheduledAppointments] = useState([])
  const [availableDoctors, setAvailableDoctors] = useState([])
  const [showScheduledAppointments, setShowScheduledAppointments] = useState(false)
  const [showAvailableDoctors, setShowAvailableDoctors] = useState(false)

  const [formData, setFormData] = useState({
    patientId: selectedPatient?.id || '',
    doctorId: '',
    appointmentDate: '',
    reason: '',
    priority: 'normal',
  })

  const [lookupPatientEmail, setLookupPatientEmail] = useState('')

  useEffect(() => {
    // Load doctors on component mount
    loadDoctors()
    // Load all scheduled appointments
    loadAllScheduledAppointments()
    // Load available doctors
    loadAvailableDoctors()
    
    // If patient was passed, load their appointments
    if (selectedPatient?.id) {
      setFormData(prev => ({ ...prev, patientId: selectedPatient.id }))
      loadPatientAppointmentsForId(selectedPatient.id)
    }
  }, [selectedPatient])

  const loadDoctors = async () => {
    try {
      const response = await fetch(getApiUrl('/api/doctors'))
      if (response.ok) {
        const data = await response.json()
        setDoctors(data)
      }
    } catch (error) {
      console.error('Error loading doctors:', error)
    }
  }

  const loadAllScheduledAppointments = async () => {
    try {
      const response = await fetch(getApiUrl('/api/appointments?status=scheduled'))
      if (response.ok) {
        const data = await response.json()
        setAllScheduledAppointments(data)
      }
    } catch (error) {
      console.error('Error loading scheduled appointments:', error)
    }
  }

  const loadAvailableDoctors = async () => {
    try {
      const response = await fetch(getApiUrl('/api/doctors'))
      if (response.ok) {
        const data = await response.json()
        const notOnLeave = data.filter((doc: any) => !doc.is_on_leave)
        setAvailableDoctors(notOnLeave)
      }
    } catch (error) {
      console.error('Error loading available doctors:', error)
    }
  }

  const loadPatientAppointmentsForId = async (patientId: string) => {
    try {
      const appointmentsResponse = await fetch(getApiUrl(`/api/appointments/patient/${patientId}`))
      if (appointmentsResponse.ok) {
        const appts = await appointmentsResponse.json()
        setAppointments(appts)
      }
    } catch (error) {
      console.error('Error loading appointments:', error)
    }
  }

  const loadPatientAppointments = async () => {
    if (!lookupPatientEmail) {
      alert('Please enter patient email')
      return
    }

    setLoading(true)
    try {
      // First find patient by email
      const patientResponse = await fetch(getApiUrl(`/api/patients/lookup?email=${lookupPatientEmail}`), {
        method: 'POST'
      })

      if (patientResponse.ok) {
        const patients = await patientResponse.json()
        if (patients.length > 0) {
          const patientId = patients[0].id
          setFormData(prev => ({ ...prev, patientId }))

          // Get patient appointments
          const appointmentsResponse = await fetch(getApiUrl(`/api/appointments/patient/${patientId}`))
          if (appointmentsResponse.ok) {
            const appts = await appointmentsResponse.json()
            setAppointments(appts)
          }
        }
      }
    } catch (error) {
      console.error('Error:', error)
      alert('Failed to load patient appointments')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleBookAppointment = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.patientId) {
      alert('Please lookup a patient first')
      return
    }

    if (!formData.doctorId) {
      alert('Please select a doctor')
      return
    }

    // Get department_id from selected doctor
    const selectedDoctor = doctors.find((d: any) => d.id === formData.doctorId)
    const departmentId = selectedDoctor?.department_id || ''

    if (!departmentId) {
      alert('Doctor has no assigned department')
      return
    }

    setLoading(true)
    try {
      const response = await fetch(getApiUrl('/api/appointments/'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_id: formData.patientId,
          doctor_id: formData.doctorId,
          department_id: departmentId,
          appointment_date: new Date(formData.appointmentDate).toISOString(),
          reason_for_visit: formData.reason,
          priority: formData.priority,
        })
      })

      if (response.ok) {
        const data = await response.json()
        alert(`Appointment booked successfully! Appointment #: ${data.appointment_number}`)
        setFormData({
          patientId: '',
          doctorId: '',
          appointmentDate: '',
          reason: '',
          priority: 'normal',
        })
        loadPatientAppointments()
      } else {
        const errorData = await response.json().catch(() => ({}))
        alert(`Error booking appointment: ${errorData.detail || 'Unknown error'}`)
      }
    } catch (error) {
      console.error('Error:', error)
      alert(`Failed to book appointment: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="appointments-page">
      <div className="appointments-header">
        <div className="header-content">
          <h1>📅 Appointment Booking</h1>
          <p>Schedule and manage your appointments with our doctors</p>
        </div>
      </div>

      <div className="appointments-container">
        <div className="page-content">
          {/* Patient Lookup Section */}
          <div className="patient-lookup-section">
            <div className="lookup-card">
              <div className="lookup-header">
                <h2>🔍 Find Patient Record</h2>
                <p>Enter patient email to view or book appointments</p>
              </div>
              <div className="lookup-form">
                <div className="input-group">
                  <input
                    type="email"
                    placeholder="Enter patient email"
                    value={lookupPatientEmail}
                    onChange={(e) => setLookupPatientEmail(e.target.value)}
                    className="email-input"
                  />
                  <button onClick={loadPatientAppointments} disabled={loading} className="search-btn">
                    {loading ? '⏳ Searching...' : '🔎 Search'}
                  </button>
                </div>
              </div>
            </div>
          </div>

          {formData.patientId && (
            <>
              {/* Book Appointment Section */}
              <div className="booking-section">
                <div className="section-card">
                  <div className="section-header">
                    <h2>📋 Book New Appointment</h2>
                    <p>Fill in the details to schedule your appointment</p>
                  </div>
                  
                  <form onSubmit={handleBookAppointment} className="booking-form">
                    <div className="form-grid">
                      <div className="form-group">
                        <label htmlFor="doctorId">🏥 Select Doctor</label>
                        <select
                          id="doctorId"
                          name="doctorId"
                          value={formData.doctorId}
                          onChange={handleInputChange}
                          required
                          className="form-input"
                        >
                          <option value="">-- Choose a doctor --</option>
                          {doctors.map((doctor: any) => (
                            <option key={doctor.id} value={doctor.id}>
                              Dr. {doctor.name}
                            </option>
                          ))}
                        </select>
                      </div>

                      <div className="form-group">
                        <label htmlFor="appointmentDate">📆 Appointment Date & Time</label>
                        <input
                          id="appointmentDate"
                          type="datetime-local"
                          name="appointmentDate"
                          value={formData.appointmentDate}
                          onChange={handleInputChange}
                          required
                          className="form-input"
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="priority">⚠️ Priority Level</label>
                        <select
                          id="priority"
                          name="priority"
                          value={formData.priority}
                          onChange={handleInputChange}
                          className="form-input"
                        >
                          <option value="normal">Normal</option>
                          <option value="urgent">Urgent</option>
                          <option value="emergency">Emergency</option>
                        </select>
                      </div>

                      <div className="form-group full-width">
                        <label htmlFor="reason">📝 Reason for Visit</label>
                        <textarea
                          id="reason"
                          name="reason"
                          placeholder="Describe your symptoms or reason for visiting..."
                          value={formData.reason}
                          onChange={handleInputChange}
                          rows={4}
                          className="form-input textarea"
                        />
                      </div>
                    </div>

                    <button type="submit" className="submit-btn" disabled={loading}>
                      {loading ? '⏳ Booking...' : '✓ Book Appointment'}
                    </button>
                  </form>
                </div>
              </div>

              {/* Appointment History Section */}
              <div className="history-section">
                <div className="section-card">
                  <div className="section-header">
                    <h2>📊 Appointment History</h2>
                    <p>Your previous and upcoming appointments</p>
                  </div>

                  {appointments.length > 0 ? (
                    <div className="appointments-list">
                      {appointments.map((apt: any) => (
                        <div key={apt.id} className="appointment-card">
                          <div className="appointment-header">
                            <div className="appointment-number">
                              <span className="label">Appointment ID</span>
                              <span className="value">{apt.appointment_number}</span>
                            </div>
                            <span className={`status-badge status-${apt.status}`}>
                              {apt.status.charAt(0).toUpperCase() + apt.status.slice(1)}
                            </span>
                          </div>
                          
                          <div className="appointment-details">
                            <div className="detail-item">
                              <span className="icon">📅</span>
                              <div>
                                <span className="label">Date & Time</span>
                                <span className="value">{new Date(apt.appointment_date).toLocaleString()}</span>
                              </div>
                            </div>
                            {apt.reason_for_visit && (
                              <div className="detail-item">
                                <span className="icon">📝</span>
                                <div>
                                  <span className="label">Reason</span>
                                  <span className="value">{apt.reason_for_visit}</span>
                                </div>
                              </div>
                            )}
                            {apt.priority && (
                              <div className="detail-item">
                                <span className="icon">⚠️</span>
                                <div>
                                  <span className="label">Priority</span>
                                  <span className="value">{apt.priority}</span>
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="no-appointments">
                      <p>No appointments found yet</p>
                      <small>Your scheduled appointments will appear here</small>
                    </div>
                  )}
                </div>
              </div>
            </>
          )}

          {/* Scheduled Appointments Section */}
          <div className="scheduled-appointments-section">
            <div className="section-card">
              <div className="section-header">
                <h2>📋 System Scheduled Appointments</h2>
                <button 
                  className="toggle-button"
                  onClick={() => setShowScheduledAppointments(!showScheduledAppointments)}
                >
                  {showScheduledAppointments ? '▼ Hide' : '▶ Show'} ({allScheduledAppointments.length})
                </button>
              </div>
              
              {showScheduledAppointments && (
                <div className="scheduled-list">
                  {allScheduledAppointments.length > 0 ? (
                    allScheduledAppointments.slice(0, 20).map((apt: any) => (
                      <div key={apt.id} className="scheduled-item">
                        <div className="scheduled-header">
                          <span className="apt-number">#{apt.appointment_number}</span>
                          <span className={`status-badge status-${apt.status}`}>{apt.status}</span>
                        </div>
                        <div className="scheduled-info">
                          <p><strong>📅 Date:</strong> {new Date(apt.appointment_date).toLocaleString()}</p>
                          <p><strong>📝 Reason:</strong> {apt.reason_for_visit || 'N/A'}</p>
                          <p><strong>⚠️ Priority:</strong> {apt.priority}</p>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="empty-message">No scheduled appointments</p>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Available Doctors Section */}
          <div className="available-doctors-section">
            <div className="section-card">
              <div className="section-header">
                <h2>👨‍⚕️ Available Doctors</h2>
                <button 
                  className="toggle-button"
                  onClick={() => setShowAvailableDoctors(!showAvailableDoctors)}
                >
                  {showAvailableDoctors ? '▼ Hide' : '▶ Show'} ({availableDoctors.length})
                </button>
              </div>
              
              {showAvailableDoctors && (
                <div className="doctors-list">
                  {availableDoctors.length > 0 ? (
                    availableDoctors.map((doctor: any) => (
                      <div key={doctor.id} className="doctor-card">
                        <div className="doctor-header">
                          <div className="doctor-avatar">👨‍⚕️</div>
                          <div className="doctor-info">
                            <p className="doctor-name">Dr. {doctor.name}</p>
                            <p className="doctor-qualification">{doctor.qualification || 'MD'}</p>
                          </div>
                        </div>
                        <div className="doctor-details">
                          <p><strong>📧 Email:</strong> {doctor.email}</p>
                          <p><strong>📞 Phone:</strong> {doctor.phone}</p>
                          <p><strong>⏱️ Experience:</strong> {doctor.experience_years || 0} years</p>
                          <p><strong>💰 Fee:</strong> ₹{doctor.consultation_fee || 500}</p>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="empty-message">No available doctors at the moment</p>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <style>{`
        .appointments-page {
          min-height: 100vh;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .appointments-header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 40px 20px;
          text-align: center;
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }

        .header-content h1 {
          margin: 0 0 10px 0;
          font-size: 2.5rem;
          font-weight: 700;
        }

        .header-content p {
          margin: 0;
          font-size: 1.1rem;
          opacity: 0.95;
        }

        .appointments-container {
          max-width: 1200px;
          margin: -30px auto 40px;
          padding: 40px;
          background: white;
          border-radius: 15px;
          box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        }

        .page-content {
          display: flex;
          flex-direction: column;
          gap: 30px;
        }

        /* Patient Lookup Section */
        .patient-lookup-section {
          width: 100%;
        }

        .lookup-card {
          background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
          padding: 30px;
          border-radius: 12px;
          border: 2px solid #667eea;
        }

        .lookup-header {
          margin-bottom: 25px;
        }

        .lookup-header h2 {
          margin: 0 0 8px 0;
          color: #333;
          font-size: 1.5rem;
        }

        .lookup-header p {
          margin: 0;
          color: #666;
          font-size: 0.95rem;
        }

        .lookup-form {
          display: flex;
          gap: 15px;
        }

        .input-group {
          display: flex;
          gap: 10px;
          width: 100%;
        }

        .email-input {
          flex: 1;
          padding: 12px 16px;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          font-size: 1rem;
          transition: all 0.3s ease;
        }

        .email-input:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .search-btn {
          padding: 12px 30px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          white-space: nowrap;
        }

        .search-btn:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .search-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        /* Booking Section */
        .booking-section {
          width: 100%;
        }

        .section-card {
          background: white;
          padding: 30px;
          border-radius: 12px;
          border: 1px solid #e0e0e0;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }

        .section-header {
          margin-bottom: 25px;
          border-bottom: 2px solid #f0f0f0;
          padding-bottom: 20px;
        }

        .section-header h2 {
          margin: 0 0 8px 0;
          color: #333;
          font-size: 1.5rem;
        }

        .section-header p {
          margin: 0;
          color: #666;
          font-size: 0.95rem;
        }

        .booking-form {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .form-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 20px;
        }

        .form-group {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .form-group.full-width {
          grid-column: 1 / -1;
        }

        .form-group label {
          font-weight: 600;
          color: #333;
          font-size: 0.95rem;
        }

        .form-input {
          padding: 12px 16px;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          font-size: 1rem;
          font-family: inherit;
          transition: all 0.3s ease;
        }

        .form-input:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .form-input.textarea {
          resize: vertical;
          min-height: 100px;
        }

        .submit-btn {
          padding: 14px 30px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          margin-top: 10px;
        }

        .submit-btn:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .submit-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        /* History Section */
        .history-section {
          width: 100%;
        }

        .appointments-list {
          display: grid;
          grid-template-columns: 1fr;
          gap: 15px;
        }

        .appointment-card {
          background: white;
          border: 1px solid #e0e0e0;
          border-radius: 10px;
          padding: 20px;
          transition: all 0.3s ease;
          border-left: 4px solid #667eea;
        }

        .appointment-card:hover {
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
          transform: translateY(-2px);
        }

        .appointment-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 15px;
          padding-bottom: 15px;
          border-bottom: 1px solid #f0f0f0;
        }

        .appointment-number {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .appointment-number .label {
          font-size: 0.85rem;
          color: #999;
          font-weight: 500;
        }

        .appointment-number .value {
          font-size: 1.1rem;
          font-weight: 700;
          color: #667eea;
        }

        .status-badge {
          padding: 6px 16px;
          border-radius: 20px;
          font-size: 0.85rem;
          font-weight: 600;
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

        .appointment-details {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 15px;
        }

        .detail-item {
          display: flex;
          gap: 12px;
          align-items: flex-start;
        }

        .detail-item .icon {
          font-size: 1.3rem;
          min-width: 30px;
          text-align: center;
        }

        .detail-item div {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .detail-item .label {
          font-size: 0.85rem;
          color: #999;
          font-weight: 500;
        }

        .detail-item .value {
          font-size: 0.95rem;
          color: #333;
          font-weight: 500;
        }

        .no-appointments {
          text-align: center;
          padding: 40px 20px;
          color: #999;
        }

        .no-appointments p {
          margin: 0 0 8px 0;
          font-size: 1.1rem;
          font-weight: 500;
        }

        .no-appointments small {
          display: block;
          color: #bbb;
        }

        @media (max-width: 768px) {
          .form-grid {
            grid-template-columns: 1fr;
          }

          .header-content h1 {
            font-size: 1.8rem;
          }

          .appointment-details {
            grid-template-columns: 1fr;
          }

          .lookup-form {
            flex-direction: column;
          }

          .input-group {
            flex-direction: column;
          }
        }

        /* Scheduled Appointments and Available Doctors Sections */
        .scheduled-appointments-section,
        .available-doctors-section {
          margin-top: 30px;
        }

        .section-card {
          background: white;
          border-radius: 12px;
          padding: 25px;
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
          padding-bottom: 15px;
          border-bottom: 2px solid #667eea;
        }

        .section-header h2 {
          margin: 0;
          font-size: 1.5rem;
          color: #333;
        }

        .toggle-button {
          background: #667eea;
          color: white;
          border: none;
          padding: 8px 16px;
          border-radius: 6px;
          cursor: pointer;
          font-weight: 600;
          transition: all 0.3s ease;
        }

        .toggle-button:hover {
          background: #5568d3;
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }

        .scheduled-list,
        .doctors-list {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
          gap: 20px;
          margin-top: 20px;
        }

        .scheduled-item,
        .doctor-card {
          background: #f8f9fa;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          padding: 15px;
          transition: all 0.3s ease;
        }

        .scheduled-item:hover,
        .doctor-card:hover {
          transform: translateY(-4px);
          box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
          border-color: #667eea;
        }

        .scheduled-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 12px;
        }

        .apt-number {
          font-weight: 700;
          color: #667eea;
          font-size: 1.1rem;
        }

        .scheduled-info {
          font-size: 0.9rem;
          color: #555;
        }

        .scheduled-info p {
          margin: 8px 0;
        }

        .doctor-header {
          display: flex;
          gap: 15px;
          align-items: center;
          margin-bottom: 15px;
          padding-bottom: 15px;
          border-bottom: 1px solid #ddd;
        }

        .doctor-avatar {
          font-size: 2rem;
          width: 50px;
          height: 50px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: #667eea;
          border-radius: 50%;
          color: white;
        }

        .doctor-info {
          flex: 1;
        }

        .doctor-name {
          margin: 0;
          font-weight: 700;
          font-size: 1.1rem;
          color: #333;
        }

        .doctor-qualification {
          margin: 4px 0 0 0;
          font-size: 0.85rem;
          color: #999;
        }

        .doctor-details {
          font-size: 0.9rem;
          color: #555;
        }

        .doctor-details p {
          margin: 8px 0;
        }

        .empty-message {
          text-align: center;
          color: #999;
          padding: 20px;
          font-style: italic;
        }
      `}</style>
    </div>
  )
}

export default AppointmentBooking
