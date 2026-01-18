import React, { useState } from 'react'
import { getApiUrl } from '../utils/api'

interface PatientRegistrationProps {
  onNavigate?: (page: string) => void
  onPatientSelected?: (patient: any) => void
}

const PatientRegistration: React.FC<PatientRegistrationProps> = ({ onNavigate, onPatientSelected }) => {
  const [activeTab, setActiveTab] = useState<'register' | 'lookup'>('register')
  const [loading, setLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')
  const [errorMessage, setErrorMessage] = useState('')
  const [foundPatient, setFoundPatient] = useState<any>(null)

  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    age: '',
    gender: '',
    bloodGroup: '',
    address: '',
    emergencyContact: '',
    emergencyPhone: '',
  })

  const [lookupData, setLookupData] = useState({
    searchType: 'email',
    searchValue: '',
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmitRegistration = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setErrorMessage('')
    setSuccessMessage('')

    try {
      const response = await fetch(getApiUrl('/api/patients/register'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          first_name: formData.firstName,
          last_name: formData.lastName,
          email: formData.email,
          phone: formData.phone,
          age: parseInt(formData.age),
          gender: formData.gender,
          blood_group: formData.bloodGroup,
          address: formData.address,
          emergency_contact_name: formData.emergencyContact,
          emergency_contact_phone: formData.emergencyPhone,
        })
      })

      if (response.ok) {
        const data = await response.json()
        setSuccessMessage(`🎉 Success! Your Patient ID: ${data.patient_id}`)
        setTimeout(() => {
          setSuccessMessage('')
        }, 5000)
        setFormData({
          firstName: '',
          lastName: '',
          email: '',
          phone: '',
          age: '',
          gender: '',
          bloodGroup: '',
          address: '',
          emergencyContact: '',
          emergencyPhone: '',
        })
      } else {
        setErrorMessage('❌ Error registering patient. Please try again.')
      }
    } catch (error) {
      console.error('Error:', error)
      setErrorMessage('❌ Failed to register patient')
    } finally {
      setLoading(false)
    }
  }

  const handleLookupPatient = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setErrorMessage('')
    setFoundPatient(null)

    try {
      const lookupQuery: Record<string, string> = {}
      if (lookupData.searchType === 'email') {
        lookupQuery.email = lookupData.searchValue
      } else if (lookupData.searchType === 'phone') {
        lookupQuery.phone = lookupData.searchValue
      } else if (lookupData.searchType === 'patientId') {
        lookupQuery.patient_id = lookupData.searchValue
      }

      const params = new URLSearchParams(lookupQuery)
      const response = await fetch(getApiUrl(`/api/patients/lookup?${params}`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })

      if (response.ok) {
        const data = await response.json()
        if (data.length > 0) {
          setFoundPatient(data[0])
        } else {
          setErrorMessage('❌ No patient found with the provided information')
        }
      } else {
        setErrorMessage('❌ Error searching for patient')
      }
    } catch (error) {
      console.error('Error:', error)
      setErrorMessage('❌ Failed to lookup patient')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="registration-page">
      <div className="registration-header">
        <div className="header-content">
          <h1>📋 Patient Registration</h1>
          <p>Quick and secure patient registration process</p>
        </div>
      </div>

      <div className="registration-container">
        <div className="tabs-container">
          <button
            className={`tab-btn ${activeTab === 'register' ? 'active' : ''}`}
            onClick={() => { setActiveTab('register'); setErrorMessage(''); setFoundPatient(null); }}
          >
            <span className="tab-icon">✏️</span>
            <span>New Patient</span>
          </button>
          <button
            className={`tab-btn ${activeTab === 'lookup' ? 'active' : ''}`}
            onClick={() => { setActiveTab('lookup'); setErrorMessage(''); setFoundPatient(null); }}
          >
            <span className="tab-icon">🔍</span>
            <span>Find Patient</span>
          </button>
        </div>

        {successMessage && (
          <div className="alert alert-success">
            {successMessage}
          </div>
        )}

        {errorMessage && (
          <div className="alert alert-error">
            {errorMessage}
          </div>
        )}

        {activeTab === 'register' && (
          <form onSubmit={handleSubmitRegistration} className="registration-form">
            <div className="form-section">
              <h3>📝 Basic Information</h3>
              <div className="form-grid">
                <div className="form-group">
                  <label>First Name *</label>
                  <input
                    type="text"
                    name="firstName"
                    placeholder="John"
                    value={formData.firstName}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Last Name *</label>
                  <input
                    type="text"
                    name="lastName"
                    placeholder="Doe"
                    value={formData.lastName}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Email *</label>
                  <input
                    type="email"
                    name="email"
                    placeholder="john@example.com"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Phone *</label>
                  <input
                    type="tel"
                    name="phone"
                    placeholder="+1 (555) 123-4567"
                    value={formData.phone}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>
            </div>

            <div className="form-section">
              <h3>👤 Medical Details</h3>
              <div className="form-grid">
                <div className="form-group">
                  <label>Age *</label>
                  <input
                    type="number"
                    name="age"
                    placeholder="30"
                    min="0"
                    max="150"
                    value={formData.age}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Gender *</label>
                  <select
                    name="gender"
                    value={formData.gender}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="">Select Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Blood Group</label>
                  <select
                    name="bloodGroup"
                    value={formData.bloodGroup}
                    onChange={handleInputChange}
                  >
                    <option value="">Select Blood Group</option>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Address</label>
                  <input
                    type="text"
                    name="address"
                    placeholder="123 Main Street"
                    value={formData.address}
                    onChange={handleInputChange}
                  />
                </div>
              </div>
            </div>

            <div className="form-section">
              <h3>🚨 Emergency Contact</h3>
              <div className="form-grid">
                <div className="form-group">
                  <label>Contact Name</label>
                  <input
                    type="text"
                    name="emergencyContact"
                    placeholder="Jane Doe"
                    value={formData.emergencyContact}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="form-group">
                  <label>Contact Phone</label>
                  <input
                    type="tel"
                    name="emergencyPhone"
                    placeholder="+1 (555) 987-6543"
                    value={formData.emergencyPhone}
                    onChange={handleInputChange}
                  />
                </div>
              </div>
            </div>

            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? (
                <>
                  <span className="spinner"></span> Registering...
                </>
              ) : (
                <>✅ Register Patient</>
              )}
            </button>
          </form>
        )}

        {activeTab === 'lookup' && (
          <div className="lookup-section">
            <form onSubmit={handleLookupPatient} className="lookup-form">
              <div className="lookup-header">
                <h3>🔍 Find Your Patient Record</h3>
                <p>Search by email, phone, or patient ID</p>
              </div>

              <div className="search-options">
                <label className={`option ${lookupData.searchType === 'email' ? 'active' : ''}`}>
                  <input
                    type="radio"
                    name="searchType"
                    value="email"
                    checked={lookupData.searchType === 'email'}
                    onChange={() => setLookupData(prev => ({ ...prev, searchType: 'email' }))}
                  />
                  <span>📧 Email</span>
                </label>
                <label className={`option ${lookupData.searchType === 'phone' ? 'active' : ''}`}>
                  <input
                    type="radio"
                    name="searchType"
                    value="phone"
                    checked={lookupData.searchType === 'phone'}
                    onChange={() => setLookupData(prev => ({ ...prev, searchType: 'phone' }))}
                  />
                  <span>📱 Phone</span>
                </label>
                <label className={`option ${lookupData.searchType === 'patientId' ? 'active' : ''}`}>
                  <input
                    type="radio"
                    name="searchType"
                    value="patientId"
                    checked={lookupData.searchType === 'patientId'}
                    onChange={() => setLookupData(prev => ({ ...prev, searchType: 'patientId' }))}
                  />
                  <span>🆔 Patient ID</span>
                </label>
              </div>

              <div className="search-input-group">
                <input
                  type="text"
                  placeholder={
                    lookupData.searchType === 'email' ? 'Enter your email address' :
                    lookupData.searchType === 'phone' ? 'Enter your phone number' :
                    'Enter your patient ID (e.g., PAT12345)'
                  }
                  value={lookupData.searchValue}
                  onChange={(e) => setLookupData(prev => ({ ...prev, searchValue: e.target.value }))}
                  required
                />
                <button type="submit" className="search-btn" disabled={loading}>
                  {loading ? 'Searching...' : '🔎 Search'}
                </button>
              </div>
            </form>

            {foundPatient && (
              <div className="patient-card">
                <div className="card-header">
                  <h3>✅ Patient Found</h3>
                </div>
                <div className="card-content">
                  <div className="patient-info-grid">
                    <div className="info-item">
                      <span className="label">Name:</span>
                      <span className="value">{foundPatient.first_name} {foundPatient.last_name}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">Patient ID:</span>
                      <span className="value patient-id">{foundPatient.patient_id}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">Email:</span>
                      <span className="value">{foundPatient.email}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">Phone:</span>
                      <span className="value">{foundPatient.phone}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">Age:</span>
                      <span className="value">{foundPatient.age} years</span>
                    </div>
                    <div className="info-item">
                      <span className="label">Gender:</span>
                      <span className="value">{foundPatient.gender}</span>
                    </div>
                    {foundPatient.blood_group && (
                      <div className="info-item">
                        <span className="label">Blood Group:</span>
                        <span className="value">{foundPatient.blood_group}</span>
                      </div>
                    )}
                    {foundPatient.address && (
                      <div className="info-item">
                        <span className="label">Address:</span>
                        <span className="value">{foundPatient.address}</span>
                      </div>
                    )}
                  </div>
                  <button className="action-btn" onClick={() => onPatientSelected?.(foundPatient)}>
                    📅 Book Appointment for this Patient
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <style>{`
        .registration-page {
          min-height: 100vh;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          padding: 0;
        }

        .registration-header {
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

        .registration-container {
          max-width: 900px;
          margin: -30px auto 40px;
          padding: 40px;
          background: white;
          border-radius: 15px;
          box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        }

        .tabs-container {
          display: flex;
          gap: 15px;
          margin-bottom: 40px;
          border-bottom: 2px solid #eee;
        }

        .tab-btn {
          background: none;
          border: none;
          padding: 15px 30px;
          font-size: 1rem;
          font-weight: 600;
          color: #666;
          cursor: pointer;
          transition: all 0.3s ease;
          border-bottom: 3px solid transparent;
          display: flex;
          align-items: center;
          gap: 10px;
          margin-bottom: -2px;
        }

        .tab-btn:hover {
          color: #667eea;
        }

        .tab-btn.active {
          color: #667eea;
          border-bottom-color: #667eea;
        }

        .tab-icon {
          font-size: 1.3rem;
        }

        .alert {
          padding: 15px 20px;
          border-radius: 8px;
          margin-bottom: 25px;
          font-weight: 500;
          animation: slideIn 0.3s ease;
        }

        .alert-success {
          background: #d4edda;
          color: #155724;
          border: 1px solid #c3e6cb;
        }

        .alert-error {
          background: #f8d7da;
          color: #721c24;
          border: 1px solid #f5c6cb;
        }

        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .registration-form,
        .lookup-form {
          animation: fadeIn 0.4s ease;
        }

        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }

        .form-section {
          margin-bottom: 35px;
        }

        .form-section h3 {
          font-size: 1.2rem;
          color: #333;
          margin: 0 0 20px 0;
          padding-bottom: 10px;
          border-bottom: 2px solid #667eea;
        }

        .form-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
          gap: 20px;
        }

        .form-group {
          display: flex;
          flex-direction: column;
        }

        .form-group label {
          margin-bottom: 8px;
          font-weight: 600;
          color: #333;
          font-size: 0.95rem;
        }

        .form-group input,
        .form-group select {
          padding: 12px 15px;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          font-size: 1rem;
          transition: all 0.3s ease;
          background: white;
          color: #333;
        }

        .form-group input:focus,
        .form-group select:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .form-group input::placeholder {
          color: #999;
        }

        .submit-btn {
          width: 100%;
          padding: 14px 30px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 1.05rem;
          font-weight: 700;
          cursor: pointer;
          transition: all 0.3s ease;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 10px;
          margin-top: 30px;
        }

        .submit-btn:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        .submit-btn:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }

        .spinner {
          display: inline-block;
          width: 16px;
          height: 16px;
          border: 3px solid rgba(255, 255, 255, 0.3);
          border-radius: 50%;
          border-top-color: white;
          animation: spin 0.6s linear infinite;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        /* Lookup Styles */
        .lookup-section {
          animation: fadeIn 0.4s ease;
        }

        .lookup-header {
          text-align: center;
          margin-bottom: 30px;
        }

        .lookup-header h3 {
          font-size: 1.5rem;
          color: #333;
          margin: 0 0 10px 0;
        }

        .lookup-header p {
          color: #666;
          margin: 0;
        }

        .search-options {
          display: flex;
          gap: 15px;
          margin-bottom: 30px;
          justify-content: center;
        }

        .search-options .option {
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 12px 20px;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.3s ease;
          background: white;
        }

        .search-options .option:hover {
          border-color: #667eea;
          background: #f8f9ff;
        }

        .search-options .option.active {
          background: #667eea;
          color: white;
          border-color: #667eea;
        }

        .search-options input[type="radio"] {
          cursor: pointer;
          width: 18px;
          height: 18px;
        }

        .search-input-group {
          display: flex;
          gap: 10px;
          margin-bottom: 30px;
        }

        .search-input-group input {
          flex: 1;
          padding: 14px 18px;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          font-size: 1rem;
          transition: all 0.3s ease;
        }

        .search-input-group input:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .search-btn {
          padding: 14px 30px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 8px;
          font-weight: 700;
          cursor: pointer;
          transition: all 0.3s ease;
          white-space: nowrap;
        }

        .search-btn:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        .search-btn:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }

        /* Patient Card */
        .patient-card {
          margin-top: 30px;
          border: 2px solid #667eea;
          border-radius: 12px;
          overflow: hidden;
          animation: slideUp 0.3s ease;
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .card-header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 20px;
        }

        .card-header h3 {
          margin: 0;
          font-size: 1.3rem;
        }

        .card-content {
          padding: 25px;
        }

        .patient-info-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 20px;
          margin-bottom: 25px;
        }

        .info-item {
          background: #f8f9ff;
          padding: 15px;
          border-radius: 8px;
          border-left: 4px solid #667eea;
        }

        .info-item .label {
          display: block;
          color: #666;
          font-size: 0.9rem;
          font-weight: 600;
          margin-bottom: 5px;
        }

        .info-item .value {
          display: block;
          color: #333;
          font-size: 1.05rem;
          font-weight: 500;
        }

        .patient-id {
          font-family: 'Courier New', monospace;
          background: #667eea;
          color: white;
          padding: 4px 8px;
          border-radius: 4px;
          display: inline-block;
        }

        .action-btn {
          width: 100%;
          padding: 14px 20px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 1rem;
          font-weight: 700;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .action-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        @media (max-width: 768px) {
          .registration-header {
            padding: 30px 20px;
          }

          .header-content h1 {
            font-size: 1.8rem;
          }

          .registration-container {
            margin: -20px 15px 30px;
            padding: 25px;
          }

          .form-grid {
            grid-template-columns: 1fr;
          }

          .search-options {
            flex-direction: column;
          }

          .search-input-group {
            flex-direction: column;
          }

          .tabs-container {
            flex-wrap: wrap;
          }

          .patient-info-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  )
}

export default PatientRegistration
