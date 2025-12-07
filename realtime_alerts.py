"""
Real-Time Opportunity Alert System
Proactive monitoring system that instantly alerts about emerging opportunities or threats
"""
from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict


class RealtimeAlertSystem:
    """Monitor and alert on real-time opportunities and threats"""
    
    def __init__(self, config):
        self.config = config
        self.brand_name = config.BRAND_NAME
        self.competitors = config.COMPETITOR_BRANDS
        self.alert_history = []
    
    def generate_alerts(self, platform_data: Dict, sov_data: Dict, sentiment_data: Dict) -> List[Dict]:
        """Generate all real-time alerts"""
        alerts = []
        
        # Check for various alert types
        alerts.extend(self._detect_competitor_launches(platform_data))
        alerts.extend(self._detect_sentiment_crises(sentiment_data))
        alerts.extend(self._detect_influencer_mentions(platform_data))
        alerts.extend(self._detect_trend_emergence(platform_data))
        alerts.extend(self._detect_white_space_opportunities(platform_data))
        alerts.extend(self._detect_platform_specific_triggers(platform_data))
        
        # Sort by priority
        alerts.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
        
        return alerts
    
    def _detect_competitor_launches(self, platform_data: Dict) -> List[Dict]:
        """Detect when competitors release new products or campaigns"""
        alerts = []
        
        # Keywords that indicate new launches
        launch_keywords = ["new", "launch", "announce", "release", "introducing", "latest"]
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    title = result.get("title", "").lower()
                    snippet = result.get("snippet", "").lower()
                    text = f"{title} {snippet}"
                    
                    # Check if competitor mentioned with launch keywords
                    for competitor in self.competitors:
                        if competitor.lower() in text:
                            if any(kw in text for kw in launch_keywords):
                                # Check recency (if available)
                                published_time = result.get("published_time", "")
                                is_recent = self._is_recent(published_time)
                                
                                alerts.append({
                                    "type": "competitor_launch",
                                    "priority": "high",
                                    "priority_score": 90 if is_recent else 70,
                                    "title": f"{competitor} New Product/Campaign Detected",
                                    "description": f"New content detected: {title[:100]}",
                                    "platform": platform,
                                    "link": result.get("link", ""),
                                    "competitor": competitor,
                                    "suggested_action": f"Monitor {competitor}'s new offering and prepare response content",
                                    "urgency": "high" if is_recent else "medium"
                                })
        
        return alerts
    
    def _detect_sentiment_crises(self, sentiment_data: Dict) -> List[Dict]:
        """Detect negative sentiment spikes before they become trends"""
        alerts = []
        
        for platform, data in sentiment_data.items():
            if isinstance(data, dict):
                sentiment_stats = data.get("sentiment_stats", {})
                brand_sentiment = sentiment_stats.get(self.brand_name, {})
                
                if brand_sentiment:
                    positive_ratio = brand_sentiment.get("positive_ratio", 0)
                    
                    if positive_ratio < 0.4:  # Less than 40% positive
                        alerts.append({
                            "type": "sentiment_crisis",
                            "priority": "high",
                            "priority_score": 85,
                            "title": f"Negative Sentiment Spike on {platform}",
                            "description": f"Only {positive_ratio*100:.1f}% positive mentions detected",
                            "platform": platform,
                            "positive_ratio": positive_ratio,
                            "suggested_action": "Review recent content and comments. Address common concerns proactively.",
                            "urgency": "high"
                        })
        
        return alerts
    
    def _detect_influencer_mentions(self, platform_data: Dict) -> List[Dict]:
        """Detect when relevant influencers mention smart fans"""
        alerts = []
        
        # Keywords that indicate influencer content
        influencer_indicators = ["review", "unboxing", "sponsored", "collab", "partner"]
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    title = result.get("title", "").lower()
                    channel = result.get("channel", "").lower()
                    
                    # Check for high engagement (potential influencer)
                    views = result.get("views_count", 0) or 0
                    if views > 50000:  # High view count suggests influencer
                        if any(indicator in title for indicator in influencer_indicators):
                            # Check if mentions any brand
                            text = f"{title} {result.get('snippet', '')}".lower()
                            if self.brand_name.lower() in text:
                                alerts.append({
                                    "type": "influencer_mention",
                                    "priority": "medium",
                                    "priority_score": 75,
                                    "title": f"Influencer Mention Detected",
                                    "description": f"High-engagement content mentions {self.brand_name}",
                                    "platform": platform,
                                    "channel": channel,
                                    "views": views,
                                    "link": result.get("link", ""),
                                    "suggested_action": "Engage with the influencer. Share and amplify positive mentions.",
                                    "urgency": "medium"
                                })
                            elif any(comp.lower() in text for comp in self.competitors):
                                alerts.append({
                                    "type": "influencer_opportunity",
                                    "priority": "medium",
                                    "priority_score": 65,
                                    "title": f"Influencer Opportunity: Competitor Mentioned",
                                    "description": f"Influencer content mentions competitors but not {self.brand_name}",
                                    "platform": platform,
                                    "channel": channel,
                                    "suggested_action": "Reach out to influencer for potential collaboration",
                                    "urgency": "medium"
                                })
        
        return alerts
    
    def _detect_trend_emergence(self, platform_data: Dict) -> List[Dict]:
        """Identify rising topics before they become mainstream"""
        alerts = []
        
        # Track keyword frequency
        keyword_frequency = defaultdict(int)
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    keyword = result.get("keyword", "")
                    keyword_frequency[keyword] += 1
        
        # Identify emerging trends (keywords with increasing frequency)
        for keyword, frequency in keyword_frequency.items():
            if frequency > 5 and keyword not in self.config.SEARCH_KEYWORDS:
                # Check if Atomberg has content for this keyword
                atomberg_has_content = False
                for platform, results in platform_data.items():
                    if isinstance(results, list):
                        for result in results:
                            if keyword.lower() in result.get("keyword", "").lower():
                                text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                                if self.brand_name.lower() in text:
                                    atomberg_has_content = True
                                    break
                
                if not atomberg_has_content:
                    alerts.append({
                        "type": "trend_emergence",
                        "priority": "medium",
                        "priority_score": 60,
                        "title": f"Emerging Trend: {keyword}",
                        "description": f"Keyword '{keyword}' appearing {frequency} times but Atomberg has no content",
                        "keyword": keyword,
                        "frequency": frequency,
                        "suggested_action": f"Create content targeting '{keyword}' before it becomes mainstream",
                        "urgency": "medium"
                    })
        
        return alerts
    
    def _detect_white_space_opportunities(self, platform_data: Dict) -> List[Dict]:
        """Flag when competitors leave gaps in coverage"""
        alerts = []
        
        # Analyze coverage by keyword
        keyword_coverage = defaultdict(lambda: {"atomberg": 0, "competitors": 0})
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    keyword = result.get("keyword", "")
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    
                    if self.brand_name.lower() in text:
                        keyword_coverage[keyword]["atomberg"] += 1
                    elif any(comp.lower() in text for comp in self.competitors):
                        keyword_coverage[keyword]["competitors"] += 1
        
        # Find white spaces
        for keyword, coverage in keyword_coverage.items():
            if coverage["competitors"] == 0 and coverage["atomberg"] == 0:
                # No one is covering this - opportunity
                alerts.append({
                    "type": "white_space_opportunity",
                    "priority": "high",
                    "priority_score": 80,
                    "title": f"White Space Opportunity: {keyword}",
                    "description": f"No competitor content found for '{keyword}' - first-mover advantage",
                    "keyword": keyword,
                    "suggested_action": f"Create first-mover content for '{keyword}' to establish authority",
                    "urgency": "high"
                })
        
        return alerts
    
    def _detect_platform_specific_triggers(self, platform_data: Dict) -> List[Dict]:
        """Platform-specific alert triggers"""
        alerts = []
        
        for platform, results in platform_data.items():
            if not isinstance(results, list):
                continue
            
            # YouTube-specific: High engagement videos
            if platform == "youtube":
                for result in results:
                    views = result.get("views_count", 0) or 0
                    if views > 100000:
                        text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                        if self.brand_name.lower() not in text:
                            # High-performing video doesn't mention Atomberg
                            alerts.append({
                                "type": "platform_opportunity",
                                "priority": "medium",
                                "priority_score": 55,
                                "title": f"High-Performing Video Opportunity on YouTube",
                                "description": f"Video with {views:,} views doesn't mention {self.brand_name}",
                                "platform": platform,
                                "link": result.get("link", ""),
                                "suggested_action": "Consider creating similar content or reaching out for collaboration",
                                "urgency": "low"
                            })
            
            # Google-specific: Top ranking opportunities
            elif platform == "google":
                for idx, result in enumerate(results[:5]):  # Top 5 results
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    if self.brand_name.lower() not in text and idx < 3:
                        alerts.append({
                            "type": "seo_opportunity",
                            "priority": "medium",
                            "priority_score": 65,
                            "title": f"Top Ranking Opportunity on Google",
                            "description": f"Result #{idx+1} doesn't mention {self.brand_name}",
                            "platform": platform,
                            "position": idx + 1,
                            "suggested_action": "Create SEO-optimized content to rank for this keyword",
                            "urgency": "medium"
                        })
        
        return alerts
    
    def _is_recent(self, published_time: str) -> bool:
        """Check if content is recent (within last 7 days)"""
        if not published_time:
            return False
        
        try:
            # Parse time strings like "2 weeks ago", "3 days ago"
            if "day" in published_time.lower():
                days = int(published_time.split()[0])
                return days <= 7
            elif "week" in published_time.lower():
                return False  # Not recent enough
            elif "hour" in published_time.lower():
                return True  # Very recent
            else:
                return False
        except:
            return False
    
    def format_alert_card(self, alert: Dict) -> Dict:
        """Format alert as actionable card"""
        priority_colors = {
            "high": "#FF6B6B",
            "medium": "#FFA500",
            "low": "#4ECDC4"
        }
        
        return {
            "alert_id": f"{alert['type']}_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "type": alert.get("type", "unknown"),
            "priority": alert.get("priority", "medium"),
            "priority_color": priority_colors.get(alert.get("priority", "medium"), "#4ECDC4"),
            "title": alert.get("title", ""),
            "description": alert.get("description", ""),
            "platform": alert.get("platform", ""),
            "suggested_action": alert.get("suggested_action", ""),
            "urgency": alert.get("urgency", "medium"),
            "priority_score": alert.get("priority_score", 0),
            "action_items": self._generate_action_items(alert),
            "link": alert.get("link", "")
        }
    
    def _generate_action_items(self, alert: Dict) -> List[str]:
        """Generate specific action items for each alert"""
        action_items = []
        alert_type = alert.get("type", "")
        
        if alert_type == "competitor_launch":
            action_items.append("Analyze competitor's new offering")
            action_items.append("Prepare comparison content highlighting Atomberg's advantages")
            action_items.append("Monitor competitor's marketing messaging")
        
        elif alert_type == "sentiment_crisis":
            action_items.append("Review recent negative comments")
            action_items.append("Identify common concerns")
            action_items.append("Create FAQ or response content addressing issues")
        
        elif alert_type == "influencer_mention":
            action_items.append("Engage with the influencer (like, comment, share)")
            action_items.append("Amplify positive mentions on social media")
            action_items.append("Consider long-term partnership")
        
        elif alert_type == "trend_emergence":
            action_items.append(f"Research keyword: {alert.get('keyword', '')}")
            action_items.append("Create content targeting emerging trend")
            action_items.append("Optimize for early SEO advantage")
        
        else:
            action_items.append("Review alert details")
            action_items.append("Assess opportunity/risk")
            action_items.append("Take appropriate action")
        
        return action_items

