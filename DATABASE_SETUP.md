# 🏥 Database Schema Setup - Required Action

Your patient registration is failing because the **database tables don't exist in Supabase yet**.

## What You Need To Do

### Step 1: Get the SQL Schema
The SQL schema is displayed when you run:
```bash
python apply_database_schema.py
```

Or you can directly open: `backend/database/schema.sql`

### Step 2: Apply Schema to Supabase

#### **Option A: Using Supabase Dashboard (Easiest - Recommended)** ✅

1. Go to: https://app.supabase.com/
2. Login and select your project
3. Click **SQL Editor** in the left sidebar
4. Click **New Query** button
5. Run this command to get the schema:
   ```bash
   python apply_database_schema.py
   ```
6. Copy **ALL** the SQL shown (from "COPY FROM HERE" to "COPY UNTIL HERE")
7. Paste it into the Supabase SQL Editor
8. Click **RUN** button
9. Wait for completion (should see success message)

#### **Option B: Using Command Line**

If you have `psql` installed:
```bash
psql postgresql://postgres:<YOUR_PASSWORD>@svixrgqmbxfnpqpcyimk.supabase.co/postgres < backend/database/schema.sql
```

Replace `<YOUR_PASSWORD>` with your Supabase database password.

### Step 3: Verify Tables Were Created

After applying the schema, run:
```bash
python setup_database.py
```

You should see:
```
[SUCCESS] ✓ patients table exists
[SUCCESS] ✓ doctors table exists
[SUCCESS] ✓ appointments table exists
... and other tables ...
```

### Step 4: Test Patient Registration

1. Go to http://localhost:5173/
2. Click **Register** tab
3. Fill in the form and click **Register Patient**
4. You should see the new Patient ID!

## What Tables Will Be Created

The schema creates the following 13 tables:

| Table | Purpose |
|-------|---------|
| `patients` | Store patient information |
| `doctors` | Store doctor information |
| `departments` | Hospital departments |
| `specializations` | Doctor specializations |
| `appointments` | Appointment bookings |
| `doctor_slots` | Available doctor time slots |
| `patient_visits` | Patient visit history |
| `chat_sessions` | AI receptionist chat sessions |
| `ai_recommendations` | AI analysis & recommendations |
| `feedback` | Patient feedback & ratings |
| `hospital_statistics` | Daily hospital stats |
| `recommended_tests` | Medical tests catalog |
| `symptom_department_mapping` | Symptom to department routing |

## Troubleshooting

**Q: I got an error "table patients does not exist"**
- You haven't applied the schema yet. Follow Steps 1-2 above.

**Q: The schema was applied but I still get errors**
- Wait 10-20 seconds and refresh your browser
- Try registering again

**Q: I want to reset all data**
- In Supabase SQL Editor, run:
  ```sql
  DROP SCHEMA public CASCADE;
  CREATE SCHEMA public;
  ```
- Then re-apply the schema.sql file

## Need Help?

1. Check that your Supabase credentials are correct in `backend/.env`
2. Verify the schema file exists at `backend/database/schema.sql`
3. Make sure you're using the correct Supabase project

---

**Once schema is applied, patient registration will work! ✨**
