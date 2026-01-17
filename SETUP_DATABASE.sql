-- =====================================================
-- HOSPITAL AI AGENT - COMPLETE DATABASE SETUP
-- =====================================================
-- Copy and paste this entire script in Supabase SQL Editor
-- Go to: https://app.supabase.com → SQL Editor → New Query
-- =====================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- CREATE ALL TABLES
-- =====================================================

-- Departments Table
CREATE TABLE IF NOT EXISTS departments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    head_doctor_id UUID,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Specializations Table
CREATE TABLE IF NOT EXISTS specializations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    department_id UUID REFERENCES departments(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Symptom to Department Mapping
CREATE TABLE IF NOT EXISTS symptom_department_mapping (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symptom VARCHAR(100) NOT NULL,
    department_id UUID NOT NULL REFERENCES departments(id),
    priority VARCHAR(20) DEFAULT 'normal',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Doctors Table
CREATE TABLE IF NOT EXISTS doctors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    specialization_id UUID REFERENCES specializations(id),
    department_id UUID NOT NULL REFERENCES departments(id),
    qualification TEXT,
    experience_years INT,
    opd_start_time TIME,
    opd_end_time TIME,
    consultation_fee INT,
    available_days VARCHAR(50),
    is_on_leave BOOLEAN DEFAULT FALSE,
    leave_start_date DATE,
    leave_end_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Doctor Availability Slots
CREATE TABLE IF NOT EXISTS doctor_slots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    doctor_id UUID NOT NULL REFERENCES doctors(id),
    slot_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    capacity INT DEFAULT 1,
    booked INT DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Patients Table
CREATE TABLE IF NOT EXISTS patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10),
    blood_group VARCHAR(5),
    address TEXT,
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    medical_history TEXT,
    allergies TEXT,
    has_emergency_flag BOOLEAN DEFAULT FALSE,
    emergency_description TEXT,
    preferred_department_id UUID REFERENCES departments(id),
    registration_date TIMESTAMP DEFAULT NOW(),
    last_visit_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Patient Visits Table
CREATE TABLE IF NOT EXISTS patient_visits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id UUID NOT NULL REFERENCES doctors(id),
    appointment_id UUID,
    visit_date TIMESTAMP DEFAULT NOW(),
    symptoms TEXT,
    diagnosis TEXT,
    treatment TEXT,
    prescribed_tests TEXT,
    prescribed_medicines TEXT,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'completed',
    visit_type VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Appointments Table
CREATE TABLE IF NOT EXISTS appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    appointment_number VARCHAR(20) UNIQUE NOT NULL,
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id UUID NOT NULL REFERENCES doctors(id),
    department_id UUID NOT NULL REFERENCES departments(id),
    appointment_date TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled',
    reason_for_visit TEXT,
    priority VARCHAR(20) DEFAULT 'normal',
    room_number VARCHAR(10),
    confirmation_sent BOOLEAN DEFAULT FALSE,
    confirmation_method VARCHAR(20),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Recommended Tests
CREATE TABLE IF NOT EXISTS recommended_tests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- AI Recommendations
CREATE TABLE IF NOT EXISTS ai_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    visit_id UUID REFERENCES patient_visits(id),
    symptom_analysis TEXT,
    severity VARCHAR(20),
    recommended_department_id UUID REFERENCES departments(id),
    recommended_doctor_id UUID REFERENCES doctors(id),
    recommended_tests TEXT,
    immediate_actions TEXT,
    confidence_score DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Patient Feedback
CREATE TABLE IF NOT EXISTS feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    visit_id UUID REFERENCES patient_visits(id),
    doctor_id UUID,
    appointment_id UUID,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    feedback_text TEXT,
    categories VARCHAR(255),
    suggestions TEXT,
    is_anonymous BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Hospital Statistics
CREATE TABLE IF NOT EXISTS hospital_statistics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    statistic_date DATE DEFAULT CURRENT_DATE,
    total_patients_today INT DEFAULT 0,
    total_appointments_today INT DEFAULT 0,
    emergency_cases INT DEFAULT 0,
    completed_visits INT DEFAULT 0,
    average_wait_time INT,
    available_doctors INT DEFAULT 0,
    occupied_rooms INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Chat Sessions
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(50) UNIQUE NOT NULL,
    patient_id UUID REFERENCES patients(id),
    conversation_data JSONB,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Hospital Info
CREATE TABLE IF NOT EXISTS hospital_info (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hospital_name VARCHAR(200) NOT NULL DEFAULT 'City Hospital',
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(200),
    established_year INT,
    total_beds INT,
    ambulance_count INT,
    operating_theatres INT,
    icu_beds INT,
    description TEXT,
    logo_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- CREATE INDEXES
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_patients_email ON patients(email);
CREATE INDEX IF NOT EXISTS idx_patients_phone ON patients(phone);
CREATE INDEX IF NOT EXISTS idx_patients_patient_id ON patients(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_doctor ON appointments(doctor_id);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date);
CREATE INDEX IF NOT EXISTS idx_doctor_slots_doctor ON doctor_slots(doctor_id);
CREATE INDEX IF NOT EXISTS idx_doctor_slots_date ON doctor_slots(slot_date);
CREATE INDEX IF NOT EXISTS idx_visits_patient ON patient_visits(patient_id);
CREATE INDEX IF NOT EXISTS idx_visits_doctor ON patient_visits(doctor_id);
CREATE INDEX IF NOT EXISTS idx_feedback_patient ON feedback(patient_id);
CREATE INDEX IF NOT EXISTS idx_chat_session_id ON chat_sessions(session_id);

-- =====================================================
-- CREATE FUNCTIONS AND TRIGGERS
-- =====================================================

-- Function to auto-generate patient ID
CREATE OR REPLACE FUNCTION generate_patient_id()
RETURNS TRIGGER AS $$
BEGIN
    NEW.patient_id := 'PAT' || LPAD(CAST((EXTRACT(EPOCH FROM NOW())::INT % 100000) AS VARCHAR), 5, '0');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for patient ID generation
DROP TRIGGER IF EXISTS trigger_patient_id ON patients;
CREATE TRIGGER trigger_patient_id
BEFORE INSERT ON patients
FOR EACH ROW
EXECUTE FUNCTION generate_patient_id();

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at columns
DROP TRIGGER IF EXISTS trigger_patients_updated_at ON patients;
CREATE TRIGGER trigger_patients_updated_at
BEFORE UPDATE ON patients
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS trigger_doctors_updated_at ON doctors;
CREATE TRIGGER trigger_doctors_updated_at
BEFORE UPDATE ON doctors
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS trigger_appointments_updated_at ON appointments;
CREATE TRIGGER trigger_appointments_updated_at
BEFORE UPDATE ON appointments
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- DISABLE RLS ON ALL TABLES
-- =====================================================

ALTER TABLE patients DISABLE ROW LEVEL SECURITY;
ALTER TABLE doctors DISABLE ROW LEVEL SECURITY;
ALTER TABLE appointments DISABLE ROW LEVEL SECURITY;
ALTER TABLE doctor_slots DISABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions DISABLE ROW LEVEL SECURITY;
ALTER TABLE departments DISABLE ROW LEVEL SECURITY;
ALTER TABLE specializations DISABLE ROW LEVEL SECURITY;
ALTER TABLE symptom_department_mapping DISABLE ROW LEVEL SECURITY;
ALTER TABLE patient_visits DISABLE ROW LEVEL SECURITY;
ALTER TABLE recommended_tests DISABLE ROW LEVEL SECURITY;
ALTER TABLE ai_recommendations DISABLE ROW LEVEL SECURITY;
ALTER TABLE feedback DISABLE ROW LEVEL SECURITY;
ALTER TABLE hospital_statistics DISABLE ROW LEVEL SECURITY;
ALTER TABLE hospital_info DISABLE ROW LEVEL SECURITY;

-- =====================================================
-- GRANT PERMISSIONS
-- =====================================================

GRANT ALL ON ALL TABLES IN SCHEMA public TO anon;
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- =====================================================
-- INSERT DEFAULT DATA
-- =====================================================

INSERT INTO hospital_info (hospital_name, phone, email, address, total_beds, ambulance_count, operating_theatres)
VALUES ('City Hospital', '+1-800-HOSPITAL', 'info@cityhospital.com', '123 Main Street, Medical City', 500, 10, 8)
ON CONFLICT DO NOTHING;

-- Insert sample departments
INSERT INTO departments (name, description) VALUES
('General Medicine', 'General medical care and treatment'),
('Cardiology', 'Heart and cardiovascular diseases'),
('Orthopedics', 'Bone, joint, and muscle disorders'),
('Pediatrics', 'Child healthcare and treatment'),
('Gynecology', 'Women health and childbirth'),
('Emergency', 'Emergency and trauma care')
ON CONFLICT (name) DO NOTHING;

-- =====================================================
-- DATABASE SETUP COMPLETE
-- =====================================================
-- If you see "Success. No errors." message above,
-- your database is now fully configured!
-- 
-- Next steps:
-- 1. Close this SQL Editor
-- 2. Run: python check_and_fix_db.py
-- 3. Your Hospital AI Agent is ready to use!
-- =====================================================
