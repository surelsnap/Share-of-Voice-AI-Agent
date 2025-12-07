# Atomberg SoV Analysis AI Agent

An intelligent AI agent that analyzes Share of Voice (SoV) for Atomberg across multiple platforms including Google, YouTube, Instagram, and X (Twitter).

##  Problem Statement

Build an AI agent that:
- Searches for "smart fan" and related keywords on Google/YouTube/Instagram/X
- Analyzes top N search results
- Quantifies Share of Voice (SoV) for Atomberg vs. competitors
- Provides sentiment analysis and Share of Positive Voice
- Generates actionable insights and recommendations

##  Features

### Core Features
- **Multi-Platform Search**: YouTube (primary) and Google (secondary) with enhanced metrics
- **Comprehensive SoV Calculation**: 
  - Presence score (40%): Brand mentions in titles/descriptions
  - Engagement score (30%): Normalized views, likes, comments
  - Sentiment score (20%): Share of positive voice
  - Dominance score (10%): Ranking position in results
- **Cross-Keyword Analysis**: Identifies content gaps and opportunity areas across keywords
- **Enhanced YouTube Metrics**: Comments collection, engagement rate calculation, video age normalization
- **Sentiment Analysis**: Uses VADER and TextBlob including comment analysis
- **Automated Insights**: Generates actionable recommendations with priority levels
- **Visualizations**: Creates charts and graphs for better understanding

### Advanced AI Features
1. **Predictive SoV Forecasting Engine**: Forecasts future SoV trends 3-6 months ahead with confidence intervals
2. **Content Gap Heatmap Generator**: Visual intelligence system identifying exactly where content opportunities exist
3. **Viral Content Deconstruction Engine**: Reverse-engineers why competitor content goes viral and generates "viral recipes"
4. **Real-Time Opportunity Alert System**: Proactive monitoring with instant alerts for opportunities and threats
5. **ROI-Focused Content Recommendation Engine**: Predicts content ROI and helps prioritize marketing investments
6. **Brand Perception Gap Analyzer**: Compares intended messaging with actual market perception

##  Requirements

- Python 3.8+
- Internet connection for API calls
- API keys for production mode

##  Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd atomberg
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **Choose your mode:**

### Demo Mode (Default - No Setup Required)
- Works immediately without API keys
- Uses mock data to demonstrate functionality
- Perfect for testing and understanding the agent

### Production Mode (API Keys Required)
- Provides real search results from Google and YouTube
- Fetches actual comments and engagement metrics

**To enable Production Mode:**

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. **Get YouTube Data API v3 Key:**
   - Visit: https://console.cloud.google.com/apis/credentials
   - Create a new project or select existing
   - Click "Create Credentials" → "API Key"
   - Enable "YouTube Data API v3" for your project
   - Copy the API key

3. **Get Google Custom Search API:**
   - Create API Key: https://console.cloud.google.com/apis/credentials
   - Create Custom Search Engine: https://programmablesearchengine.google.com/
   - Enable "Custom Search API" in Google Cloud Console
   - Copy both API Key and Search Engine ID

4. **Add keys to `.env` file:**
```env
YOUTUBE_API_KEY=your_youtube_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_custom_search_engine_id_here
```

##  Usage

Run the main script:
```bash
python main.py
```

The agent will automatically detect:
- **PRODUCTION MODE** if API keys are configured
- **DEMO MODE** if no API keys (uses mock data)

The agent will:
1. Search across configured platforms
2. Analyze SoV metrics
3. Generate advanced AI insights (forecasting, gaps, viral analysis, alerts, ROI, perception)
4. Create visualizations
5. Save comprehensive JSON results

##  Output

The agent generates:
- `output/sov_analysis_results.json`: Complete analysis data including all advanced AI features
- `output/visualizations/sov_comparison.png`: SoV comparison chart

The JSON output includes:
- Standard SoV analysis (mentions, engagement, sentiment, dominance)
- Cross-keyword analysis and content gaps
- **SoV Forecasts**: 3-6 month predictions with confidence intervals
- **Content Gap Heatmap**: Topic, format, and platform-specific opportunities
- **Viral Content Analysis**: Hook patterns, emotional triggers, viral recipes
- **Real-Time Alerts**: Prioritized alerts with actionable recommendations
- **ROI Recommendations**: Content ideas with predicted ROI and resource optimization
- **Perception Gap Analysis**: Messaging alignment and brand perception insights

##  Configuration

Edit `config.py` to customize:
- Search keywords
- Competitor brands
- Number of results to analyze
- Enabled platforms
- Output directories

## 🎓 Author

Created as part of Atomberg's AI Internship Problem Statement solution.


