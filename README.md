# Hospital AI Receptionist

A minimal AI-powered hospital receptionist system that understands patient queries, routes them to the correct ward, collects required patient details, and sends structured data via webhook.

## Features

- **Natural Language Processing**: Understands patient queries and symptoms
- **Intelligent Routing**: Automatically routes to General, Emergency, or Mental Health wards
- **Data Collection**: Collects patient name, age, and query details
- **Clarification Questions**: Asks one question at a time for missing information
- **Webhook Integration**: Sends completed patient data to external systems
- **Database Storage**: Stores patient data in Supabase

## Architecture

### Backend (Python/FastAPI)
- **LangGraph**: Handles conversation flow and routing logic
- **FastAPI**: REST API endpoints
- **Supabase**: Database for patient data storage

### Frontend (React/Vite)
- **React**: User interface components
- **TypeScript**: Type safety
- **Simple Chat UI**: Clean, hospital-appropriate interface

## Quick Start

1. **Clone and setup environment**:
   ```bash
   git clone <repository-url>
   cd hospital-ai-receptionist
   python setup_env.py  # Creates environment files
   ```

2. **Setup Supabase**:
   - Create a new Supabase project
   - Create a `patients` table with columns: `session_id`, `patient_name`, `patient_age`, `patient_query`, `ward`, `created_at`
   - Copy your project URL and anon key to `backend/.env`

3. **Install and run**:
   ```bash
   # Backend
   cd backend && pip install -r requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

   # Frontend (new terminal)
   cd frontend && npm install && npm run dev
   ```

4. **Open** http://localhost:5173

## Ward Classification Rules

- **Emergency Ward**: Keywords like "emergency", "urgent", "heart attack", "chest pain", "difficulty breathing", "accident", "severe pain"
- **Mental Health Ward**: Keywords like "depression", "anxiety", "suicide", "mental health", "therapy", "stress", "panic attack"
- **General Ward**: All other queries

## API Endpoints

### POST /api/chat
Send patient messages and receive AI responses.

**Request:**
```json
{
  "message": "I have chest pain",
  "session_id": "unique_session_id"
}
```

**Response:**
```json
{
  "response": "I understand you're experiencing chest pain. This sounds like an emergency situation. May I please have your full name?"
}
```

## Webhook Payload

When all patient information is collected, a POST request is sent to the configured webhook URL:

```json
{
  "patient_name": "John Doe",
  "patient_age": 35,
  "patient_query": "I have chest pain and difficulty breathing",
  "ward": "emergency"
}
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- Supabase account

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   # Run the setup script to create environment files
   python setup_env.py
   ```

   Or manually create `backend/.env` with:
   ```
   # Supabase Configuration
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_ANON_KEY=your-supabase-anon-key-here

   # Webhook Configuration
   WEBHOOK_URL=https://your-webhook-endpoint.com/webhook
   ```

4. Set up Supabase database:
   Create a table called `patients` with columns:
   - `session_id` (text, primary key)
   - `patient_name` (text)
   - `patient_age` (integer)
   - `patient_query` (text)
   - `ward` (text)
   - `created_at` (timestamp)

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables (optional):
   The frontend will automatically create `.env.local` from the setup script, or you can manually create it:
   ```
   # Frontend Environment Variables
   VITE_PORT=5173
   VITE_API_URL=http://localhost:8000/api
   ```

## Running the Application

### Start Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Testing the System

1. Open the frontend at http://localhost:5173
2. Try different types of queries:
   - General: "I have a headache"
   - Emergency: "I think I broke my arm"
   - Mental Health: "I'm feeling very anxious"
3. Observe how the AI collects information step by step
4. Check Supabase for stored patient data
5. Monitor webhook calls for completed patient information

## Conversation Flow Example

**User:** "I have chest pain"
**AI:** "I understand you're experiencing chest pain. This sounds like an emergency situation. May I please have your full name?"
**User:** "John Doe"
**AI:** "Could you please tell me your age?"
**User:** "35"
**AI:** "Thank you for providing your information. Your request has been forwarded to the Emergency Department. A healthcare professional will assist you shortly."

## Security Considerations

- Input validation on all endpoints
- Rate limiting should be implemented for production
- HTTPS should be used in production
- Environment variables for sensitive configuration
- CORS configured appropriately

## Production Deployment

1. Set up production Supabase instance
2. Configure production webhook URL
3. Deploy backend to cloud service (Heroku, AWS, etc.)
4. Deploy frontend to static hosting (Vercel, Netlify, etc.)
5. Set up monitoring and logging
6. Configure backup strategies for database