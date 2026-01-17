-- =====================================================
-- PERMANENT RLS DISABLE - FOR PRODUCTION
-- =====================================================
-- Run this in Supabase SQL Editor to PERMANENTLY disable RLS
-- This ensures both development and production work correctly

-- Drop all existing policies first (if any)
DROP POLICY IF EXISTS "Enable insert for all users" ON public.patients;
DROP POLICY IF EXISTS "Enable read for all users" ON public.patients;
DROP POLICY IF EXISTS "Enable update for all users" ON public.patients;
DROP POLICY IF EXISTS "Enable delete for all users" ON public.patients;

DROP POLICY IF EXISTS "Enable insert for all users" ON public.doctors;
DROP POLICY IF EXISTS "Enable read for all users" ON public.doctors;
DROP POLICY IF EXISTS "Enable update for all users" ON public.doctors;
DROP POLICY IF EXISTS "Enable delete for all users" ON public.doctors;

DROP POLICY IF EXISTS "Enable insert for all users" ON public.appointments;
DROP POLICY IF EXISTS "Enable read for all users" ON public.appointments;
DROP POLICY IF EXISTS "Enable update for all users" ON public.appointments;
DROP POLICY IF EXISTS "Enable delete for all users" ON public.appointments;

DROP POLICY IF EXISTS "Enable insert for all users" ON public.departments;
DROP POLICY IF EXISTS "Enable read for all users" ON public.departments;
DROP POLICY IF EXISTS "Enable update for all users" ON public.departments;
DROP POLICY IF EXISTS "Enable delete for all users" ON public.departments;

DROP POLICY IF EXISTS "Enable insert for all users" ON public.chat_sessions;
DROP POLICY IF EXISTS "Enable read for all users" ON public.chat_sessions;
DROP POLICY IF EXISTS "Enable update for all users" ON public.chat_sessions;
DROP POLICY IF EXISTS "Enable delete for all users" ON public.chat_sessions;

DROP POLICY IF EXISTS "Enable insert for all users" ON public.specializations;
DROP POLICY IF EXISTS "Enable read for all users" ON public.specializations;
DROP POLICY IF EXISTS "Enable update for all users" ON public.specializations;
DROP POLICY IF EXISTS "Enable delete for all users" ON public.specializations;

-- =====================================================
-- DISABLE RLS ON ALL TABLES
-- =====================================================

ALTER TABLE IF EXISTS public.patients DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.doctors DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.appointments DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.departments DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.specializations DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.symptom_department_mapping DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.doctor_slots DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.patient_visits DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.recommended_tests DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.ai_recommendations DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.feedback DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.hospital_statistics DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.chat_sessions DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.hospital_info DISABLE ROW LEVEL SECURITY;

-- =====================================================
-- GRANT FULL PERMISSIONS
-- =====================================================

GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT USAGE ON SCHEMA public TO postgres;

GRANT ALL ON ALL TABLES IN SCHEMA public TO anon;
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres;

GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO postgres;

GRANT ALL ON ALL ROUTINES IN SCHEMA public TO anon;
GRANT ALL ON ALL ROUTINES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL ROUTINES IN SCHEMA public TO postgres;

-- =====================================================
-- VERIFICATION
-- =====================================================
-- After running this, you should see no RLS policies listed
-- Go to Authentication → Policies to verify all tables show "RLS DISABLED"
