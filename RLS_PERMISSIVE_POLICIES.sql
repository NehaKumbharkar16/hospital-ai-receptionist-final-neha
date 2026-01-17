-- =====================================================
-- CREATE PERMISSIVE RLS POLICIES - ALTERNATIVE FIX
-- =====================================================
-- If disabling RLS didn't work, create policies that allow all access

-- Enable RLS first (if not already enabled)
ALTER TABLE public.patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.doctors ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.departments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.specializations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.hospital_info ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.doctor_slots ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.patient_visits ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.hospital_statistics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.recommended_tests ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.symptom_department_mapping ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- CREATE PERMISSIVE POLICIES FOR PATIENTS TABLE
-- =====================================================

DROP POLICY IF EXISTS "Allow all for patients" ON public.patients;
CREATE POLICY "Allow all for patients" ON public.patients
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- =====================================================
-- CREATE PERMISSIVE POLICIES FOR DOCTORS TABLE
-- =====================================================

DROP POLICY IF EXISTS "Allow all for doctors" ON public.doctors;
CREATE POLICY "Allow all for doctors" ON public.doctors
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- =====================================================
-- CREATE PERMISSIVE POLICIES FOR APPOINTMENTS TABLE
-- =====================================================

DROP POLICY IF EXISTS "Allow all for appointments" ON public.appointments;
CREATE POLICY "Allow all for appointments" ON public.appointments
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- =====================================================
-- CREATE PERMISSIVE POLICIES FOR DEPARTMENTS TABLE
-- =====================================================

DROP POLICY IF EXISTS "Allow all for departments" ON public.departments;
CREATE POLICY "Allow all for departments" ON public.departments
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- =====================================================
-- CREATE PERMISSIVE POLICIES FOR OTHER TABLES
-- =====================================================

DROP POLICY IF EXISTS "Allow all for specializations" ON public.specializations;
CREATE POLICY "Allow all for specializations" ON public.specializations
  FOR ALL
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for chat_sessions" ON public.chat_sessions;
CREATE POLICY "Allow all for chat_sessions" ON public.chat_sessions
  FOR ALL
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for hospital_info" ON public.hospital_info;
CREATE POLICY "Allow all for hospital_info" ON public.hospital_info
  FOR ALL
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for doctor_slots" ON public.doctor_slots;
CREATE POLICY "Allow all for doctor_slots" ON public.doctor_slots
  FOR ALL
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for patient_visits" ON public.patient_visits;
CREATE POLICY "Allow all for patient_visits" ON public.patient_visits
  FOR ALL
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for ai_recommendations" ON public.ai_recommendations;
CREATE POLICY "Allow all for ai_recommendations" ON public.ai_recommendations
  FOR ALL
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for feedback" ON public.feedback;
CREATE POLICY "Allow all for feedback" ON public.feedback
  FOR ALL
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for hospital_statistics" ON public.hospital_statistics;
CREATE POLICY "Allow all for hospital_statistics" ON public.hospital_statistics
  FOR ALL
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for recommended_tests" ON public.recommended_tests;
CREATE POLICY "Allow all for recommended_tests" ON public.recommended_tests
  FOR ALL
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for symptom_department_mapping" ON public.symptom_department_mapping;
CREATE POLICY "Allow all for symptom_department_mapping" ON public.symptom_department_mapping
  FOR ALL
  USING (true)
  WITH CHECK (true);

-- =====================================================
-- GRANT PERMISSIONS
-- =====================================================

GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon;
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;
