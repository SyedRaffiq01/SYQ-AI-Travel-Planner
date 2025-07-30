from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import google.generativeai as genai
import os
import requests
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Travel Planner AI")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None
    print("Warning: GEMINI_API_KEY not found in environment variables")

class TravelRequest(BaseModel):
    source: str
    destination: str
    start_date: str
    end_date: str
    budget: float
    travelers: int
    interests: List[str]
    include_flights: bool = False

class ChatRequest(BaseModel):
    question: str
    travel_plan: str

def get_flight_data(source, destination, start_date):
    """Fetch flight data from SerpAPI"""
    try:
        serp_api_key = os.environ.get("SERP_API_KEY")
        if not serp_api_key:
            return None
            
        source_code = source.strip().upper()
        dest_code = destination.strip().upper()

        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_flights",
            "departure_id": source_code,
            "arrival_id": dest_code,
            "outbound_date": start_date,
            "currency": "INR",
            "hl": "en",
            "type": "2",
            "api_key": serp_api_key
        }

        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching flight data: {str(e)}")
        return None

@app.get("/")
async def root():
    """Serve the main page or API info"""
    try:
        return FileResponse('static/index.html')
    except FileNotFoundError:
        return {
            "message": "Travel Planning AI API is running",
            "status": "healthy",
            "gemini_configured": bool(model),
            "endpoints": ["/health", "/generate-plan", "/chat", "/plan-trip"]
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "gemini_api_configured": bool(model),
        "environment_vars": {
            "GEMINI_API_KEY": bool(os.environ.get("GEMINI_API_KEY")),
            "GOOGLE_API_KEY": bool(os.environ.get("GOOGLE_API_KEY")),
            "SERP_API_KEY": bool(os.environ.get("SERP_API_KEY"))
        }
    }

@app.post("/generate-plan")
async def generate_travel_plan(request: TravelRequest):
    """Generate a comprehensive travel plan"""
    try:
        if not model:
            raise HTTPException(
                status_code=500, 
                detail="Gemini AI is not configured. Please set GEMINI_API_KEY environment variable."
            )
        
        # Construct the prompt
        prompt = f"""
Create a detailed travel plan with the following details:
From: {request.source}
To: {request.destination}
Dates: {request.start_date} to {request.end_date}
Budget: ₹{request.budget} (Indian Rupees)
Number of Travelers: {request.travelers}
Interests: {', '.join(request.interests)}

Please provide:
1. Day-by-day itinerary
2. Estimated costs breakdown (in Indian Rupees - INR)
3. Recommended accommodations
4. Must-visit places based on the interests
5. Local transportation options
6. Food recommendations
7. Tips and precautions
8. Weather considerations for the dates

Note: All cost estimates should be provided in Indian Rupees (INR) with ₹ symbol.
Format the response in markdown for better readability.
"""

        # Generate response using Gemini
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            raise HTTPException(status_code=500, detail="Failed to generate travel plan")

        # Handle flight data if requested
        flight_data = None
        if request.include_flights:
            try:
                flight_data = get_flight_data(request.source, request.destination, request.start_date)
            except Exception as e:
                print(f"Flight data error: {str(e)}")

        # Format the travel plan
        travel_plan = f"""# Your Travel Plan

{response.text}
"""

        return {
            "success": True,
            "plan": travel_plan,
            "flight_details": flight_data if flight_data else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in generate_travel_plan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/chat")
async def chat_with_plan(request: ChatRequest):
    """Chat about the travel plan"""
    try:
        if not model:
            raise HTTPException(
                status_code=500, 
                detail="Gemini AI is not configured. Please set GEMINI_API_KEY environment variable."
            )
            
        prompt = f"""
Given this travel plan:
{request.travel_plan}

Please answer this question about the plan:
{request.question}

Provide a clear and concise response, using markdown formatting where appropriate.
If the question is about something not covered in the plan, suggest relevant information or alternatives.
"""

        response = model.generate_content(prompt)
        
        if not response or not response.text:
            raise HTTPException(status_code=500, detail="Failed to generate response")
            
        return {
            "success": True,
            "response": response.text
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat_with_plan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/plan-trip")
async def plan_trip(request: TravelRequest):
    """Legacy endpoint for backward compatibility"""
    return await generate_travel_plan(request)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    print(f"Could not mount static files: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)