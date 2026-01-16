import React, { useState, useEffect } from 'react'

interface AppointmentBookingProps {
  onNavigate?: (page: string) => void
}

const AppointmentBooking: React.FC<AppointmentBookingProps> = ({ onNavigate }) => {
  const [loading, setLoading] = useState(false)
  const [doctors, setDoctors] = useState([])
  const [appointments, setAppointments] = useState([])

  const [formData, setFormData] = useState({
    patientId: '',
    doctorId: '',
    appointmentDate: '',
    reason: '',
    priority: 'normal',
  })

  const [lookupPatientEmail, setLookupPatientEmail] = useState('')

  useEffect(() => {
    // Load doctors on component mount
    loadDoctors()
  }, [])

  const loadDoctors = async () => {
    try {
      const response = await fetch('/api/doctors')
      if (response.ok) {
        const data = await response.json()
        setDoctors(data)
      }
    } catch (error) {
      console.error('Error loading doctors:', error)
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
      const patientResponse = await fetch(`/api/patients/lookup?email=${lookupPatientEmail}`, {
        method: 'POST'
      })

      if (patientResponse.ok) {
        const patients = await patientResponse.json()
        if (patients.length > 0) {
          const patientId = patients[0].id
          setFormData(prev => ({ ...prev, patientId }))

          // Get patient appointments
          const appointmentsResponse = await fetch(`/api/appointments/patient/${patientId}`)
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

    setLoading(true)
    try {
      const response = await fetch('/api/appointments/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_id: formData.patientId,
          doctor_id: formData.doctorId,
          department_id: '', // Should be fetched from doctor
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
        alert('Error booking appointment')
      }
    } catch (error) {
      console.error('Error:', error)
      alert('Failed to book appointment')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="appointments-container">
      <h2>Appointment Management</h2>

      <div className="appointment-content">
        {/* Patient Lookup */}
        <div className="patient-lookup">
          <h3>Find Patient</h3>
          <div className="search-form">
            <input
              type="email"
              placeholder="Enter patient email"
              value={lookupPatientEmail}
              onChange={(e) => setLookupPatientEmail(e.target.value)}
            />
            <button onClick={loadPatientAppointments} disabled={loading}>
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </div>

        {formData.patientId && (
          <>
            {/* Book Appointment */}
            <div className="book-appointment">
              <h3>Book New Appointment</h3>
              <form onSubmit={handleBookAppointment} className="form">
                <select
                  name="doctorId"
                  value={formData.doctorId}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select Doctor</option>
                  {doctors.map((doctor: any) => (
                    <option key={doctor.id} value={doctor.id}>
                      {doctor.name} - {doctor.specialization_id}
                    </option>
                  ))}
                </select>

                <input
                  type="datetime-local"
                  name="appointmentDate"
                  value={formData.appointmentDate}
                  onChange={handleInputChange}
                  required
                />

                <textarea
                  name="reason"
                  placeholder="Reason for visit"
                  value={formData.reason}
                  onChange={handleInputChange}
                  rows={4}
                />

                <select
                  name="priority"
                  value={formData.priority}
                  onChange={handleInputChange}
                >
                  <option value="normal">Normal</option>
                  <option value="urgent">Urgent</option>
                  <option value="emergency">Emergency</option>
                </select>

                <button type="submit" className="submit-btn" disabled={loading}>
                  {loading ? 'Booking...' : 'Book Appointment'}
                </button>
              </form>
            </div>

            {/* Appointment History */}
            <div className="appointment-history">
              <h3>Appointment History</h3>
              {appointments.length > 0 ? (
                <div className="appointments-list">
                  {appointments.map((apt: any) => (
                    <div key={apt.id} className="appointment-item">
                      <p><strong>Appointment #:</strong> {apt.appointment_number}</p>
                      <p><strong>Date:</strong> {new Date(apt.appointment_date).toLocaleString()}</p>
                      <p><strong>Status:</strong> <span className={`status ${apt.status}`}>{apt.status}</span></p>
                      <p><strong>Reason:</strong> {apt.reason_for_visit}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p>No appointments found</p>
              )}
            </div>
          </>
        )}
      </div>

      <style>{`
        .appointment-content {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 30px;
          margin-top: 30px;
        }

        .patient-lookup,
        .book-appointment {
          background: #f9f9f9;
          padding: 20px;
          border-radius: 8px;
          border: 1px solid #e0e0e0;
        }

        .search-form {
          display: flex;
          gap: 10px;
        }

        .search-form input {
          flex: 1;
          padding: 10px;
          border: 1px solid #ddd;
          border-radius: 5px;
        }

        .search-form button {
          background: #667eea;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 5px;
          cursor: pointer;
          font-weight: 600;
        }

        .search-form button:hover {
          background: #764ba2;
        }

        .appointment-history {
          grid-column: 1 / -1;
        }

        .appointments-list {
          display: grid;
          gap: 15px;
        }

        .appointment-item {
          background: #f9f9f9;
          padding: 15px;
          border-radius: 8px;
          border-left: 4px solid #667eea;
        }

        .appointment-item p {
          margin: 8px 0;
          font-size: 0.95rem;
        }

        .status {
          display: inline-block;
          padding: 4px 12px;
          border-radius: 20px;
          font-size: 0.85rem;
          font-weight: 600;
        }

        .status.scheduled { background: #e3f2fd; color: #1976d2; }
        .status.completed { background: #c8e6c9; color: #388e3c; }
        .status.cancelled { background: #ffcdd2; color: #d32f2f; }

        @media (max-width: 768px) {
          .appointment-content {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  )
}

export default AppointmentBooking
