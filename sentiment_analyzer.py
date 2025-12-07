# Sentiment Analysis - checks if mentions are positive or negative
# Using VADER and TextBlob libraries

from collections import defaultdict
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    """Analyze sentiment of brand mentions"""
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
    
    def analyze_sentiment(self, results: List[Dict], platform: str) -> Dict:
        """Analyze sentiment for each brand including comments"""
        brand_sentiments = defaultdict(list)
        
        for result in results:
            # Combine title, snippet, and comments for analysis
            text = f"{result.get('title', '')} {result.get('snippet', '')}"
            
            # Add comments if available (especially for YouTube)
            comments = result.get("comments", [])
            if comments:
                comments_text = " ".join([str(c) for c in comments[:50]])  # Limit to 50 comments
                text += " " + comments_text
            
            # Analyze overall sentiment of the text
            vader_scores = self.vader.polarity_scores(text)
            textblob_sentiment = TextBlob(text).sentiment.polarity
            
            # Combined sentiment score (normalized to 0-1)
            combined_score = (vader_scores['compound'] + 1) / 2  # Normalize -1 to 1 -> 0 to 1
            
            # Check which brands are mentioned
            text_lower = text.lower()
            for brand in ["Atomberg", "Havells", "Crompton", "Orient", "Bajaj", "Usha", "Luminous"]:
                pattern = r'\b' + re.escape(brand.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    brand_sentiments[brand].append(combined_score)
        
        # Calculate sentiment statistics for each brand
        sentiment_stats = {}
        positive_sov = {}
        total_positive_mentions = 0
        
        for brand, scores in brand_sentiments.items():
            if scores:
                avg_sentiment = sum(scores) / len(scores)
                positive_count = sum(1 for s in scores if s > 0.6)  # Threshold for positive
                total_positive_mentions += positive_count
                
                sentiment_stats[brand] = {
                    "average_sentiment": avg_sentiment,
                    "positive_count": positive_count,
                    "total_mentions": len(scores),
                    "positive_ratio": positive_count / len(scores) if len(scores) > 0 else 0
                }
            else:
                sentiment_stats[brand] = {
                    "average_sentiment": 0.5,
                    "positive_count": 0,
                    "total_mentions": 0,
                    "positive_ratio": 0
                }
        
        # Calculate Share of Positive Voice
        if total_positive_mentions > 0:
            for brand in sentiment_stats.keys():
                positive_count = sentiment_stats[brand]["positive_count"]
                positive_sov[brand] = (positive_count / total_positive_mentions) * 100
        else:
            for brand in sentiment_stats.keys():
                positive_sov[brand] = 0.0
        
        return {
            "sentiment_stats": sentiment_stats,
            "positive_sov": positive_sov,
            "total_positive_mentions": total_positive_mentions
        }

