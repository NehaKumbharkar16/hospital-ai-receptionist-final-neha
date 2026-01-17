# 🏥 HOSPITAL AI AGENT - DATABASE SETUP FIX

## ⚠️ Problem
You're getting this error:
```
ERROR: 42P01: relation "symptom_department_mapping" does not exist
```

This means **ALL the database tables need to be created first**.

---

## ✅ Solution - Follow These Steps:

### Step 1: Open Supabase SQL Editor
1. Go to: **https://app.supabase.com**
2. Select your **Hospital AI Agent project**
3. Click **SQL Editor** (left sidebar)
4. Click **New Query**

### Step 2: Copy Complete Setup SQL
1. Open file: `SETUP_DATABASE.sql` in this directory
2. Copy the **entire content**

### Step 3: Paste & Execute
1. Paste into Supabase SQL Editor
2. Click **Run** button
3. Wait for "Success. No errors." message

### Step 4: Verify Setup
After SQL finishes successfully, run:
```bash
python check_and_fix_db.py
```

---

## 📋 What This Does
The SQL script will:
- ✅ Create all 14 database tables
- ✅ Create indexes for performance
- ✅ Create automatic triggers
- ✅ Disable RLS (Row Level Security)
- ✅ Grant proper permissions
- ✅ Insert sample data (departments, hospital info)

---

## 🎯 Expected Result
After completion, you'll see:
```
✅ patients              Connected
✅ doctors               Connected
✅ appointments          Connected
✅ hospital_info         Connected
✅ departments           Connected
```

---

## 🆘 Still Having Issues?

If you get an error about **"already exists"**, that's fine - just continue.
If you get a **permission error**, the RLS disable part may not have worked.

### Manual RLS Fix (if needed):
1. Go to Supabase: **Authentication** → **Policies**
2. For each table, click **"Disable RLS"**
3. Or create a new query in SQL Editor and run:

```sql
ALTER TABLE patients DISABLE ROW LEVEL SECURITY;
ALTER TABLE doctors DISABLE ROW LEVEL SECURITY;
ALTER TABLE appointments DISABLE ROW LEVEL SECURITY;
ALTER TABLE departments DISABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions DISABLE ROW LEVEL SECURITY;
ALTER TABLE hospital_info DISABLE ROW LEVEL SECURITY;
```

---

## 📞 Need Help?
1. Check [Supabase Docs](https://supabase.com/docs)
2. Verify .env file has correct credentials
3. Re-run verification script

---

**Once setup is complete, your Hospital AI Agent will be fully operational!** 🚀
