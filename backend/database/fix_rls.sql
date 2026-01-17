-- Fix RLS (Row Level Security) Issues
-- This script disables RLS on key tables to allow application access

-- Disable RLS on patients table
ALTER TABLE patients DISABLE ROW LEVEL SECURITY;

-- Disable RLS on doctors table
ALTER TABLE doctors DISABLE ROW LEVEL SECURITY;

-- Disable RLS on appointments table
ALTER TABLE appointments DISABLE ROW LEVEL SECURITY;

-- Disable RLS on doctor_slots table
ALTER TABLE doctor_slots DISABLE ROW LEVEL SECURITY;

-- Disable RLS on chat_sessions table
ALTER TABLE chat_sessions DISABLE ROW LEVEL SECURITY;

-- Disable RLS on all other tables
ALTER TABLE departments DISABLE ROW LEVEL SECURITY;
ALTER TABLE specializations DISABLE ROW LEVEL SECURITY;
ALTER TABLE symptom_department_mapping DISABLE ROW LEVEL SECURITY;
ALTER TABLE patient_visits DISABLE ROW LEVEL SECURITY;
ALTER TABLE recommended_tests DISABLE ROW LEVEL SECURITY;
ALTER TABLE ai_recommendations DISABLE ROW LEVEL SECURITY;
ALTER TABLE feedback DISABLE ROW LEVEL SECURITY;
ALTER TABLE hospital_statistics DISABLE ROW LEVEL SECURITY;

-- Create hospital_info table (if it doesn't exist)
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

-- Insert default hospital info if table is empty
INSERT INTO hospital_info (hospital_name, phone, email)
SELECT 'City Hospital', '+1-800-HOSPITAL', 'info@cityhospital.com'
WHERE NOT EXISTS (SELECT 1 FROM hospital_info);

-- Disable RLS on hospital_info
ALTER TABLE hospital_info DISABLE ROW LEVEL SECURITY;

-- Grant permissions to anon role (public access)
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon;
GRANT ALL ON ALL ROUTINES IN SCHEMA public TO anon;

-- Grant permissions to authenticated role
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL ROUTINES IN SCHEMA public TO authenticated;
