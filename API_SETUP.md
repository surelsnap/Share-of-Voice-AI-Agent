# API Keys Setup Guide

## Where to Insert API Keys

API keys are configured in the **`.env`** file in the project root directory.

## Step-by-Step Setup

### 1. Create `.env` File

Copy the example file:
```bash
cp .env.example .env
```

Or create a new `.env` file in the project root with the following structure:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_custom_search_engine_id_here
```

### 2. Get YouTube Data API v3 Key

**Purpose:** Fetches real YouTube video data, comments, and engagement metrics

**Steps:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **API Key**
5. Copy the generated API key
6. Go to **APIs & Services** → **Library**
7. Search for "YouTube Data API v3"
8. Click **Enable** to activate the API for your project
9. Paste the key in `.env` as `YOUTUBE_API_KEY`

**API Quota:** 10,000 units/day (free tier)
**Cost:** Free for reasonable usage

### 3. Get Google Custom Search API

**Purpose:** Performs real Google searches for keyword analysis

**Steps:**

**Part A: Create API Key**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Use the same project as YouTube API (or create new)
3. Navigate to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **API Key**
5. Copy the generated API key
6. Go to **APIs & Services** → **Library**
7. Search for "Custom Search API"
8. Click **Enable** to activate the API
9. Paste the key in `.env` as `GOOGLE_API_KEY`

**Part B: Create Custom Search Engine**
1. Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
2. Click **Add** to create a new search engine
3. Enter:
   - **Sites to search:** `*` (to search entire web)
   - **Name:** Atomberg SoV Analysis (or any name)
4. Click **Create**
5. Click **Control Panel** → **Basics**
6. Copy the **Search engine ID**
7. Paste in `.env` as `GOOGLE_CSE_ID`

**API Quota:** 100 queries/day (free tier)
**Cost:** Free for reasonable usage

### 4. Verify Setup

After adding API keys to `.env`, run:
```bash
python main.py
```

You should see:
```
🔧 MODE: PRODUCTION (Using API keys)
   ✓ YouTube API: Configured
   ✓ Google API: Configured
```

## File Structure

```
atomberg/
├── .env                    # ← ADD YOUR API KEYS HERE (not in git)
├── .env.example            # Template file (safe to commit)
├── config.py               # Reads from .env file
└── ...
```

## Security Notes

⚠️ **Important:**
- Never commit `.env` file to git (it's in `.gitignore`)
- Keep your API keys secret
- Don't share API keys publicly
- Rotate keys if accidentally exposed

## Mode Detection

The agent automatically detects the mode:

- **Production Mode:** If at least one API key is present
- **Demo Mode:** If no API keys (or all keys are empty)

You can mix modes:
- Only YouTube API → Production mode for YouTube, Demo for Google
- Only Google API → Production mode for Google, Demo for YouTube
- Both APIs → Full production mode

## Troubleshooting

### "API key not valid" error
- Check that the API key is correctly copied (no extra spaces)
- Verify the API is enabled in Google Cloud Console
- Check that billing is enabled (required for some APIs)

### "Quota exceeded" error
- You've hit the daily API limit
- Wait 24 hours or upgrade to paid tier
- The agent will fall back to demo mode automatically

### "Search engine ID not found"
- Verify the Custom Search Engine ID is correct
- Check that the search engine is active in Programmable Search Engine dashboard

## Optional: Twitter/Instagram APIs

For future implementation, you can also add:
```env
TWITTER_BEARER_TOKEN=your_twitter_token
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

These are currently not used but reserved for future features.

