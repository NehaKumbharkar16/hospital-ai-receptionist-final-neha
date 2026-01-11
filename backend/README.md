# Hospital AI Backend - Render Deployment

This FastAPI backend provides AI-powered hospital receptionist functionality.

## 🚀 Deploy to Render

### Method 1: Using render.yaml (Recommended)

1. **Connect your GitHub repository** to Render
2. **Create a new Web Service** from your repository
3. **Render will automatically detect** the `render.yaml` file
4. **Set Environment Variables** in Render dashboard:
   - `SUPABASE_URL` = `https://svixrgqmbxfnpqpcyimk.supabase.co`
   - `SUPABASE_ANON_KEY` = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (your key)
   - `GOOGLE_API_KEY` = `your-google-gemini-api-key` (optional)
   - `WEBHOOK_URL` = `your-webhook-url` (optional)

### Method 2: Manual Setup

1. **Create a new Web Service** on Render
2. **Connect your repository**
3. **Configure the service**:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables** (same as above)

## 📋 Environment Variables Required

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Your Supabase project URL | ✅ |
| `SUPABASE_ANON_KEY` | Supabase anonymous key | ✅ |
| `GOOGLE_API_KEY` | Google Gemini API key | ❌ (falls back to keyword classification) |
| `WEBHOOK_URL` | Webhook endpoint for notifications | ❌ |

## 🔗 API Endpoints

- `GET /` - Health check
- `POST /api/chat` - Chat with AI receptionist

## 🧪 Testing the Deployment

Once deployed, test with:

```bash
curl -X POST https://your-render-url.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test123"}'
```

## 📊 Monitoring

- Check Render logs for any errors
- Monitor Supabase for data storage
- Use Render's built-in metrics

## 🆘 Troubleshooting

**Common Issues:**

1. **Environment Variables**: Make sure all required env vars are set in Render dashboard
2. **CORS Issues**: Update the `allow_origins` in `main.py` if needed
3. **Database Connection**: Verify Supabase credentials are correct
4. **Port Issues**: Render uses `$PORT` environment variable automatically

**Debug Commands:**
```bash
# Check if app starts locally
uvicorn main:app --host 0.0.0.0 --port 8000

# Test API endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi", "session_id": "test"}'
```