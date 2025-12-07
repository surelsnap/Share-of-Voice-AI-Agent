# Configuration file
# Stores all settings and API keys

import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# Search Configuration
# Keywords prioritized by search intent
SEARCH_KEYWORDS = [
    "smart fan",
    "energy efficient fan",
    "BLDC fan",
    "smart ceiling fan",
    "WiFi fan"
]

COMPETITOR_BRANDS = ["Havells", "Crompton", "Orient", "Bajaj", "Usha", "Luminous"]
BRAND_NAME = "Atomberg"

# Platform Configuration - Priority: YouTube (Primary), Google (Secondary)
PLATFORMS = {
    "youtube": True,   # Primary - Best for engagement metrics and visual analysis
    "google": True,    # Secondary - Broader market presence
    "twitter": False,  # Tertiary - Requires API keys
    "instagram": False # Tertiary - Requires API keys
}

# Search Parameters
TOP_N_RESULTS = 20  # Justification: YouTube shows 20 results per page
                    # Provides sufficient data without API quota issues

# SoV Calculation Weights (as per implementation guide)
SOV_WEIGHTS = {
    "presence_score": 0.4,      # Mentions in titles/descriptions
    "engagement_score": 0.3,    # Views/likes/comments
    "sentiment_score": 0.2,     # Positive sentiment ratio
    "dominance_score": 0.1      # Ranking position
}

# API Keys (set these in .env file for production mode)
# Leave empty to run in demo mode with mock data
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")

# Mode Detection
# Production mode: At least one API key is configured
# Demo mode: No API keys configured (uses mock data)
PRODUCTION_MODE = bool(YOUTUBE_API_KEY or GOOGLE_API_KEY)
DEMO_MODE = not PRODUCTION_MODE

# Data Collection Settings
MAX_COMMENTS_PER_VIDEO = 100  # Limit comments per video for analysis
ENGAGEMENT_NORMALIZATION = True  # Normalize engagement across video ages

# Output Configuration
OUTPUT_DIR = "output"
RESULTS_FILE = f"{OUTPUT_DIR}/sov_analysis_results.json"
VISUALIZATIONS_DIR = f"{OUTPUT_DIR}/visualizations"

