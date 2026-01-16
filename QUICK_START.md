# Quick Start Guide

## 1-Minute Setup

### Prerequisites
- Backend running: `cd backend && python -m uvicorn main:app --reload --port 8000`
- Frontend running: `cd frontend && npm run dev`
- Database: Supabase connected with schema applied

## Running the System (LOCAL)

### Terminal 1 - Start Backend
```bash
cd backend
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

uvicorn main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Terminal 2 - Start Frontend
```bash
cd frontend
npm run dev
```

Expected output:
```
  VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
```

### Terminal 3 (Optional) - Test Database
```bash
# Test patient registration
curl -X POST http://localhost:8000/api/patients/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "age": 30,
    "gender": "male",
    "blood_group": "O+",
    "address": "123 Main St"
  }'
```

## Accessing the System

Open browser: `http://localhost:5173`

### Main Features:
- **🏥 Home** - Landing page with feature overview
- **🤖 AI Receptionist** - Chat with AI for symptom analysis
- **📋 Patient Registration** - Register new patients
- **📅 Appointments** - Book and manage appointments
- **📊 Dashboard** - Admin statistics and analytics

## Testing Workflows

### 1. Patient Registration Flow
1. Navigate to "Register" page
2. Fill in patient details
3. Click "Register Patient"
4. Copy the Patient ID returned
5. Use this ID for appointments

### 2. AI Receptionist Flow
1. Go to "AI Receptionist" page
2. Describe your symptoms (e.g., "I have a headache and fever")
3. AI analyzes and recommends ward
4. Your data is automatically saved

### 3. Appointment Booking Flow
1. Go to "Appointments" page
2. Search patient by email
3. Select available doctor
4. Choose date/time
5. Select priority level
6. Book appointment

### 4. Admin Dashboard Flow
1. Go to "Dashboard" page
2. View real-time statistics:
   - Total patients today
   - Pending appointments
   - Emergency cases
   - Available doctors
3. See recent emergency cases
4. View newly registered patients

## Common Commands

```bash
# Clear backend cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version

# Check Node version
node --version

# Kill process on port 8000 (if stuck)
# Windows: netstat -ano | findstr :8000
# macOS/Linux: lsof -i :8000

# View backend logs
# Check the terminal running uvicorn

# View frontend build errors
# Check the terminal running npm run dev
```

## API Health Check

```bash
# Backend health
curl http://localhost:8000/docs

# Frontend health
curl http://localhost:5173

# Database connection
curl http://localhost:8000/api/patients
```

## Environment Configuration

### Backend (.env)
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
GOOGLE_API_KEY=your-gemini-api-key
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## Troubleshooting

### "Port 8000 already in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### "Module not found" (Backend)
```bash
cd backend
pip install -r requirements.txt
```

### "Module not found" (Frontend)
```bash
cd frontend
npm install
```

### "Cannot connect to Supabase"
- Check SUPABASE_URL and SUPABASE_KEY in .env
- Verify Supabase project is active
- Check internet connection

### "AI Receptionist not responding"
- Verify GOOGLE_API_KEY is set
- Check API key has Gemini access
- Check backend logs for errors

## Performance Tips

1. **Clear cache regularly**: `rm -rf backend/__pycache__ frontend/node_modules/.vite`
2. **Use Chrome DevTools** to monitor network and performance
3. **Backend Performance**: Uvicorn auto-reloading may be slow, disable with `--no-reload` for production
4. **Frontend Performance**: Check Vite build time in console

## Database Management

### View Patient Records
1. Go to Supabase dashboard
2. Click "patients" table
3. Browse registered patients

### View Appointments
1. Supabase > "appointments" table
2. Filter by appointment_date

### View Statistics
1. Supabase > "hospital_statistics" table
2. Check daily stats

## Deployment Checklist

Before deploying to Render:
- [ ] All env variables configured
- [ ] Database schema applied to production Supabase
- [ ] API endpoints tested locally
- [ ] Frontend builds without errors
- [ ] CORS URLs updated for production domain
- [ ] Service role key secure (only in backend)
- [ ] Git repo up to date

## Next Steps

1. **Run locally** and test all features (20 minutes)
2. **Familiarize** with the admin dashboard
3. **Set up production** database in Supabase
4. **Deploy** to Render (see HOSPITAL_SYSTEM_SETUP.md)
5. **Monitor** logs and performance
6. **Customize** as needed for your hospital

## Support

**Issue: Something isn't working?**

1. Check backend terminal for error messages
2. Open browser DevTools (F12) and check console
3. Check Supabase dashboard for data
4. Verify all environment variables are set
5. Review logs in backend/main.py

**Quick Debug:**
```bash
# Test backend
curl http://localhost:8000/api/patients

# Test specific endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"user_input": "I have a headache"}'
```

---

**Ready to start?** Open two terminals and run the backend and frontend commands above!
