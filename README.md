# 🌍 SYQ Travel Planner AI

A comprehensive travel planning application powered by Google's Gemini AI with INR currency support and flight integration.

## ✨ Features

- **AI-Powered Planning**: Uses Google Gemini AI for intelligent travel recommendations
- **Flight Integration**: Real-time flight data with pricing in INR
- **Interactive Chat**: Ask questions about your travel plan
- **Budget-Friendly**: All costs displayed in Indian Rupees (₹)
- **Customizable**: Based on your interests and preferences

## 🚀 Quick Deploy

### Deploy to Railway (Recommended)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

1. Click the Railway button above
2. Connect your GitHub account
3. Set environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `SERP_API_KEY`: Your SerpAPI key (optional, for flight data)

### Deploy to Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Deploy to Vercel
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/SyedRaffiq01/SYQ-AI-Travel-Planner)

## 🛠️ Local Development

### Using GitHub Codespaces (Easiest)
1. Click the "Code" button on GitHub
2. Select "Codespaces" tab
3. Click "Create codespace on main"
4. Wait for the environment to set up
5. The app will automatically start on port 8000

### Manual Setup
```bash
# Clone the repository
git clone https://github.com/SyedRaffiq01/SYQ-AI-Travel-Planner.git
cd SYQ-AI-Travel-Planner

# Navigate to the app directory
cd "Travel Planner agent/Travel-Planner-AI"

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Using Docker
```bash
# Build the image
docker build -t travel-planner-ai .

# Run the container
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key_here travel-planner-ai
```

## 🔧 Environment Variables

Create a `.env` file in the `Travel Planner agent/Travel-Planner-AI` directory:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
SERP_API_KEY=your_serpapi_key_here  # Optional, for flight data
```

### Getting API Keys

1. **Gemini API Key**: 
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key

2. **SerpAPI Key** (Optional):
   - Go to [SerpAPI](https://serpapi.com/)
   - Sign up and get your API key

## 📱 Usage

1. Open the application in your browser
2. Fill in your travel details:
   - Source and destination
   - Travel dates
   - Budget in INR
   - Number of travelers
   - Your interests
3. Click "Generate Plan" to get your AI-powered itinerary
4. Use the chat feature to ask questions about your plan

## 🌐 Live Demo

- **Railway**: [Your Railway URL]
- **Render**: [Your Render URL]
- **Vercel**: [Your Vercel URL]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the [Issues](https://github.com/SyedRaffiq01/SYQ-AI-Travel-Planner/issues) page
2. Create a new issue if your problem isn't listed
3. Provide detailed information about the error

---

Made with ❤️ by [SyedRaffiq01](https://github.com/SyedRaffiq01)