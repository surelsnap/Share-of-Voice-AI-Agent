# Search engines for Google and YouTube
# I used APIs and libraries to search these platforms

import requests
import time

# try to import youtube search library
try:
    from youtubesearchpython import VideosSearch
    VideosSearch_available = True
except ImportError:
    VideosSearch = None
    VideosSearch_available = False
    print("Warning: youtube-search-python not installed")


class GoogleSearcher:
    # Google search class - can use API or demo mode
    
    def __init__(self, config):
        self.config = config
        self.api_key = config.GOOGLE_API_KEY
        self.cse_id = config.GOOGLE_CSE_ID
        self.top_n = config.TOP_N_RESULTS
        
        # check if we have API keys
        if self.api_key and self.cse_id:
            self.production_mode = True
        else:
            self.production_mode = False
    
    def search(self, keyword: str, num_results: int = None) -> List[Dict]:
        """Search Google for a keyword"""
        if num_results is None:
            num_results = self.top_n
        
        results = []
        
        # try to use API if we have keys
        if self.production_mode:
            try:
                url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    "key": self.api_key,
                    "cx": self.cse_id,
                    "q": keyword,
                    "num": min(num_results, 10)  # API only allows 10 at a time
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    items = data.get("items", [])
                    for item in items[:num_results]:
                        results.append({
                            "title": item.get("title", ""),
                            "link": item.get("link", ""),
                            "snippet": item.get("snippet", ""),
                            "platform": "google",
                            "keyword": keyword,
                            "mode": "production"
                        })
                    print(f"    Found {len(results)} Google results (production mode)")
                else:
                    print(f"    API error: {response.status_code}")
            except Exception as e:
                print(f"    API failed: {e}, using demo mode")
                self.production_mode = False
        
        # if no results, use mock data (demo mode)
        if not results:
            print(f"    Using demo mode for Google search")
            results = self._create_mock_results(keyword, num_results)
        
        return results
    
    def _create_mock_results(self, keyword, num_results):
        # create fake results for demo mode
        # TODO: maybe improve this later
        mock_results = []
        for i in range(min(num_results, 10)):
            mock_results.append({
                "title": f"Smart Fan Review - Result {i+1}",
                "link": f"https://example.com/smart-fan-{i+1}",
                "snippet": f"Discussion about {keyword} and various fan brands including Atomberg, Havells, and Crompton.",
                "platform": "google",
                "keyword": keyword,
                "mode": "demo"
            })
        return mock_results
    
    def search_all_keywords(self) -> List[Dict]:
        """Search all configured keywords"""
        all_results = []
        for keyword in self.config.SEARCH_KEYWORDS:
            print(f"    Searching: '{keyword}'")
            results = self.search(keyword)
            all_results.extend(results)
            time.sleep(1)  # Rate limiting
        return all_results


class YouTubeSearcher:
    """YouTube Search implementation with enhanced engagement metrics - Supports both Production and Demo modes"""
    
    def __init__(self, config):
        self.config = config
        self.top_n = config.TOP_N_RESULTS
        self.max_comments = config.MAX_COMMENTS_PER_VIDEO
        self.youtube_api_key = config.YOUTUBE_API_KEY
        self.production_mode = config.PRODUCTION_MODE and bool(self.youtube_api_key)
    
    def _extract_engagement_metrics(self, item: Dict) -> Dict:
        """Extract engagement metrics from YouTube video data"""
        try:
            # Parse views
            views_text = item.get("viewCount", {}).get("text", "0")
            views = self._parse_views(views_text)
            
            # Extract likes (if available)
            likes_text = item.get("accessibility", {}).get("title", "")
            # Try to extract likes from accessibility text or use estimate
            likes = self._estimate_likes(views) if "likes" not in item else item.get("likes", 0)
            
            # Get comment count (if available)
            comment_count = item.get("commentCount", 0)
            
            return {
                "views": views,
                "likes": likes,
                "comment_count": comment_count,
                "views_text": views_text
            }
        except Exception as e:
            return {"views": 0, "likes": 0, "comment_count": 0, "views_text": "0"}
    
    def _parse_views(self, views_str: str) -> int:
        """Parse YouTube views string to integer"""
        try:
            views_str = views_str.replace(",", "").replace(" views", "").strip()
            if "K" in views_str.upper():
                return int(float(views_str.upper().replace("K", "").replace(" views", "")) * 1000)
            elif "M" in views_str.upper():
                return int(float(views_str.upper().replace("M", "").replace(" views", "")) * 1000000)
            elif "B" in views_str.upper():
                return int(float(views_str.upper().replace("B", "").replace(" views", "")) * 1000000000)
            else:
                return int(views_str)
        except:
            return 0
    
    def _estimate_likes(self, views: int) -> int:
        """Estimate likes based on views (typical YouTube ratio ~1-3%)"""
        # Typical engagement: 1-3% of views are likes
        import random
        return int(views * random.uniform(0.01, 0.03))
    
    def _collect_comments(self, video_id: str) -> List[str]:
        """Collect comments for a video using YouTube Data API v3 (Production) or return empty (Demo)"""
        if self.production_mode and video_id:
            try:
                # Use YouTube Data API v3 to fetch comments
                url = "https://www.googleapis.com/youtube/v3/commentThreads"
                params = {
                    "key": self.youtube_api_key,
                    "part": "snippet",
                    "videoId": video_id,
                    "maxResults": min(self.max_comments, 100),  # API limit
                    "order": "relevance"
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    comments = []
                    for item in data.get("items", []):
                        comment_text = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {}).get("textDisplay", "")
                        if comment_text:
                            comments.append(comment_text)
                    return comments[:self.max_comments]
                else:
                    print(f"      ⚠ YouTube Comments API returned status {response.status_code}")
            except Exception as e:
                print(f"      ⚠ Failed to fetch comments: {e}")
        
        # Demo mode or API failure - return empty
        return []
    
    def search(self, keyword: str, num_results: int = None) -> List[Dict]:
        """Search YouTube for a keyword with enhanced metrics"""
        if num_results is None:
            num_results = self.top_n
        
        results = []
        
        # PRODUCTION MODE: Use youtube-search-python (works without API) + YouTube Data API for comments
        # DEMO MODE: Use youtube-search-python with mock data fallback
        
        try:
            if VideosSearch:
                # Using youtube-search-python library (works in both modes)
                search = VideosSearch(keyword, limit=num_results)
                search_results = search.result()
                
                mode_indicator = "production" if self.production_mode else "demo"
                
                for idx, item in enumerate(search_results.get("result", [])):
                    engagement = self._extract_engagement_metrics(item)
                    
                    # Extract video ID from link
                    video_link = item.get("link", "")
                    video_id = video_link.split("v=")[-1].split("&")[0] if "v=" in video_link else ""
                    
                    # Collect comments (Production mode uses API, Demo mode returns empty)
                    comments = self._collect_comments(video_id)
                    
                    result = {
                        "title": item.get("title", ""),
                        "link": video_link,
                        "snippet": item.get("descriptionSnippet", [{}])[0].get("text", "") if item.get("descriptionSnippet") else "",
                        "views": engagement["views_text"],
                        "views_count": engagement["views"],
                        "likes": engagement["likes"],
                        "comment_count": engagement["comment_count"],
                        "comments": comments[:self.max_comments],  # Limit comments
                        "duration": item.get("duration", ""),
                        "channel": item.get("channel", {}).get("name", ""),
                        "published_time": item.get("publishedTime", ""),
                        "age_days": self._calculate_age_days(item.get("publishedTime", "")),
                        "platform": "youtube",
                        "keyword": keyword,
                        "position": idx + 1,  # For ranking dominance calculation
                        "mode": mode_indicator
                    }
                    results.append(result)
                
                if self.production_mode:
                    print(f"    ✓ Production mode: Found {len(results)} real YouTube results")
                else:
                    print(f"    📝 Demo mode: Found {len(results)} YouTube results (limited comment data)")
            else:
                raise ImportError("youtube-search-python not available")
        except Exception as e:
            print(f"    ⚠ YouTube search failed: {e}, using demo mode")
            # Fallback mock results
            results = self._create_mock_results(keyword, num_results)
        
        return results
    
    def _calculate_age_days(self, published_time: str) -> int:
        """Calculate video age in days"""
        # Parse published time (e.g., "2 weeks ago", "3 months ago")
        try:
            if "week" in published_time.lower():
                weeks = int(published_time.split()[0])
                return weeks * 7
            elif "month" in published_time.lower():
                months = int(published_time.split()[0])
                return months * 30
            elif "year" in published_time.lower():
                years = int(published_time.split()[0])
                return years * 365
            elif "day" in published_time.lower():
                return int(published_time.split()[0])
            else:
                return 30  # Default
        except:
            return 30
    
    def _create_mock_results(self, keyword: str, num_results: int) -> List[Dict]:
        """Create mock results for demonstration with enhanced metrics (Demo Mode)"""
        import random
        mock_results = []
        for i in range(min(num_results, 10)):
            views = (i+1) * 10000 + random.randint(1000, 5000)
            likes = int(views * random.uniform(0.01, 0.03))
            comments = int(views * random.uniform(0.001, 0.005))
            
            mock_results.append({
                "title": f"Smart Fan Review Video {i+1} - {keyword}",
                "link": f"https://youtube.com/watch?v=mock{i+1}",
                "snippet": f"Video about {keyword} featuring Atomberg and other fan brands",
                "views": f"{views:,}",
                "views_count": views,
                "likes": likes,
                "comment_count": comments,
                "comments": [],  # Mock comments can be added if needed
                "duration": f"{5+i}:30",
                "channel": f"Tech Channel {i+1}",
                "published_time": f"{i+1} weeks ago",
                "age_days": (i+1) * 7,
                "platform": "youtube",
                "keyword": keyword,
                "position": i + 1,
                "mode": "demo"
            })
        return mock_results
    
    def search_all_keywords(self) -> List[Dict]:
        """Search all configured keywords"""
        all_results = []
        for keyword in self.config.SEARCH_KEYWORDS:
            print(f"    Searching: '{keyword}'")
            results = self.search(keyword)
            all_results.extend(results)
            time.sleep(1)  # Rate limiting
        return all_results

