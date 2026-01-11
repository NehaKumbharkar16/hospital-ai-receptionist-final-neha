# 🚀 Hospital AI Agent - Complete Deployment Guide

This guide will help you deploy both the backend (FastAPI) and frontend (React) to production.

## 📋 Prerequisites

- ✅ GitHub account
- ✅ Render account (free tier available)
- ✅ Vercel/Netlify account for frontend (optional)
- ✅ Supabase project set up
- ✅ Google Gemini API key (optional)

## 🏗️ Backend Deployment (Render)

### Step 1: Prepare Backend for Deployment

Your backend is already configured with `render.yaml` for easy deployment.

### Step 2: Deploy to Render

1. **Go to [Render Dashboard](https://dashboard.render.com)**

2. **Click "New" → "Web Service"**

3. **Connect your GitHub repository**
   - Select your `Hospital AI Agent Cursor` repository
   - Render will detect the `render.yaml` file

4. **Configure the service**:
   - **Name**: `hospital-ai-backend`
   - **Runtime**: Python 3 (auto-detected)
   - **Build Command**: `pip install -r requirements.txt` (auto-detected)
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT` (auto-detected)

5. **Add Environment Variables**:
   ```
   SUPABASE_URL=https://svixrgqmbxfnpqpcyimk.supabase.co
   SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN2aXhyZ3FtYnhmbnBxcGN5aW1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgwNDk2MDcsImV4cCI6MjA4MzYyNTYwN30.GOTzgfC8ew5QoMeayF-Wpl3VZwbDsl46y7blFlvyVBU
   GOOGLE_API_KEY=your-google-gemini-api-key-here  # Optional
   WEBHOOK_URL=your-webhook-url-here  # Optional
   ```

6. **Click "Create Web Service"**

7. **Wait for deployment** (usually 2-5 minutes)

8. **Copy the deployment URL** (something like: `https://hospital-ai-backend.onrender.com`)

### Step 3: Test Backend Deployment

```bash
# Test the deployed API
curl -X POST https://your-backend-url.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test123"}'
```

Expected response:
```json
{"response": "Hello! I'm the hospital AI receptionist. May I please have your full name?"}
```

## 🎨 Frontend Deployment (Vercel/Netlify)

### Option 1: Deploy to Vercel (Recommended)

1. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**

2. **Click "New Project"**

3. **Import your GitHub repository**

4. **Configure the project**:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

5. **Add Environment Variables**:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com/api
   ```

6. **Click "Deploy"**

7. **Copy the deployment URL** (something like: `https://hospital-ai-agent.vercel.app`)

### Option 2: Deploy to Netlify

1. **Go to [Netlify Dashboard](https://app.netlify.com)**

2. **Click "Add new site" → "Import an existing project"**

3. **Connect your GitHub repository**

4. **Configure build settings**:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`

5. **Add environment variables**:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com/api
   ```

6. **Click "Deploy site"**

## 🔄 Update CORS for Production

Once both are deployed, update the backend CORS settings:

```python
# In backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "https://hospital-ai-agent.vercel.app",  # Your Vercel URL
        "https://your-netlify-site.netlify.app",  # Your Netlify URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🧪 Testing Complete Deployment

1. **Open your deployed frontend URL**

2. **Test the conversation flow**:
   - Enter name: "John Doe"
   - Enter age: "30"
   - Enter symptoms: "I have chest pain"
   - Should route to Emergency Department

3. **Check Supabase dashboard** for stored data

4. **Verify webhook notifications** (if configured)

## 📊 Monitoring & Maintenance

### Backend (Render)
- **Logs**: Check Render dashboard for application logs
- **Metrics**: Monitor response times and error rates
- **Scaling**: Render automatically scales based on traffic

### Frontend (Vercel/Netlify)
- **Analytics**: Monitor user interactions
- **Performance**: Check Core Web Vitals
- **Updates**: Automatic deployments on git push

### Database (Supabase)
- **Dashboard**: Monitor table usage and performance
- **Backups**: Automatic daily backups
- **Security**: Row Level Security (RLS) enabled

## 🆘 Troubleshooting

### Backend Issues
```
# Check Render logs
# Test API directly
curl https://your-backend.onrender.com/

# Test chat endpoint
curl -X POST https://your-backend.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "session_id": "test"}'
```

### Frontend Issues
```
# Check browser console for errors
# Verify VITE_API_URL is set correctly
# Check CORS errors in network tab
```

### Database Issues
```
# Check Supabase connection logs
# Verify table permissions
# Check Row Level Security settings
```

## 💰 Cost Optimization

### Render (Backend)
- **Free Tier**: 750 hours/month
- **Paid Plans**: From $7/month for more resources

### Vercel (Frontend)
- **Free Tier**: Generous limits for small projects
- **Paid Plans**: From $20/month for teams

### Supabase (Database)
- **Free Tier**: 500MB database, 50MB file storage
- **Paid Plans**: From $25/month for more resources

## 🎉 Deployment Complete!

Your Hospital AI Agent is now live and accessible worldwide! 🌟

**Production URLs:**
- Frontend: `https://your-frontend-domain.com`
- Backend: `https://your-backend.onrender.com`
- API: `https://your-backend.onrender.com/api/chat`

The system will handle patient intake, AI classification, and data storage automatically! 🏥🤖