# Hospital Management System Setup Guide

## Overview
This is a comprehensive hospital management system with integrated AI Receptionist that provides:
- 🤖 AI-powered patient intake and symptom analysis
- 📋 Patient registration and lookup
- 📅 Appointment booking and management
- 👨‍⚕️ Doctor and department management
- 📊 Admin dashboard with statistics
- ⭐ Feedback and rating system

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **AI**: Google Gemini API
- **Conversation Flow**: LangGraph

### Frontend
- **Framework**: React + TypeScript
- **Build Tool**: Vite
- **Styling**: CSS with Responsive Design

## Prerequisites
- Python 3.8+
- Node.js 16+
- Supabase Account
- Google Gemini API Key
- Git

## Setup Instructions

### 1. Database Setup (Supabase)

1. Create a Supabase project at https://supabase.com
2. Copy your project URL and API keys
3. Go to SQL Editor in Supabase dashboard
4. Run the schema from `backend/database/schema.sql`:
   ```sql
   -- Copy entire contents of schema.sql and execute in Supabase SQL Editor
   ```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp env.template .env

# Edit .env with your credentials:
# - SUPABASE_URL: Your Supabase project URL
# - SUPABASE_KEY: Your Supabase anon key (for frontend)
# - SUPABASE_SERVICE_ROLE_KEY: Your service role key (for backend inserts)
# - GOOGLE_API_KEY: Your Google Gemini API key
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp env.template .env

# Edit .env with your backend URL:
# VITE_API_URL=http://localhost:8000
```

### 4. Running Locally

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:5173`

## API Endpoints

### Patient Management
- `POST /api/patients/register` - Register new patient
- `POST /api/patients/lookup` - Lookup patient by email/phone/ID
- `GET /api/patients/{id}` - Get patient details
- `PUT /api/patients/{id}` - Update patient information
- `GET /api/patients` - List all patients

### Appointments
- `POST /api/appointments` - Create appointment
- `GET /api/appointments/{id}` - Get appointment details
- `PUT /api/appointments/{id}` - Update appointment
- `DELETE /api/appointments/{id}` - Cancel appointment
- `GET /api/appointments/patient/{patient_id}` - Get patient's appointments

### Doctors
- `GET /api/doctors` - List all doctors
- `POST /api/doctors` - Add doctor
- `PUT /api/doctors/{id}` - Update doctor
- `GET /api/doctors/{id}/slots` - Get available time slots

### Admin
- `GET /api/admin/statistics` - Hospital statistics
- `GET /api/admin/dashboard/overview` - Dashboard overview
- `GET /api/admin/emergency-cases` - Emergency cases list
- `POST /api/admin/feedback` - Submit feedback
- `GET /api/admin/feedback/summary` - Feedback summary

### Chat (AI Receptionist)
- `POST /api/chat` - Send message to AI receptionist
- `POST /api/store-patient-data` - Store patient data from chat

## Features

### 1. AI Receptionist
- Multi-turn conversation with patient
- Symptom classification using Gemini AI
- Ward recommendation (General, Emergency, Mental Health)
- Patient data collection and storage

### 2. Patient Management
- New patient registration with auto-generated ID
- Lookup existing patients
- Profile update and management
- Registration date tracking

### 3. Appointment System
- Book appointments with doctors
- Auto-generated appointment numbers
- Status tracking (scheduled, completed, cancelled)
- Priority levels (normal, urgent, emergency)
- Department-specific scheduling

### 4. Doctor Management
- Doctor profiles with specializations
- Availability/on-leave status
- OPD timings
- Slot capacity management

### 5. Admin Dashboard
- Real-time hospital statistics
- Patient registration trends
- Appointment status overview
- Emergency case tracking
- Doctor availability monitoring

### 6. Feedback System
- Patient feedback after appointments
- Star ratings (1-5)
- Doctor ratings and reviews
- Feedback aggregation and analysis

## Database Schema

### Main Tables
- **patients** - Patient information and demographics
- **doctors** - Doctor profiles and specializations
- **departments** - Hospital departments
- **appointments** - Appointment bookings and tracking
- **visits** - Patient visits and treatment records
- **feedback** - Patient feedback and ratings
- **chat_sessions** - AI receptionist chat history
- **hospital_statistics** - Daily statistics tracking

### Key Features
- UUID-based primary keys for security
- Auto-generated patient IDs (PAT12345 format)
- Automatic timestamp management
- Row-level security (RLS) policies
- Comprehensive indexing for performance

## Deployment

### Render.com Deployment

1. **Create Render Account**: https://render.com

2. **Connect GitHub Repository**

3. **Set Environment Variables** in Render dashboard:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `GOOGLE_API_KEY`

4. **Deploy Backend**:
   - Create new "Web Service"
   - Connect to GitHub repo
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `cd backend && uvicorn main:app --host 0.0.0.0`

5. **Deploy Frontend**:
   - Create new "Static Site"
   - Connect to GitHub repo
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/dist`

### CORS Configuration
The application supports CORS from:
- `http://localhost:5173` (local development)
- `http://localhost:3000` (alternative local)
- Your Render deployment URL
- Production domains

## Troubleshooting

### Common Issues

**1. RLS Policy Error**
```
Error: 'new row violates row-level security policy'
```
**Solution**: Ensure `SUPABASE_SERVICE_ROLE_KEY` is set in backend `.env` and the app uses `get_supabase_admin()` for inserts.

**2. Patient Data Not Saving**
- Check service role key is in environment
- Verify database schema is applied to Supabase
- Check backend logs for errors
- Ensure Enum fields are converted to strings before insertion

**3. Frontend Can't Connect to Backend**
- Verify backend is running on port 8000
- Check CORS is enabled
- Update `VITE_API_URL` in frontend `.env`
- Check browser console for CORS errors

**4. Gemini API Errors**
- Verify `GOOGLE_API_KEY` is set in backend `.env`
- Check API key has access to Gemini API
- Ensure requests don't exceed rate limits

## Development Workflow

### Adding a New Endpoint

1. **Create Model** (if needed):
   ```python
   # backend/models/hospital.py
   class NewEntity(BaseModel):
       field1: str
       field2: int
   ```

2. **Create Router**:
   ```python
   # backend/routers/new_router.py
   from fastapi import APIRouter
   from models.hospital import NewEntity
   
   router = APIRouter(prefix="/new", tags=["New"])
   
   @router.get("/")
   async def get_data():
       # Implementation
       pass
   ```

3. **Register Router**:
   ```python
   # backend/main.py
   from routers import new_router
   app.include_router(new_router.router, prefix="/api")
   ```

4. **Create Frontend Component** (if needed):
   ```tsx
   // frontend/src/pages/NewPage.tsx
   const NewPage: React.FC = () => {
       const [data, setData] = useState([])
       
       useEffect(() => {
           fetchData()
       }, [])
       
       return (
           <div>
               {/* Component content */}
           </div>
       )
   }
   ```

5. **Update Navigation** (if new main page):
   ```tsx
   // frontend/src/App.tsx
   {currentPage === 'newpage' && <NewPage />}
   ```

## Performance Optimization

1. **Database Indexes**: Already implemented on frequently queried columns
2. **Pagination**: Implement for large lists
3. **Caching**: Use Redis for frequently accessed data
4. **API Optimization**: Use GraphQL for selective field queries
5. **Frontend Optimization**: Code splitting with React.lazy()

## Security Considerations

1. **Authentication**: Supabase JWT tokens
2. **RLS Policies**: Configured for each table
3. **Service Role Key**: Only used on backend (never exposed to frontend)
4. **HTTPS**: Use in production
5. **API Rate Limiting**: Configure on Render/Vercel
6. **Input Validation**: Pydantic models enforce type safety

## Testing

Run tests locally:
```bash
cd backend
python -m pytest
```

Example test file: `backend/test_workflow.py`

## Support

For issues or questions:
1. Check logs: `backend/main.py` output and browser console
2. Review database in Supabase dashboard
3. Check API endpoints with Postman or curl
4. Verify environment variables are set correctly

## License

This project is provided as-is for educational and commercial use.

## Next Steps

1. ✅ Run locally and test all features
2. ✅ Deploy to Render.com
3. ⏳ Add email notifications for appointments
4. ⏳ Implement real-time updates with WebSockets
5. ⏳ Add payment integration for online consultation
6. ⏳ Implement video consultation feature
7. ⏳ Add mobile app (React Native)

---

**Last Updated**: 2024
**Version**: 2.0.0
