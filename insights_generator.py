"""
Insights Generator
Generates actionable insights and recommendations based on SoV analysis
"""
from typing import Dict, List
from collections import defaultdict


class InsightsGenerator:
    """Generate insights and recommendations"""
    
    def __init__(self, config):
        self.config = config
        self.brand_name = config.BRAND_NAME
    
    def generate_insights(self, sov_data: Dict, overall_sov: Dict = None, cross_keyword: Dict = None) -> List[Dict]:
        """Generate insights from SoV data with cross-keyword analysis"""
        insights = []
        
        # Analyze each platform
        for platform, data in sov_data.items():
            sov_metrics = data.get("sov_metrics", {})
            weighted_sov = sov_metrics.get("weighted_sov", {})
            
            brand_sov = weighted_sov.get(self.brand_name, 0)
            competitor_sov = max(
                weighted_sov.get(comp, 0) 
                for comp in self.config.COMPETITOR_BRANDS
            ) if self.config.COMPETITOR_BRANDS else 0
            
            # Insight 1: Platform performance
            if brand_sov > competitor_sov:
                insights.append({
                    "type": "strength",
                    "platform": platform,
                    "insight": f"Atomberg has a strong SoV on {platform} ({brand_sov:.1f}%) compared to competitors",
                    "recommendation": f"Continue current content strategy on {platform} and consider increasing investment"
                })
            else:
                insights.append({
                    "type": "opportunity",
                    "platform": platform,
                    "insight": f"Atomberg's SoV on {platform} ({brand_sov:.1f}%) is lower than top competitor ({competitor_sov:.1f}%)",
                    "recommendation": f"Increase content creation and engagement on {platform}. Focus on keyword optimization and influencer partnerships"
                })
        
        # Overall insights
        if overall_sov:
            brand_overall = overall_sov.get("sov_percentage", {}).get(self.brand_name, 0)
            
            insights.append({
                "type": "summary",
                "platform": "overall",
                "insight": f"Overall SoV: Atomberg has {brand_overall:.1f}% Share of Voice across all platforms",
                "recommendation": "Focus on platforms with highest engagement potential. Consider A/B testing content formats."
            })
        
        # Cross-keyword insights
        if cross_keyword:
            gaps = cross_keyword.get("content_gaps", [])
            opportunities = cross_keyword.get("opportunity_areas", [])
            
            if gaps:
                top_gaps = sorted(gaps, key=lambda x: x.get("gap", 0), reverse=True)[:3]
                for gap in top_gaps:
                    insights.append({
                        "type": "content_gap",
                        "platform": "all",
                        "insight": f"Content gap identified for '{gap['keyword']}': Atomberg has {gap['atomberg_sov']:.1f}% SoV vs {gap['top_competitor']}'s {gap['competitor_sov']:.1f}%",
                        "recommendation": f"Create targeted content for '{gap['keyword']}' to close the {gap['gap']:.1f}% gap. Focus on {gap['keyword']}-specific content with clear value propositions."
                    })
            
            if opportunities:
                for opp in opportunities:
                    insights.append({
                        "type": "opportunity_area",
                        "platform": "all",
                        "insight": f"{opp['area']} shows {opp['average_gap']:.1f}% average SoV gap",
                        "recommendation": opp.get("recommendation", ""),
                        "priority": opp.get("priority", "medium")
                    })
        
        # General keyword insights
        keywords_str = ", ".join(self.config.SEARCH_KEYWORDS)
        insights.append({
            "type": "keyword",
            "platform": "all",
            "insight": f"Keywords analyzed: {keywords_str}",
            "recommendation": "Expand keyword targeting to include: 'BLDC ceiling fan', 'energy saving fan', 'smart home fan'. Create content around these long-tail keywords."
        })
        
        # Sentiment insights
        for platform, data in sov_data.items():
            sentiment = data.get("sentiment", {})
            sentiment_stats = sentiment.get("sentiment_stats", {})
            brand_sentiment = sentiment_stats.get(self.brand_name, {})
            
            if brand_sentiment:
                positive_ratio = brand_sentiment.get("positive_ratio", 0)
                if positive_ratio > 0.7:
                    insights.append({
                        "type": "sentiment",
                        "platform": platform,
                        "insight": f"Strong positive sentiment on {platform} ({positive_ratio*100:.1f}% positive mentions)",
                        "recommendation": "Leverage positive sentiment by sharing user testimonials and reviews. Consider influencer partnerships."
                    })
                elif positive_ratio < 0.5:
                    insights.append({
                        "type": "sentiment",
                        "platform": platform,
                        "insight": f"Sentiment improvement needed on {platform} ({positive_ratio*100:.1f}% positive mentions)",
                        "recommendation": "Address common concerns in content. Engage with negative feedback proactively. Highlight unique value propositions."
                    })
        
        # Generate keyword strategy recommendations
        if cross_keyword:
            associations = cross_keyword.get("brand_keyword_associations", {})
            brand_assoc = associations.get(self.brand_name, {})
            
            if brand_assoc:
                top_keyword = max(brand_assoc.items(), key=lambda x: x[1])
                insights.append({
                    "type": "keyword_strategy",
                    "platform": "all",
                    "insight": f"Atomberg is most associated with '{top_keyword[0]}' ({top_keyword[1]:.1f}% of mentions)",
                    "recommendation": f"Leverage strength in '{top_keyword[0]}' while expanding presence in underperforming keywords. Consider creating content series around top-performing keywords."
                })
        
        return insights

