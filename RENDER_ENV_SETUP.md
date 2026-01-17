# ⚠️ RENDER ENVIRONMENT VARIABLES - CRITICAL FIX

## The Problem
Render is getting "permission denied" because **SUPABASE_SERVICE_ROLE_KEY is not set** in Render's environment.

On Render:
- `.env` files don't exist (not deployed)
- Environment variables must be set in Render dashboard
- The app can't write without the SERVICE_ROLE_KEY

## The Solution - Set Render Environment Variables

### Step 1: Get Your Credentials
Open your local `backend/.env` file and find:
```
SUPABASE_URL=https://svixrgqmbxfnpqpcyimk.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN2aXhyZ3FtYnhmbnBxcGN5aW1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgwNDk2MDcsImV4cCI6MjA4MzYyNTYwN30.GOTzgfC8ew5QoMeayF-Wpl3VZwbDsl46y7blFlvyVBU
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN2aXhyZ3FtYnhmbnBxcGN5aW1rIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODA0OTYwNywiZXhwIjoyMDgzNjI1NjA3fQ.qqNlKwkl9K-6-0cCnVyJNvJ5YgIgdt-tmoZENpmauAk
GOOGLE_API_KEY=AIzaSyCgefitlyeOHwB-kwSY73D2sY8qD6UJaRs
```

### Step 2: Set Variables in Render
1. Go to: https://dashboard.render.com
2. Click **Hospital AI Agent** service
3. Click **Environment** (in left sidebar)
4. Add these 4 environment variables:

| Name | Value |
|------|-------|
| `SUPABASE_URL` | `https://svixrgqmbxfnpqpcyimk.supabase.co` |
| `SUPABASE_ANON_KEY` | (copy from backend/.env) |
| `SUPABASE_SERVICE_ROLE_KEY` | (copy from backend/.env) |
| `GOOGLE_API_KEY` | (copy from backend/.env) |

**Important:** Copy the FULL value, including the entire JWT token

### Step 3: Save and Deploy
1. Click **Save Changes**
2. Go back to service page
3. Click **Manual Deploy**
4. Wait 2-3 minutes for deployment
5. Check logs to verify: "[DATABASE] ✅ Connected with service role key"

### Step 4: Test
Try registering a patient:
```bash
curl -X POST https://hospital-ai-receptionist-final.onrender.com/api/patients/register \
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

Should return patient data (not 500 error)

## Verify in Logs
After redeploy, go to **Logs** and look for:
```
[DATABASE] ✅ Connected with anon key
[DATABASE] ✅ Connected with service role key
```

If you see:
```
[DATABASE] ❌ SERVICE ROLE KEY NOT FOUND - WRITES WILL FAIL
```

Then the environment variable wasn't set correctly. Go back to Step 2 and check you copied the full value.

## Common Mistakes
❌ Copied only part of the token  
❌ Added extra spaces before/after  
❌ Used wrong variable name  
❌ Didn't click "Save Changes"  
❌ Didn't click "Manual Deploy"  

## Still Not Working?
1. Check Render logs for the exact error
2. Verify all 4 variables are set
3. Make sure SERVICE_ROLE_KEY is not empty
4. Try copying the value again (make sure entire JWT token is included)
5. Wait full 3 minutes after deploy before testing

---
**Key Point:** Without SUPABASE_SERVICE_ROLE_KEY in Render environment, the app can only use the anon key, which respects RLS and gets blocked even though RLS is disabled!
