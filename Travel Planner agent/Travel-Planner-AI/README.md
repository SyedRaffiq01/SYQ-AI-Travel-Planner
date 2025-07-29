# SYQ AI Travel Planner 🌍

A comprehensive travel planning application powered by Google's Gemini AI that generates personalized travel itineraries with Indian Rupee (INR) currency support.

![Travel Planner](https://img.shields.io/badge/Travel-Planner-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-red)
![Currency](https://img.shields.io/badge/Currency-INR-orange)

## ✨ Features

- **🤖 AI-Powered Planning**: Uses Google's Gemini AI for intelligent travel recommendations
- **💰 INR Currency Support**: All budgets and costs displayed in Indian Rupees (₹)
- **📅 Day-by-Day Itinerary**: Detailed daily schedules with activities and timings
- **🏨 Accommodation Recommendations**: Budget-friendly hotel and lodging suggestions
- **✈️ Flight Integration**: Optional flight search with real-time pricing in INR
- **🍽️ Food Recommendations**: Local cuisine and restaurant suggestions
- **🚌 Transportation Options**: Local transport recommendations and costs
- **💬 Interactive Chat**: Ask questions about your generated travel plan
- **🌤️ Weather Considerations**: Weather-based recommendations for travel dates

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- (Optional) SerpAPI key for flight data

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SyedRaffiq01/SYQ-AI-Travel-Planner.git
   cd SYQ-AI-Travel-Planner
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file and add your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   SERP_API_KEY=your_serp_api_key_here  # Optional for flight data
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8000`

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve the main application page |
| `/generate-plan` | POST | Generate comprehensive travel plan |
| `/chat` | POST | Chat about existing travel plan |
| `/plan-trip` | POST | Legacy endpoint for backward compatibility |

## 💡 Usage

1. **Enter Travel Details**:
   - Source and destination locations
   - Travel dates (start and end)
   - Budget in Indian Rupees (₹)
   - Number of travelers
   - Interests (comma-separated)
   - Optional: Include flight details

2. **Generate Plan**: Click "Generate Travel Plan" to get your AI-powered itinerary

3. **Interactive Chat**: Ask questions about your plan using the chat feature

4. **Flight Options**: If enabled, view flight options with prices in INR

## 🏗️ Project Structure

```
SYQ-AI-Travel-Planner/
├── app.py                 # FastAPI backend application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
└── static/              # Frontend files
    ├── index.html       # Main application interface
    ├── script.js        # Frontend JavaScript logic
    └── styles.css       # Application styling
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key for AI responses |
| `GOOGLE_API_KEY` | Yes | Alternative name for Gemini API key |
| `SERP_API_KEY` | No | SerpAPI key for flight data (optional) |

### Getting API Keys

1. **Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy and paste into your `.env` file

2. **SerpAPI Key** (Optional):
   - Visit [SerpAPI](https://serpapi.com/)
   - Sign up for a free account
   - Get your API key from the dashboard

## 🌟 Key Features Explained

### INR Currency Support
- All budget inputs accept Indian Rupees
- Cost breakdowns displayed in ₹
- Flight prices fetched in INR currency
- Local expense estimates in Indian context

### AI-Powered Recommendations
- Personalized itineraries based on interests
- Weather-appropriate activity suggestions
- Budget-conscious recommendations
- Cultural and local insights

### Interactive Experience
- Real-time chat with AI about your travel plan
- Modify and refine your itinerary
- Get specific answers about destinations
- Explore alternative options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for intelligent travel recommendations
- SerpAPI for flight data integration
- FastAPI for the robust backend framework
- The open-source community for various tools and libraries

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the documentation
- Review the API key setup

---

**Made with ❤️ by Syed Raffiq**

*Happy Traveling! 🧳✈️*