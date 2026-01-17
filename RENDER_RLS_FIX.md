# Hospital AI Agent - Render Deployment Fix

## Problem
Getting `permission denied for table patients` error (code 42501) on Render

## Root Cause
RLS (Row Level Security) is blocking database access on the production Supabase instance

## Solution

### Option 1: Quick Fix (Recommended)
1. Go to: https://app.supabase.com
2. Select your project
3. Go to **SQL Editor** → **New Query**
4. Copy the entire content from: `PERMANENT_RLS_FIX.sql`
5. Click **Run** (wait for success)
6. Go to Render dashboard
7. Click your **Hospital AI Agent** project
8. Click **Manual Deploy** or wait for auto-redeploy
9. Wait 2-3 minutes for deployment to complete
10. Test by registering a patient

### Option 2: Disable RLS via UI
1. Go to https://app.supabase.com
2. Click **Authentication** → **Policies**
3. For EACH table, click the table name
4. Click **"Disable RLS"** button
5. Repeat for:
   - patients
   - doctors
   - appointments
   - departments
   - chat_sessions
   - specializations
   - symptom_department_mapping
   - hospital_info
   - doctor_slots
   - patient_visits
   - ai_recommendations
   - feedback
   - hospital_statistics
   - recommended_tests

### Option 3: Check Render Environment Variables
1. Go to Render dashboard
2. Select your Hospital AI Agent service
3. Click **Environment** (or **Settings**)
4. Verify these are set:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `GOOGLE_API_KEY`

If missing, add them from your `backend/.env` file

### Option 4: Force Redeploy
1. Go to Render dashboard
2. Select Hospital AI Agent service
3. Click **"Manual Deploy"** button
4. Wait for deployment to complete (should take 2-3 minutes)

## Verification
After fix, test with:
```bash
curl -X POST http://your-render-url/api/patients/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "9999999999",
    "age": 30,
    "gender": "male"
  }'
```

Should return patient data (not a 500 error)

## Still Having Issues?

### Check Logs
1. Go to Render dashboard
2. Click your service
3. Click **Logs**
4. Look for error messages

### Check Database
Run this locally:
```bash
python final_verify.py
```

Should show ✅ all tables accessible

### Nuclear Option
If nothing works:
1. Go to Supabase dashboard
2. Settings → Migrate Data → Reset Database
3. Re-run the `SETUP_DATABASE.sql` script
4. Then run `PERMANENT_RLS_FIX.sql`
5. Redeploy on Render

## Prevention
To prevent RLS issues in future:
1. Always use `get_supabase_admin()` for writes
2. Check RLS status before deploying
3. Have RLS disabled in production (or use proper policies)

---

**Need Help?** Check the logs on both Render and Supabase
