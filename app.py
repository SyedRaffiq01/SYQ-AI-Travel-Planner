import sys
import os

# Add the Travel Planner AI directory to the Python path
travel_planner_path = os.path.join(os.path.dirname(__file__), "Travel Planner agent", "Travel-Planner-AI")
sys.path.insert(0, travel_planner_path)

# Change working directory to the Travel Planner AI directory
os.chdir(travel_planner_path)

# Import the FastAPI app from the Travel Planner AI directory
from app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)