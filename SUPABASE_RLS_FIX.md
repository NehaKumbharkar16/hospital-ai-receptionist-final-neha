# Fixing Supabase Row-Level Security (RLS) Error

## Problem
```
ERROR: new row violates row-level security policy for table "patients"
(code: '42501')
```

This error occurs when trying to insert patient data into the Supabase `patients` table. It happens because:
1. The table has Row-Level Security (RLS) enabled
2. The application was using only the `SUPABASE_ANON_KEY`, which has limited permissions
3. Server-side operations need the `SUPABASE_SERVICE_ROLE_KEY` to bypass RLS restrictions

## Solution

### 1. Get Your Service Role Key
1. Go to your Supabase project dashboard
2. Navigate to **Settings** → **API**
3. Copy the **Service Role Secret** (NOT the anon key)
4. ⚠️ **IMPORTANT**: Keep this key SECRET - only use it on the backend!

### 2. Update Environment Variables
Add the service role key to your `.env` file:

```env
SUPABASE_URL=your-project-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

For deployment on Render.com:
1. Go to your service dashboard
2. Navigate to **Environment** → **Environment Variables**
3. Add `SUPABASE_SERVICE_ROLE_KEY=your-service-role-key`

### 3. Code Changes (Already Applied)
The code has been updated to:
- Import `get_supabase_admin()` function
- Use the admin client (`supabase_admin`) for INSERT operations
- Continue using the anon client for read operations

The changes made:
- ✅ Updated `backend/database/__init__.py` to create both clients
- ✅ Updated `backend/routers/chat.py` to use admin client for inserts
- ✅ Updated `backend/env.template` with SERVICE_ROLE_KEY placeholder

### 4. (Optional) Alternative: Disable RLS
If you don't need RLS protection, you can disable it on the table:

1. Go to Supabase dashboard
2. Click on the `patients` table
3. Click the **🔓 RLS Disabled** toggle (top right)
4. Select **Disable RLS**

However, **using the service role key is the recommended approach** as it's more secure.

## Verification
After making changes:
1. Restart the backend server
2. Test the chat workflow to completion
3. Check for "SUCCESS: Patient data stored" in the logs
4. Verify the data appears in Supabase → `patients` table

## Security Notes
- **Service Role Key**: Server-side only. NEVER expose in frontend code or public repositories
- **Anon Key**: Safe to use in frontend. Has limited permissions by RLS policies
- Use environment variables, NOT hardcoded keys
- Add `.env` to `.gitignore`
