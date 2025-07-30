# Deploy to Render

## Quick Deploy Steps:

1. **Push your code to GitHub** (if not already done)

2. **Go to Render Dashboard**: https://render.com/

3. **Create New Web Service**:
   - Connect your GitHub repository
   - Choose this repository: `CODEAI`
   - Name: `syq-travel-planner`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `PYTHON_VERSION`: `3.11.0` (optional)

5. **Deploy**: Click "Create Web Service"

## Alternative: Using render.yaml

If you have a `render.yaml` file in your repo, Render will automatically use it for configuration.

## Test Endpoints After Deployment:

- Root: `https://your-app.onrender.com/`
- Health: `https://your-app.onrender.com/health`
- API: `https://your-app.onrender.com/generate-plan` (POST)

## Environment Variables Needed:

- `GEMINI_API_KEY` or `GOOGLE_API_KEY`: Your Google Gemini API key

## File Structure for Render:

```
/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── index.html          # Frontend HTML
├── static/             # Static files (CSS, JS)
├── render.yaml         # Render configuration (optional)
└── Dockerfile          # Docker configuration (optional)
```