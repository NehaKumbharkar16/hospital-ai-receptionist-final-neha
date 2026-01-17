# RENDER ENVIRONMENT VARIABLE SETUP - STEP BY STEP

## Your Credentials (Ready to Copy)

```
SUPABASE_URL = https://svixrgqmbxfnpqpcyimk.supabase.co

SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN2aXhyZ3FtYnhmbnBxcGN5aW1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgwNDk2MDcsImV4cCI6MjA4MzYyNTYwN30.GOTzgfC8ew5QoMeayF-Wpl3VZwbDsl46y7blFlvyVBU

SUPABASE_SERVICE_ROLE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN2aXhyZ3FtYnhmbnBxcGN5aW1rIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODA0OTYwNywiZXhwIjoyMDgzNjI1NjA3fQ.qqNlKwkl9K-6-0cCnVyJNvJ5YgIgdt-tmoZENpmauAk

GOOGLE_API_KEY = AIzaSyCgefitlyeOHwB-kwSY73D2sY8qD6UJaRs
```

## Steps to Fix Render

### 1️⃣ Go to Render Dashboard
- Open: https://dashboard.render.com
- Click your **Hospital AI Agent** service
- Click **"Settings"** (in the top menu or sidebar)

### 2️⃣ Find Environment Variables
- Look for **"Environment"** section (or **"Environment Variables"**)
- You should see a form to add variables

### 3️⃣ Add Each Variable
Copy and paste these exactly (one at a time):

**Variable 1: SUPABASE_URL**
```
Name: SUPABASE_URL
Value: https://svixrgqmbxfnpqpcyimk.supabase.co
```
Click **"Add"**

**Variable 2: SUPABASE_ANON_KEY**
```
Name: SUPABASE_ANON_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN2aXhyZ3FtYnhmbnBxcGN5aW1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgwNDk2MDcsImV4cCI6MjA4MzYyNTYwN30.GOTzgfC8ew5QoMeayF-Wpl3VZwbDsl46y7blFlvyVBU
```
Click **"Add"**

**Variable 3: SUPABASE_SERVICE_ROLE_KEY** ⭐ IMPORTANT
```
Name: SUPABASE_SERVICE_ROLE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN2aXhyZ3FtYnhmbnBxcGN5aW1rIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODA0OTYwNywiZXhwIjoyMDgzNjI1NjA3fQ.qqNlKwkl9K-6-0cCnVyJNvJ5YgIgdt-tmoZENpmauAk
```
Click **"Add"**

**Variable 4: GOOGLE_API_KEY**
```
Name: GOOGLE_API_KEY
Value: AIzaSyCgefitlyeOHwB-kwSY73D2sY8qD6UJaRs
```
Click **"Add"**

### 4️⃣ Save Changes
- Click **"Save"** or **"Save Changes"** button
- Wait for confirmation

### 5️⃣ Redeploy
- Go back to your service page
- Click **"Manual Deploy"** button
- Wait 2-3 minutes for deployment to complete
- Check the **"Logs"** tab

### 6️⃣ Verify in Logs
Look for these lines:
```
[DATABASE] ✅ Connected with anon key (read operations)
[DATABASE] ✅ Connected with service role key (write operations)
```

### 7️⃣ Test
Try registering a patient at:
https://hospital-ai-receptionist-final.onrender.com

Should work now! ✅

---

## Troubleshooting

### "SERVICE_ROLE_KEY NOT FOUND" in logs?
- Check if you copied the full value (should be ~219 characters)
- Make sure variable name is exactly: `SUPABASE_SERVICE_ROLE_KEY` (no spaces)
- Click Save again and Manual Deploy

### Still getting permission denied?
- Check Render logs for the exact error
- Verify all 4 variables are set
- Try copying from this guide again (make sure no extra spaces)

### Nothing changed after Manual Deploy?
- Wait full 3 minutes
- Hard refresh browser: **Ctrl+Shift+R**
- Check if "Manual Deploy" actually started (should see building...)
