from http.server import BaseHTTPRequestHandler
import json
import os
import google.generativeai as genai

# Initialize Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Error configuring Gemini: {e}")
        model = None
else:
    model = None

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            if not model:
                self.send_error_response(500, "Gemini AI is not configured. Please set GEMINI_API_KEY environment variable.")
                return

            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
            else:
                self.send_error_response(400, "No data provided")
                return

            # Extract request data
            source = data.get('source', '')
            destination = data.get('destination', '')
            start_date = data.get('start_date', '')
            end_date = data.get('end_date', '')
            budget = data.get('budget', 0)
            travelers = data.get('travelers', 1)
            interests = data.get('interests', [])

            if not all([source, destination, start_date, end_date]):
                self.send_error_response(400, "Missing required fields: source, destination, start_date, end_date")
                return

            # Create prompt
            prompt = f"""
Create a detailed travel plan with the following details:
From: {source}
To: {destination}
Dates: {start_date} to {end_date}
Budget: ₹{budget} (Indian Rupees)
Number of Travelers: {travelers}
Interests: {', '.join(interests)}

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

            # Generate response
            response = model.generate_content(prompt)
            
            if not response or not response.text:
                self.send_error_response(500, "Failed to generate travel plan")
                return

            travel_plan = f"""# Your Travel Plan

{response.text}
"""

            self.send_json_response({
                "success": True,
                "plan": travel_plan,
                "flight_details": None
            })

        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON")
        except Exception as e:
            self.send_error_response(500, f"Error generating travel plan: {str(e)}")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_response = {
            "success": False,
            "detail": message
        }
        self.wfile.write(json.dumps(error_response).encode())