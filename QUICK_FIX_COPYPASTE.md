# QUICK FIX - COPY & PASTE READY

⚠️ **IMPORTANT**: Copy ONLY the SQL code below - NOT the markdown headers or instructions

---

## SQL CODE TO EXECUTE IN SUPABASE

Copy everything between the dashed lines below and paste into Supabase SQL Editor:

---

```
-- COMPLETE RLS FIX - Execute this once
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

GRANT USAGE ON SCHEMA public TO postgres, anon, authenticated, service_role;
GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres, anon, authenticated, service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO postgres, anon, authenticated, service_role;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO postgres, anon, authenticated, service_role;

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

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO postgres, anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO postgres, anon, authenticated, service_role;
```

---

## STEPS TO EXECUTE

1. **Open Supabase**: https://app.supabase.com/
2. **Select Project**: NehaKumbharkar16's New_Project
3. **Go to SQL Editor**: Left sidebar → SQL Editor
4. **New Query**: Click "New Query" button
5. **Paste SQL**: Paste the code from above (NOT the markdown)
6. **Run**: Click the RUN button (blue play icon)
7. **Wait**: Look for "Success. No rows returned" message

---

## THEN: RESTART RENDER SERVICE

1. **Open Render**: https://dashboard.render.com
2. **Select Service**: Hospital AI Agent
3. **Settings**: Click Settings button (top right)
4. **Restart**: Scroll to "Danger Zone" → Click "Restart Service"
5. **Wait**: 1-2 minutes for green "Live" status
6. **Deploy**: Click "Manual Deploy" button

---

## FINALLY: TEST REGISTRATION

1. **Go to**: https://hospital-ai-receptionist-final.onrender.com
2. **Click**: Register tab
3. **Fill in test patient**:
   - Email: test@example.com
   - First Name: Test
   - Last Name: User
   - Phone: 5551234567
   - Age: 30
   - Gender: Male
4. **Submit**: Click Register button
5. **Check Result**: 
   - ✅ SUCCESS = See patient ID returned
   - ❌ FAILURE = See permission error

---

## IF IT STILL FAILS

Run diagnostic tool locally:

```
cd "d:\Program\Hospital AI Agent Cursor"
python rls_diagnostic.py
```

This will show:
- RLS status for each table
- All active RLS policies  
- Whether write operations work
