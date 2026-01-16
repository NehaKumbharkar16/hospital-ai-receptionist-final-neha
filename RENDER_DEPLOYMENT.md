# Hospital Management System - Render.com Deployment Guide

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│         GitHub Repository               │
│     (Backend + Frontend + Database)     │
└────────────────────┬────────────────────┘
                     │
         ┌───────────┴──────────┐
         │                      │
         ▼                      ▼
    Render Backend          Render Frontend
    (FastAPI on              (Static Site)
     Web Service)               Vite
         │                      │
         └───────────┬──────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │   Supabase Database  │
          │   (PostgreSQL + RLS) │
          └──────────────────────┘
```

## Step-by-Step Deployment

### Phase 1: Prepare GitHub Repository

1. **Ensure your repo has proper structure:**
```
Hospital AI Agent Cursor/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── database/
│   │   └── __init__.py
│   │   └── schema.sql
│   ├── models/
│   ├── routers/
│   └── .env.template
├── frontend/
│   ├── package.json
│   ├── src/
│   ├── vite.config.ts
│   └── .env.template
├── HOSPITAL_SYSTEM_SETUP.md
└── QUICK_START.md
```

2. **Create .gitignore:**
```bash
# Backend
backend/venv/
backend/__pycache__/
backend/.env
backend/*.pyc

# Frontend
frontend/node_modules/
frontend/dist/
frontend/.env
frontend/.env.local

# General
.DS_Store
*.pyc
__pycache__
.vscode/
```

3. **Commit everything to GitHub:**
```bash
git add .
git commit -m "Hospital Management System - Ready for Deployment"
git push origin main
```

### Phase 2: Set Up Supabase Production Database

1. **Create new Supabase project** (Production):
   - Go to https://supabase.com
   - Create new project with strong password
   - Copy Project URL and API keys

2. **Apply database schema:**
   - Open Supabase SQL Editor
   - Create new query
   - Paste entire content of `backend/database/schema.sql`
   - Run the SQL

3. **Verify tables created:**
   ```sql
   SELECT table_name FROM information_schema.tables 
   WHERE table_schema = 'public';
   ```

4. **Get credentials:**
   - Go to Settings > API
   - Copy: `Project URL`, `anon key`, `service_role key`

### Phase 3: Deploy Backend to Render

1. **Create Render Account:**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create Web Service:**
   - Click "New +" > "Web Service"
   - Connect your GitHub repository
   - Select repository and main branch

3. **Configure Build Settings:**
   - **Name**: `hospital-backend` (or your choice)
   - **Runtime**: `Python 3.11`
   - **Build Command**: 
     ```
     pip install -r backend/requirements.txt
     ```
   - **Start Command**: 
     ```
     cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
     ```

4. **Set Environment Variables:**
   Click "Environment" tab and add:
   ```
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=your_anon_key_here
   SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Note the URL: `https://hospital-backend.onrender.com`

### Phase 4: Deploy Frontend to Render

1. **Create Static Site:**
   - Click "New +" > "Static Site"
   - Connect your GitHub repository

2. **Configure Build Settings:**
   - **Name**: `hospital-frontend` (or your choice)
   - **Build Command**: 
     ```
     cd frontend && npm install && npm run build
     ```
   - **Publish Directory**: `frontend/dist`

3. **Set Environment Variable:**
   Click "Environment" tab and add:
   ```
   VITE_API_URL=https://hospital-backend.onrender.com
   ```

4. **Deploy:**
   - Click "Create Static Site"
   - Wait for deployment (1-2 minutes)
   - Access at: `https://hospital-frontend.onrender.com`

### Phase 5: Update CORS Configuration

After deployment, update your backend CORS settings:

1. **Edit `backend/main.py`:**
```python
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://hospital-frontend.onrender.com",  # Add your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. **Commit and push:**
```bash
git add backend/main.py
git commit -m "Update CORS for production deployment"
git push origin main
```

Render will auto-deploy the changes.

### Phase 6: Verify Deployment

1. **Test Backend Health:**
   ```bash
   curl https://hospital-backend.onrender.com/docs
   ```
   Should open API documentation

2. **Test Patient Registration:**
   ```bash
   curl -X POST https://hospital-backend.onrender.com/api/patients/register \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Test",
       "last_name": "User",
       "email": "test@example.com",
       "phone": "1234567890",
       "age": 30,
       "gender": "male",
       "blood_group": "O+",
       "address": "Test Address"
     }'
   ```

3. **Test Frontend:**
   - Open `https://hospital-frontend.onrender.com` in browser
   - Test AI Receptionist chat
   - Register a patient
   - Try booking appointment

## Performance Monitoring

### Monitor Backend Performance

1. **Check Render Logs:**
   - Dashboard > hospital-backend > Logs
   - Look for errors and warnings

2. **Monitor Database:**
   - Supabase Dashboard
   - Check "Database" > "Stats"
   - Monitor query performance

3. **Test Load:**
```bash
# Install Apache Bench if needed
# Then test concurrent requests
ab -n 100 -c 10 https://hospital-backend.onrender.com/api/patients
```

## Troubleshooting Deployment

### Issue: Backend Deploy Fails

**Check logs:**
- Go to Render Dashboard > hospital-backend > Logs
- Look for Python errors

**Common solutions:**
```
# Missing dependency
- Add to backend/requirements.txt

# Python version incompatibility
- Change runtime to Python 3.11

# Module import error
- Check all imports in main.py
- Verify all routers are included
```

### Issue: Frontend Can't Connect to Backend

**Check:**
1. Backend URL in frontend `.env`: `VITE_API_URL=https://hospital-backend.onrender.com`
2. CORS enabled in backend for frontend URL
3. Backend service is running (check Render logs)

**Test:**
```bash
# From frontend terminal
curl https://hospital-backend.onrender.com/api/patients
```

### Issue: Database Connection Error

**Verify Supabase credentials:**
```bash
# In backend .env on Render:
SUPABASE_URL=https://xxxxx.supabase.co  # No trailing slash
SUPABASE_KEY=eyJhbGc... (should be ~200 chars)
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc... (longer, ~300 chars)
```

### Issue: AI Receptionist Not Working

**Check GOOGLE_API_KEY:**
1. Verify key is in Render environment
2. Enable Generative AI API in Google Cloud
3. Check API quotas and usage

## Scaling Considerations

### Database
- Supabase scales automatically
- Monitor connections in "Stats"
- Enable connection pooling if needed

### Backend
- Render scales automatically
- Set up alerts for high memory usage
- Consider upgrading instance type if needed

### Frontend
- Static sites scale infinitely
- No scaling needed
- CDN included with Render

## Cost Optimization

**Render.com Pricing:**
- Free tier: $0/month (limited)
- Hobby tier: $5/month each service
- Pro tier: $12+/month with better SLA

**Supabase Pricing:**
- Free tier: $0/month (good for development)
- Pro tier: $25/month (for production)

**Google API:**
- Free tier: 60 requests/minute
- Pay-as-you-go: Charged per 1000 requests

## Disaster Recovery

### Backup Database
```bash
# Supabase automatic backups included in Pro plan
# Manual backup via dashboard: Settings > Backups
```

### Monitor Uptime
- Render provides uptime dashboard
- Set up status page for users
- Consider using uptime monitoring service

### Disaster Recovery Plan
1. **GitHub**: All code backed up
2. **Supabase**: Automatic backups (Pro plan)
3. **Render**: Can redeploy from GitHub anytime

## Security Checklist

- [ ] Service role key only in backend environment
- [ ] Anon key used for frontend operations
- [ ] CORS restricted to known domains
- [ ] Environment variables use Render secrets
- [ ] GitHub repo is private
- [ ] Database RLS policies enabled
- [ ] HTTPS enabled (automatic with Render)
- [ ] API rate limiting configured
- [ ] Error messages don't expose sensitive info
- [ ] Regular security audits scheduled

## Monitoring Checklist

- [ ] Backend logs checked daily
- [ ] Database performance monitored
- [ ] Error rates tracked
- [ ] User feedback collected
- [ ] API response times monitored
- [ ] Database size growth tracked
- [ ] Cost monitoring enabled

## Post-Deployment Tasks

### Day 1 (After Deployment)
- [ ] Test all core features
- [ ] Monitor logs for errors
- [ ] Collect user feedback
- [ ] Document any issues

### Week 1
- [ ] Review usage statistics
- [ ] Optimize slow endpoints
- [ ] Update documentation
- [ ] Plan next features

### Month 1
- [ ] Full security audit
- [ ] Performance analysis
- [ ] Cost review
- [ ] Backup verification

## Continuous Deployment

Once deployed, any push to `main` branch will auto-deploy:

```bash
# Development workflow
git checkout -b feature/new-feature
# ... make changes ...
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# Create pull request and review

# Merge to main
git checkout main
git pull origin feature/new-feature
git push origin main

# Render automatically deploys!
```

## Rollback Process

If deployment breaks production:

```bash
# Option 1: Revert last commit
git revert <commit-hash>
git push origin main
# Render redeploys automatically

# Option 2: Manual rollback in Render
# Dashboard > Service > Deployments
# Click previous successful deployment
# Click "Revert to this deployment"
```

## Support

**Having issues?**

1. Check [Render Documentation](https://render.com/docs)
2. Check [Supabase Documentation](https://supabase.com/docs)
3. Review backend logs in Render
4. Check browser DevTools console
5. Test locally first to isolate issue

---

**Your Hospital Management System is now in the cloud! 🚀**

Access your system at:
- **Frontend**: `https://hospital-frontend.onrender.com`
- **Backend API**: `https://hospital-backend.onrender.com`
- **API Docs**: `https://hospital-backend.onrender.com/docs`

Happy deploying! 🏥
