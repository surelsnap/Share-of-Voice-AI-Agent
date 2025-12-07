# Quick Start Guide

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. **Choose your mode:**

### Option A: Demo Mode (No API keys needed)
- Works immediately without any setup
- Uses mock data to demonstrate functionality
- Perfect for testing and understanding the agent

### Option B: Production Mode (API keys required)
- Provides real search results from Google and YouTube
- Fetches actual comments and engagement metrics
- Requires API keys (see setup below)

## Setting Up API Keys (Production Mode)

1. **Copy the example environment file:**
```bash
cp .env.example .env
```

2. **Get YouTube Data API v3 Key:**
   - Go to: https://console.cloud.google.com/apis/credentials
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

## Running the Agent

Simply execute:
```bash
python main.py
```

The agent will automatically detect:
- **PRODUCTION MODE** if API keys are configured
- **DEMO MODE** if no API keys (uses mock data)

## What It Does

1. **Searches** for "smart fan" and related keywords on Google and YouTube
2. **Analyzes** top 20 results per platform
3. **Calculates** Share of Voice (SoV) metrics:
   - Brand mentions
   - Engagement rates
   - Sentiment analysis
   - Weighted SoV percentage
4. **Generates** advanced AI insights:
   - SoV forecasting
   - Content gap analysis
   - Viral content deconstruction
   - Real-time alerts
   - ROI recommendations
   - Perception gap analysis

## Output Files

- `output/sov_analysis_results.json` - Complete analysis data with all AI features
- `output/visualizations/sov_comparison.png` - SoV comparison chart

## Mode Comparison

| Feature | Demo Mode | Production Mode |
|---------|-----------|-----------------|
| Search Results | Mock data | Real API results |
| Comments | Empty | Real comments (if API key) |
| Engagement Metrics | Estimated | Actual metrics |
| Use Case | Testing/Demo | Production analysis |

