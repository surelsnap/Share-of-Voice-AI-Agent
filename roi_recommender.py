"""
ROI-Focused Content Recommendation Engine
Predicts content ROI and helps prioritize marketing investments
"""
from typing import Dict, List
from collections import defaultdict
import math


class ROIRecommender:
    """Recommend content based on predicted ROI"""
    
    def __init__(self, config):
        self.config = config
        self.brand_name = config.BRAND_NAME
    
    def generate_roi_recommendations(self, platform_data: Dict, sov_data: Dict, gap_analysis: Dict) -> Dict:
        """Generate ROI-focused content recommendations"""
        return {
            "content_ideas": self._generate_content_ideas(gap_analysis),
            "roi_predictions": self._predict_content_roi(platform_data, gap_analysis),
            "resource_optimization": self._optimize_resources(gap_analysis),
            "platform_roi_comparison": self._compare_platform_roi(platform_data),
            "time_to_impact": self._forecast_time_to_impact(gap_analysis),
            "prioritized_recommendations": self._prioritize_by_roi(gap_analysis)
        }
    
    def _generate_content_ideas(self, gap_analysis: Dict) -> List[Dict]:
        """Generate content ideas based on gaps"""
        ideas = []
        
        # From topic gaps
        topic_gaps = gap_analysis.get("topic_coverage", {}).get("identified_gaps", [])
        for gap in topic_gaps[:5]:
            ideas.append({
                "idea": f"Create {gap.get('topic', '')} content",
                "type": "topic_coverage",
                "gap_size": gap.get("gap_size", 0),
                "estimated_effort": "medium",
                "potential_impact": "high" if gap.get("priority") == "high" else "medium"
            })
        
        # From format gaps
        format_gaps = gap_analysis.get("format_gaps", {}).get("format_gaps", [])
        for gap in format_gaps[:3]:
            ideas.append({
                "idea": f"Create {gap.get('format', '')} format content",
                "type": "format",
                "gap_size": gap.get("competitor_count", 0),
                "estimated_effort": "low" if gap.get("format") == "tutorial" else "medium",
                "potential_impact": "high" if gap.get("priority") == "high" else "medium"
            })
        
        # From keyword cluster gaps
        cluster_gaps = gap_analysis.get("keyword_cluster_gaps", {}).get("cluster_gaps", [])
        for gap in cluster_gaps[:3]:
            ideas.append({
                "idea": f"Target {gap.get('cluster', '')} keyword cluster",
                "type": "keyword_cluster",
                "gap_size": gap.get("gap", 0),
                "estimated_effort": "high",
                "potential_impact": "very_high" if gap.get("priority") == "high" else "high"
            })
        
        return ideas
    
    def _predict_content_roi(self, platform_data: Dict, gap_analysis: Dict) -> Dict:
        """Predict ROI for each content idea"""
        roi_predictions = []
        
        content_ideas = self._generate_content_ideas(gap_analysis)
        
        for idea in content_ideas:
            # Estimate views based on gap size and platform performance
            estimated_views = self._estimate_views(idea, platform_data)
            
            # Estimate engagement rate (based on format)
            engagement_rate = self._estimate_engagement_rate(idea.get("type", ""))
            
            # Estimate conversion potential
            conversion_rate = 0.02  # 2% average conversion from views to interest
            
            # Calculate ROI components
            estimated_engagement = estimated_views * engagement_rate
            estimated_conversions = estimated_views * conversion_rate
            
            # Cost estimation (based on effort)
            cost = self._estimate_cost(idea.get("estimated_effort", "medium"))
            
            # ROI calculation
            roi = (estimated_conversions * 100) / cost if cost > 0 else 0  # Simplified ROI
            
            roi_predictions.append({
                "content_idea": idea.get("idea", ""),
                "estimated_views": estimated_views,
                "estimated_engagement": round(estimated_engagement, 0),
                "estimated_conversions": round(estimated_conversions, 0),
                "estimated_cost": cost,
                "predicted_roi": round(roi, 2),
                "roi_category": "high" if roi > 5 else "medium" if roi > 2 else "low",
                "confidence": "medium"
            })
        
        return {
            "predictions": roi_predictions,
            "top_roi_opportunities": sorted(roi_predictions, key=lambda x: x["predicted_roi"], reverse=True)[:5]
        }
    
    def _estimate_views(self, idea: Dict, platform_data: Dict) -> int:
        """Estimate potential views for content idea"""
        base_views = 5000
        
        # Adjust based on gap size
        gap_size = idea.get("gap_size", 0)
        if gap_size > 10:
            base_views *= 2
        elif gap_size > 5:
            base_views *= 1.5
        
        # Adjust based on impact
        impact = idea.get("potential_impact", "medium")
        if impact == "very_high":
            base_views *= 2
        elif impact == "high":
            base_views *= 1.5
        
        # Add some randomness
        import random
        return int(base_views * random.uniform(0.8, 1.2))
    
    def _estimate_engagement_rate(self, content_type: str) -> float:
        """Estimate engagement rate based on content type"""
        rates = {
            "topic_coverage": 0.05,  # 5%
            "format": 0.08,  # 8% for format-specific content
            "keyword_cluster": 0.04  # 4% for keyword-focused
        }
        return rates.get(content_type, 0.05)
    
    def _estimate_cost(self, effort: str) -> int:
        """Estimate cost based on effort required"""
        costs = {
            "low": 500,    # Simple content
            "medium": 1500,  # Moderate complexity
            "high": 3000     # Complex content
        }
        return costs.get(effort, 1500)
    
    def _optimize_resources(self, gap_analysis: Dict) -> Dict:
        """Recommend content types based on available resources"""
        priority_gaps = gap_analysis.get("priority_scored_gaps", [])
        
        # Group by effort required
        low_effort = [g for g in priority_gaps if g.get("effort_required") == "low"]
        medium_effort = [g for g in priority_gaps if g.get("effort_required") == "medium"]
        high_effort = [g for g in priority_gaps if g.get("effort_required") == "high"]
        
        recommendations = {
            "limited_budget": {
                "recommendations": [g.get("recommendation", "") for g in low_effort[:3]],
                "expected_impact": "medium",
                "total_estimated_cost": len(low_effort[:3]) * 500
            },
            "moderate_budget": {
                "recommendations": [g.get("recommendation", "") for g in (low_effort[:2] + medium_effort[:3])],
                "expected_impact": "high",
                "total_estimated_cost": (len(low_effort[:2]) * 500) + (len(medium_effort[:3]) * 1500)
            },
            "high_budget": {
                "recommendations": [g.get("recommendation", "") for g in priority_gaps[:5]],
                "expected_impact": "very_high",
                "total_estimated_cost": sum(self._estimate_cost(g.get("effort_required", "medium")) for g in priority_gaps[:5])
            }
        }
        
        return recommendations
    
    def _compare_platform_roi(self, platform_data: Dict) -> Dict:
        """Compare ROI across different platforms"""
        platform_roi = {}
        
        for platform, results in platform_data.items():
            if not isinstance(results, list):
                continue
            
            # Calculate average engagement
            total_views = 0
            total_engagement = 0
            
            for result in results:
                views = result.get("views_count", 0) or 0
                likes = result.get("likes", 0) or 0
                comments = result.get("comment_count", 0) or 0
                
                total_views += views
                total_engagement += likes + comments
            
            avg_engagement_rate = (total_engagement / total_views * 100) if total_views > 0 else 0
            
            # Estimate content creation cost per platform
            platform_costs = {
                "youtube": 2000,  # Video production
                "google": 800,    # SEO content
                "instagram": 1200, # Visual content
                "twitter": 500     # Short-form content
            }
            
            cost = platform_costs.get(platform, 1000)
            
            # ROI score (engagement rate / cost * 1000)
            roi_score = (avg_engagement_rate / cost * 1000) if cost > 0 else 0
            
            platform_roi[platform] = {
                "average_engagement_rate": round(avg_engagement_rate, 2),
                "estimated_content_cost": cost,
                "roi_score": round(roi_score, 2),
                "recommendation": "high_priority" if roi_score > 2 else "medium_priority" if roi_score > 1 else "low_priority"
            }
        
        return platform_roi
    
    def _forecast_time_to_impact(self, gap_analysis: Dict) -> Dict:
        """Forecast how quickly different content will show results"""
        time_forecasts = {}
        
        priority_gaps = gap_analysis.get("priority_scored_gaps", [])
        
        for gap in priority_gaps[:5]:
            gap_type = gap.get("type", "")
            
            # Estimate time to impact based on type
            if gap_type == "format":
                time_weeks = 2  # Format content shows results quickly
            elif gap_type == "topic":
                time_weeks = 4  # Topic content takes moderate time
            else:  # keyword_cluster
                time_weeks = 8  # Keyword clusters take longer
            
            time_forecasts[gap.get("name", "")] = {
                "time_to_impact_weeks": time_weeks,
                "time_to_impact_category": "fast" if time_weeks <= 2 else "medium" if time_weeks <= 4 else "slow",
                "recommendation": gap.get("recommendation", "")
            }
        
        return time_forecasts
    
    def _prioritize_by_roi(self, gap_analysis: Dict) -> List[Dict]:
        """Prioritize recommendations by ROI"""
        roi_predictions = self._predict_content_roi({}, gap_analysis)
        
        prioritized = []
        
        for prediction in roi_predictions.get("predictions", []):
            content_idea = prediction.get("content_idea", "")
            roi = prediction.get("predicted_roi", 0)
            
            # Find corresponding gap
            priority_gaps = gap_analysis.get("priority_scored_gaps", [])
            matching_gap = next((g for g in priority_gaps if content_idea.lower() in g.get("recommendation", "").lower()), None)
            
            if matching_gap:
                prioritized.append({
                    "content_idea": content_idea,
                    "roi": roi,
                    "priority_score": matching_gap.get("priority_score", 0),
                    "combined_score": (roi * 0.6) + (matching_gap.get("priority_score", 0) * 0.4),
                    "recommendation": matching_gap.get("recommendation", ""),
                    "estimated_cost": prediction.get("estimated_cost", 0),
                    "estimated_views": prediction.get("estimated_views", 0)
                })
        
        # Sort by combined score
        prioritized.sort(key=lambda x: x.get("combined_score", 0), reverse=True)
        
        return prioritized[:10]  # Top 10 ROI opportunities

