# RENDER DEPLOYMENT - RLS PERMISSION FIX

## What You're Seeing
✅ Supabase shows all tables as "UNRESTRICTED" (RLS disabled)
❌ But Render still gets "permission denied for table patients"

## Why This Happens
Render may be:
1. Using **old/cached credentials**
2. **Hasn't redeployed** after RLS was disabled
3. **Missing environment variables**
4. **Using wrong Supabase instance**

## SOLUTION - Do This Now:

### Step 1: Verify Render Environment Variables
1. Go to: https://dashboard.render.com
2. Click your **Hospital AI Agent** service
3. Click **Settings**
4. Scroll to **Environment Variables**
5. **Verify these exist:**
   - `SUPABASE_URL=https://svixrgqmbxfnpqpcyimk.supabase.co`
   - `SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (should be long)
   - `SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (should be long)
   - `GOOGLE_API_KEY=AIzaSyCgefitlyeOHwB-kwSY73D2sY8qD6UJaRs`

**If ANY are missing or wrong:**
- Edit and update from your `backend/.env` file
- Save

### Step 2: Force Redeploy
1. Go to Render dashboard
2. Click **Hospital AI Agent** service
3. Click **Manual Deploy** (top right button)
4. Wait for deployment to complete (2-3 minutes)
5. Watch the logs for any errors

### Step 3: Clear Cache
After redeploy:
1. Open https://hospital-ai-receptionist-final.onrender.com
2. Hard refresh: **Ctrl+Shift+R** (or Cmd+Shift+R on Mac)
3. Try registering a patient again

### Step 4: Test the Endpoint
If still getting error, test directly:

```bash
curl -X POST https://hospital-ai-receptionist-final.onrender.com/api/patients/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "Patient",
    "email": "test@example.com",
    "phone": "9999999999",
    "age": 30,
    "gender": "male"
  }'
```

Should return patient data, NOT a 500 error.

### Step 5: Check Render Logs
If still failing:
1. Go to Render dashboard
2. Click **Hospital AI Agent** service
3. Click **Logs**
4. Look for error details
5. Copy the error and share it

## If All Else Fails - Nuclear Option

### Option A: Update Render Environment
1. In Render dashboard, delete old env vars
2. Add fresh ones:
   - SUPABASE_URL: `https://svixrgqmbxfnpqpcyimk.supabase.co`
   - SUPABASE_ANON_KEY: (copy from your `.env`)
   - SUPABASE_SERVICE_ROLE_KEY: (copy from your `.env`)
   - GOOGLE_API_KEY: (copy from your `.env`)
3. Click **Save**
4. Click **Manual Deploy**
5. Test again

### Option B: Verify Supabase is Actually Fixed
Run this locally:
```bash
python final_verify.py
```

Should show all ✅ tables accessible.

If it shows ❌ still blocking, RLS wasn't actually disabled in Supabase.

### Option C: Re-Disable RLS in Supabase
1. Go to https://app.supabase.com
2. SQL Editor → New Query
3. Run PERMANENT_RLS_FIX.sql again
4. Click Run
5. Then redeploy Render

## Expected Result ✅
After these steps, registering a patient should work:
```json
{
  "id": "uuid-here",
  "patient_id": "PAT12345",
  "first_name": "Test",
  "last_name": "Patient",
  "email": "test@example.com",
  ...
}
```

## Still Stuck?
Check these:
1. **Supabase Status:** Is RLS really disabled? (should show "UNRESTRICTED")
2. **Render Logs:** Are there other errors besides permission denied?
3. **Environment Variables:** Are they actually saved in Render?
4. **Service Role Key:** Did you copy the full key (should be ~200 chars)?

---

**Most Common Fix:** Click "Manual Deploy" on Render after RLS is disabled in Supabase. Takes 2-3 minutes.
