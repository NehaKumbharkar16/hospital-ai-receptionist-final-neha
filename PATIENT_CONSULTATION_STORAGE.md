# Patient Consultation Data Storage

## Overview
The system now stores all patient consultation data from the AI chat:
- **Patient Name** - User's full name
- **Patient Age** - User's age
- **Symptoms** - Patient's medical complaints/symptoms
- **Suggested Ward** - AI recommended ward (GENERAL, EMERGENCY, MENTAL_HEALTH)

---

## How It Works

### 1. During Chat
When users interact with the AI Receptionist:
1. They provide their name, age, and symptoms
2. The AI analyzes the information
3. The AI determines the most appropriate ward to shift the patient

### 2. Auto-Save to Database
After the AI determines the ward, the system automatically saves:
```
Session ID → patient_name, patient_age, symptoms, suggested_ward
```

This data is stored in Supabase `chat_sessions` table with columns:
- `session_id` - Unique chat session identifier
- `patient_name` - Patient's full name
- `patient_age` - Patient's age
- `symptoms` - Patient's medical complaints
- `suggested_ward` - AI recommended ward
- `conversation_data` - Full chat history (JSON)
- `status` - Session status (active, consultation_completed)
- `created_at` - Timestamp when chat started
- `updated_at` - Last update timestamp

---

## Viewing Consultation Data

### In Supabase Dashboard
1. Go to: https://app.supabase.com
2. Select your project
3. **Data Editor** → Click **chat_sessions** table
4. You'll see all consultations with:
   - Patient names
   - Ages
   - Symptoms
   - Suggested wards

### Example Data
| Session ID | Patient Name | Age | Symptoms | Suggested Ward |
|------------|-------------|-----|----------|----------------|
| abc123 | John Doe | 45 | Chest pain, shortness of breath | EMERGENCY |
| def456 | Sarah Smith | 28 | Anxiety, stress | MENTAL_HEALTH |
| ghi789 | Mike Johnson | 35 | Fever, cough | GENERAL |

---

## Database Changes Required

Run this SQL in Supabase to add the new columns:

```sql
ALTER TABLE chat_sessions 
ADD COLUMN IF NOT EXISTS patient_name VARCHAR(255),
ADD COLUMN IF NOT EXISTS patient_age INTEGER,
ADD COLUMN IF NOT EXISTS symptoms TEXT,
ADD COLUMN IF NOT EXISTS suggested_ward VARCHAR(50);

CREATE INDEX IF NOT EXISTS idx_chat_sessions_patient_name ON chat_sessions(patient_name);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_ward ON chat_sessions(suggested_ward);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_created ON chat_sessions(created_at);
```

File: `backend/database/chat_sessions_update.sql`

---

## Implementation Details

### Code Changes
**File**: `backend/routers/chat.py`

New functions added:
1. `save_patient_consultation()` - Async wrapper for database save
2. `_save_consultation_blocking()` - Blocking function that performs the INSERT/UPDATE

Workflow:
1. AI processes user input → determines ward
2. `save_patient_consultation()` is triggered asynchronously
3. Data is saved to `chat_sessions` table
4. No blocking of chat response (async operation)

### Auto-Logging
When a consultation is saved, you'll see in Render logs:
```
[DATABASE] Saved consultation for John Doe (Age: 45) - Suggested Ward: EMERGENCY
```

---

## Next Steps

1. **Run the SQL migration** in Supabase:
   - SQL Editor → New Query
   - Paste content from `chat_sessions_update.sql`
   - Click RUN

2. **Deploy the code**:
   - Already committed to GitHub
   - Render will auto-deploy on next push OR
   - Manual Deploy: https://dashboard.render.com

3. **Test the feature**:
   - Go to https://hospital-ai-receptionist-final.onrender.com
   - Click "AI Receptionist" tab
   - Start chat and provide your name, age, symptoms
   - AI will suggest a ward
   - Your data will be saved to database automatically

4. **Verify in Supabase**:
   - Check `chat_sessions` table
   - You should see your consultation data with patient_name, age, symptoms, and suggested_ward

---

## Benefits

✅ **Persistent Storage** - No data loss on server restart
✅ **Automatic Capture** - Happens in background (no user action needed)
✅ **Non-Blocking** - Doesn't slow down chat response
✅ **Queryable** - Can search/filter by patient name, age, ward, etc.
✅ **Complete History** - Both consultation data AND chat conversation saved
✅ **Audit Trail** - Timestamps show when consultation occurred
