from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Vercel!", "status": "working"}

@app.get("/test")
def test_endpoint():
    return {
        "message": "Test endpoint working",
        "environment_vars": {
            "GEMINI_API_KEY": bool(os.environ.get("GEMINI_API_KEY")),
            "GOOGLE_API_KEY": bool(os.environ.get("GOOGLE_API_KEY"))
        }
    }

# For Vercel
def handler(request):
    return app(request)