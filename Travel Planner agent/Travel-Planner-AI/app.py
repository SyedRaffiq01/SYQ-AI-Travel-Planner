from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY or GOOGLE_API_KEY in your environment variables")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

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
        # Convert airport codes to uppercase
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
            "type": "2",  # One-way flight
            "api_key": os.getenv("SERP_API_KEY")
        }

        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Error fetching flight data: {str(e)}")
        return None

def format_flight_details_markdown(flight_data, source_code, dest_code, start_date):
    """Format flight data into markdown table"""
    if not flight_data or "best_flights" not in flight_data:
        return "No flights available for this route."

    markdown = "## Available Flight Options\n\n"
    markdown += "| Airline | Flight(s) | Departure | Arrival | Duration | Price | Features |\n"
    markdown += "|---------|-----------|-----------|----------|----------|--------|----------|\n"

    for option in flight_data["best_flights"][:3]:  # Limit to 3 flights
        # Get first and last flight for departure and arrival times
        first_flight = option["flights"][0]
        last_flight = option["flights"][-1]

        # Format flight numbers
        flight_numbers = " + ".join([f"{flight['airline']} {flight['flight_number']}" for flight in option["flights"]])

        # Get departure and arrival details
        departure = f"{first_flight['departure_airport']['name']} ({first_flight['departure_airport']['time']})"
        arrival = f"{last_flight['arrival_airport']['name']} ({last_flight['arrival_airport']['time']})"

        # Calculate total duration in hours and minutes
        total_duration = f"{option['total_duration'] // 60}h {option['total_duration'] % 60}m"

        # Get unique features
        features = set()
        for flight in option["flights"]:
            features.update([ext for ext in flight.get("extensions", []) if "Carbon emissions" not in ext])
        features_str = "<br>".join(list(features)[:3])  # Show top 3 features
        
        booking_link = f"[Book Now](https://www.google.com/flights?hl=en#flt={source_code}.{dest_code}.{start_date})"
        markdown += f"| {first_flight['airline']} | {flight_numbers} | {departure} | {arrival} | {total_duration} | ₹{option['price']} | {features_str} |\n"
        markdown += f"*{booking_link}*\n\n"

        if "layovers" in option:
            markdown += f"*Layover at: {option['layovers'][0]['name']} ({option['layovers'][0]['duration'] // 60}h {option['layovers'][0]['duration'] % 60}m)*\n\n"

    return markdown

@app.post("/generate-plan")
async def generate_travel_plan(request: TravelRequest):
    """Generate a comprehensive travel plan"""
    try:
        # Construct the base prompt
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
        """

        # Get flight details if requested
        flight_data = None
        if request.include_flights:
            flight_data = get_flight_data(
                request.source, request.destination,
                request.start_date)
            if flight_data:
                flight_context = f"""
                First, analyze these flight options (showing top 3 best flights) for the journey:
                {flight_data}

                Please analyze these flights and create a markdown table showing the best options, including:
                - Airline and flight numbers
                - Departure and arrival times
                - Total duration
                - Price
                - Key features (like legroom, Wi-Fi, etc.)
                - Layover information if any

                After the flight analysis, please provide a comprehensive travel plan that includes:
                - A day-by-day itinerary
                - All the other requested information (costs, accommodations, places to visit, etc.)
                
                Make sure to separate the flight analysis and travel plan with clear headings.
                """
                prompt += flight_context

        # Generate response using Gemini
        response = model.generate_content(prompt)

        if flight_data:
            flight_data = format_flight_details_markdown(
                flight_data,
                request.source.strip().upper(),
                request.destination.strip().upper(),
                request.start_date)

        # Format the travel plan in markdown
        travel_plan = f"""
# Your Travel Plan

{response.text}
"""

        return {
            "success": True,
            "plan": travel_plan,
            "flight_details": flight_data if request.include_flights else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_plan(request: ChatRequest):
    """Chat about the travel plan"""
    try:
        prompt = f"""
        Given this travel plan:
        {request.travel_plan}

        Please answer this question about the plan:
        {request.question}

        Provide a clear and concise response, using markdown formatting where appropriate.
        If the question is about something not covered in the plan, suggest relevant information or alternatives.
        """

        response = model.generate_content(prompt)
        return {
            "success": True,
            "response": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/plan-trip")
async def plan_trip(request: TravelRequest):
    """Legacy endpoint for backward compatibility"""
    try:
        # Construct the prompt for Gemini
        prompt = f"""As a travel planning expert, create a detailed itinerary and travel plan with the following details:
        
        From: {request.source}
        To: {request.destination}
        Dates: {request.start_date} to {request.end_date}
        Budget: ₹{request.budget} (Indian Rupees)
        Number of Travelers: {request.travelers}
        Interests: {', '.join(request.interests)}

        Please provide:
        1. Suggested daily itinerary
        2. Estimated costs breakdown (in Indian Rupees - INR)
        3. Recommended accommodations within budget
        4. Must-visit attractions based on interests
        5. Local transportation options
        6. Food and restaurant recommendations
        7. Travel tips and cultural considerations
        8. Weather considerations for the dates
        
        Note: All cost estimates should be provided in Indian Rupees (INR) with ₹ symbol.
        """

        # Generate response using Gemini
        response = model.generate_content(prompt)
        
        return {
            "success": True,
            "plan": response.text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Serve the main page"""
    try:
        return FileResponse('static/index.html')
    except FileNotFoundError:
        return {"message": "Travel Planning AI API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)