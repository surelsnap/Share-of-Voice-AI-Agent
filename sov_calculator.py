# SoV Calculator - calculates share of voice metrics
# Formula: SoV = (0.4 × Presence) + (0.3 × Engagement) + (0.2 × Sentiment) + (0.1 × Dominance)
# I read about this formula in the problem statement and implemented it

from collections import defaultdict
import re
# import math  # might need this later


class SoVCalculator:
    # calculates SoV using the formula from problem statement
    
    def __init__(self, config):
        self.config = config
        self.brand_name = config.BRAND_NAME
        self.competitors = config.COMPETITOR_BRANDS
        self.all_brands = [self.brand_name] + self.competitors
        self.weights = config.SOV_WEIGHTS
    
    def count_mentions(self, results, platform):
        # count how many times each brand is mentioned
        mentions = defaultdict(int)
        total_mentions = 0
        
        for result in results:
            # get text from title and snippet
            title = result.get('title', '')
            snippet = result.get('snippet', '')
            text = (title + " " + snippet).lower()
            
            # check each brand
            for brand in self.all_brands:
                # use regex to find exact word matches (not partial)
                pattern = r'\b' + re.escape(brand.lower()) + r'\b'
                matches = re.findall(pattern, text)
                count = len(matches)
                mentions[brand] += count
                total_mentions += count
        
        # calculate percentages
        mention_percentages = {}
        if total_mentions > 0:
            for brand in self.all_brands:
                # percentage = (brand mentions / total) * 100
                mention_percentages[brand] = (mentions[brand] / total_mentions) * 100
        else:
            # no mentions found, set all to 0
            for brand in self.all_brands:
                mention_percentages[brand] = 0.0
        
        return {
            "raw_counts": dict(mentions),
            "total_mentions": total_mentions,
            "percentages": mention_percentages
        }
    
    def calculate_engagement(self, results, platform):
        """Calculate normalized engagement metrics"""
        engagement = defaultdict(lambda: {
            "count": 0, 
            "total_views": 0,
            "total_likes": 0,
            "total_comments": 0,
            "engagement_rate": 0.0
        })
        
        for idx, result in enumerate(results):
            text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
            
            # Calculate engagement based on platform
            if platform == "youtube":
                views = self._parse_views(result.get("views", "0"))
                likes = self._parse_views(result.get("likes", "0"))
                comments = result.get("comment_count", 0)
                
                # Calculate engagement rate: (likes + comments) / views
                if views > 0:
                    engagement_rate = (likes + comments) / views
                else:
                    engagement_rate = 0
                
                # Normalize by video age if available (newer videos get slight boost)
                age_days = result.get("age_days", 30)  # Default to 30 days
                if age_days > 0:
                    # Normalize: older videos need higher engagement to score well
                    normalized_rate = engagement_rate * (30 / min(age_days, 365))
                else:
                    normalized_rate = engagement_rate
                
                # Weighted engagement score
                engagement_value = views * 0.5 + (likes * 100) * 0.3 + (comments * 50) * 0.2
            else:
                # For other platforms, use simpler metrics
                engagement_value = 100
                normalized_rate = 0.1
                views = 100
                likes = 10
                comments = 5
            
            # Check which brands are mentioned
            for brand in self.all_brands:
                pattern = r'\b' + re.escape(brand.lower()) + r'\b'
                if re.search(pattern, text):
                    engagement[brand]["count"] += 1
                    engagement[brand]["total_views"] += views
                    engagement[brand]["total_likes"] += likes
                    engagement[brand]["total_comments"] += comments
                    engagement[brand]["engagement_rate"] += normalized_rate
        
        # Calculate engagement percentages
        total_engagement = sum(e["total_views"] for e in engagement.values())
        engagement_percentages = {}
        avg_engagement_rates = {}
        
        if total_engagement > 0:
            for brand in self.all_brands:
                brand_views = engagement[brand]["total_views"]
                engagement_percentages[brand] = (brand_views / total_engagement) * 100
                if engagement[brand]["count"] > 0:
                    avg_engagement_rates[brand] = engagement[brand]["engagement_rate"] / engagement[brand]["count"]
                else:
                    avg_engagement_rates[brand] = 0.0
        else:
            for brand in self.all_brands:
                engagement_percentages[brand] = 0.0
                avg_engagement_rates[brand] = 0.0
        
        return {
            "raw_engagement": {
                k: {
                    "views": v["total_views"],
                    "likes": v["total_likes"],
                    "comments": v["total_comments"]
                } for k, v in engagement.items()
            },
            "total_engagement": total_engagement,
            "percentages": engagement_percentages,
            "avg_engagement_rates": avg_engagement_rates
        }
    
    def _parse_views(self, views_str: str) -> int:
        """Parse YouTube views string to integer"""
        try:
            # Remove commas and extract number
            views_str = views_str.replace(",", "").replace(" views", "").strip()
            if "K" in views_str.upper():
                return int(float(views_str.upper().replace("K", "")) * 1000)
            elif "M" in views_str.upper():
                return int(float(views_str.upper().replace("M", "")) * 1000000)
            else:
                return int(views_str)
        except:
            return 0
    
    def calculate_ranking_dominance(self, results, platform):
        """Calculate ranking dominance score based on position in search results"""
        dominance_scores = defaultdict(float)
        
        for idx, result in enumerate(results):
            text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
            position = idx + 1  # 1-indexed position
            
            # Higher position = higher score (inverse relationship)
            # Top result gets 100, second gets 95, etc.
            position_score = max(0, 100 - (position - 1) * 5)
            
            # Check which brands are mentioned
            for brand in self.all_brands:
                pattern = r'\b' + re.escape(brand.lower()) + r'\b'
                if re.search(pattern, text):
                    dominance_scores[brand] += position_score
        
        # Normalize dominance scores
        total_dominance = sum(dominance_scores.values())
        dominance_percentages = {}
        
        if total_dominance > 0:
            for brand in self.all_brands:
                dominance_percentages[brand] = (dominance_scores[brand] / total_dominance) * 100
        else:
            for brand in self.all_brands:
                dominance_percentages[brand] = 0.0
        
        return {
            "raw_scores": dict(dominance_scores),
            "total_dominance": total_dominance,
            "percentages": dominance_percentages
        }
    
    def calculate_sov_metrics(self, mentions, engagement, sentiment, dominance=None):
        """
        Calculate comprehensive SoV metrics using the formula:
        SoV = (0.4 × Presence) + (0.3 × Engagement) + (0.2 × Sentiment) + (0.1 × Dominance)
        """
        presence_sov = mentions.get("percentages", {})
        engagement_sov = engagement.get("percentages", {})
        sentiment_sov = sentiment.get("positive_sov", {})
        dominance_sov = dominance.get("percentages", {}) if dominance else {}
        
        weighted_sov = {}
        
        for brand in self.all_brands:
            presence_pct = presence_sov.get(brand, 0)
            engagement_pct = engagement_sov.get(brand, 0)
            sentiment_pct = sentiment_sov.get(brand, 0)
            dominance_pct = dominance_sov.get(brand, 0) if dominance_sov else 0
            
            # Weighted SoV calculation as per implementation guide
            weighted_sov[brand] = (
                presence_pct * self.weights["presence_score"] +
                engagement_pct * self.weights["engagement_score"] +
                sentiment_pct * self.weights["sentiment_score"] +
                dominance_pct * self.weights["dominance_score"]
            )
        
        return {
            "presence_sov": presence_sov,
            "engagement_sov": engagement_sov,
            "sentiment_sov": sentiment_sov,
            "dominance_sov": dominance_sov if dominance_sov else {},
            "weighted_sov": weighted_sov,
            "formula_weights": self.weights
        }
    
    def calculate_overall_sov(self, platform_sov):
        """Calculate overall SoV across all platforms"""
        # Aggregate SoV from all platforms
        total_weighted_sov = defaultdict(float)
        platform_count = len(platform_sov)
        
        if platform_count == 0:
            return {}
        
        # Average SoV across platforms
        for platform, data in platform_sov.items():
            sov_metrics = data.get("sov_metrics", {})
            weighted_sov = sov_metrics.get("weighted_sov", {})
            
            for brand, value in weighted_sov.items():
                total_weighted_sov[brand] += value
        
        # Calculate average
        overall_sov = {
            brand: total_weighted_sov[brand] / platform_count
            for brand in self.all_brands
        }
        
        return {
            "sov_percentage": overall_sov,
            "platforms_analyzed": list(platform_sov.keys()),
            "platform_count": platform_count
        }

