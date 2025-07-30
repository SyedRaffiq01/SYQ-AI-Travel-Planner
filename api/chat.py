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

            question = data.get('question', '')
            travel_plan = data.get('travel_plan', '')

            if not question:
                self.send_error_response(400, "Missing required field: question")
                return

            prompt = f"""
Given this travel plan:
{travel_plan}

Please answer this question about the plan:
{question}

Provide a clear and concise response, using markdown formatting where appropriate.
If the question is about something not covered in the plan, suggest relevant information or alternatives.
"""

            response = model.generate_content(prompt)
            
            if not response or not response.text:
                self.send_error_response(500, "Failed to generate response")
                return

            self.send_json_response({
                "success": True,
                "response": response.text
            })

        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON")
        except Exception as e:
            self.send_error_response(500, f"Error in chat: {str(e)}")

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