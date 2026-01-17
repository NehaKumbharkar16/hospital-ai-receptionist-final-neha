-- =====================================================
-- NUCLEAR OPTION - COMPLETELY REMOVE ALL RLS RESTRICTIONS
-- =====================================================
-- This is the most aggressive approach - removes all policies and disables RLS entirely

-- First, drop EVERY policy on EVERY table
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (
        SELECT tablename FROM pg_tables WHERE schemaname = 'public'
    ) LOOP
        EXECUTE 'DROP POLICY IF EXISTS ' || quote_ident(r.tablename || '_policy') || ' ON public.' || quote_ident(r.tablename);
        EXECUTE 'DROP POLICY IF EXISTS "Allow all for ' || r.tablename || '" ON public.' || quote_ident(r.tablename);
    END LOOP;
END $$;

-- Disable RLS on all tables
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (
        SELECT tablename FROM pg_tables WHERE schemaname = 'public'
    ) LOOP
        EXECUTE 'ALTER TABLE public.' || quote_ident(r.tablename) || ' DISABLE ROW LEVEL SECURITY';
    END LOOP;
END $$;

-- Grant all permissions to all roles
GRANT USAGE ON SCHEMA public TO postgres, anon, authenticated, service_role;
GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres, anon, authenticated, service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO postgres, anon, authenticated, service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO postgres, anon, authenticated, service_role;

-- Force sequence permissions
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (
        SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema = 'public'
    ) LOOP
        EXECUTE 'GRANT ALL ON ' || quote_ident(r.sequence_name) || ' TO postgres, anon, authenticated, service_role';
    END LOOP;
END $$;

-- Make sure all table permissions are set
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO postgres, anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO postgres, anon, authenticated, service_role;
