"""
Viral Content Deconstruction Engine
Reverse-engineers why competitor content goes viral and generates actionable "viral recipes"
"""
from typing import Dict, List
from collections import defaultdict
import re


class ViralContentDeconstructor:
    """Analyze viral content patterns and generate viral recipes"""
    
    def __init__(self, config):
        self.config = config
    
    def deconstruct_viral_content(self, platform_data: Dict, engagement_threshold: int = 100000) -> Dict:
        """Deconstruct viral content patterns"""
        viral_content = self._identify_viral_content(platform_data, engagement_threshold)
        
        return {
            "viral_content_analysis": viral_content,
            "hook_patterns": self._analyze_hook_patterns(viral_content),
            "emotional_triggers": self._detect_emotional_triggers(viral_content),
            "format_deconstruction": self._deconstruct_formats(viral_content),
            "audience_reaction_mapping": self._map_audience_reactions(viral_content),
            "viral_recipes": self._generate_viral_recipes(viral_content),
            "atomberg_content_scoring": self._score_atomberg_content(platform_data)
        }
    
    def _identify_viral_content(self, platform_data: Dict, threshold: int) -> List[Dict]:
        """Identify viral content based on engagement metrics"""
        viral_content = []
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    if platform == "youtube":
                        views = result.get("views_count", 0)
                        likes = result.get("likes", 0)
                        comments = result.get("comment_count", 0)
                        
                        # Calculate viral score
                        viral_score = views * 0.5 + likes * 100 + comments * 50
                        
                        if viral_score > threshold or views > threshold:
                            viral_content.append({
                                "platform": platform,
                                "title": result.get("title", ""),
                                "link": result.get("link", ""),
                                "views": views,
                                "likes": likes,
                                "comments": comments,
                                "viral_score": viral_score,
                                "snippet": result.get("snippet", ""),
                                "channel": result.get("channel", "")
                            })
        
        # Sort by viral score
        viral_content.sort(key=lambda x: x.get("viral_score", 0), reverse=True)
        return viral_content[:20]  # Top 20 viral pieces
    
    def _analyze_hook_patterns(self, viral_content: List[Dict]) -> Dict:
        """Identify successful opening patterns in first 5 seconds"""
        hook_patterns = defaultdict(int)
        
        for content in viral_content:
            title = content.get("title", "")
            
            # Analyze hook patterns
            if title.startswith(("How", "Why", "What", "When")):
                hook_patterns["question_hook"] += 1
            elif any(word in title.lower() for word in ["secret", "hidden", "amazing", "incredible"]):
                hook_patterns["curiosity_hook"] += 1
            elif any(word in title.lower() for word in ["best", "top", "ultimate", "complete"]):
                hook_patterns["authority_hook"] += 1
            elif "vs" in title.lower() or "comparison" in title.lower():
                hook_patterns["comparison_hook"] += 1
            elif any(word in title.lower() for word in ["review", "unboxing", "test"]):
                hook_patterns["review_hook"] += 1
            elif any(num in title for num in ["5", "10", "3", "7"]):
                hook_patterns["number_hook"] += 1
        
        # Get most common patterns
        top_patterns = sorted(hook_patterns.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "patterns": dict(hook_patterns),
            "top_patterns": [{"pattern": p[0], "frequency": p[1]} for p in top_patterns],
            "recommendation": self._generate_hook_recommendations(top_patterns)
        }
    
    def _generate_hook_recommendations(self, top_patterns: List) -> str:
        """Generate hook recommendations based on patterns"""
        if not top_patterns:
            return "Use question-based hooks to create curiosity"
        
        top_pattern = top_patterns[0][0]
        
        recommendations = {
            "question_hook": "Start with 'How' or 'Why' questions to immediately engage curiosity",
            "curiosity_hook": "Use words like 'secret', 'hidden', or 'amazing' to create intrigue",
            "authority_hook": "Position as 'best' or 'ultimate' guide to establish authority",
            "comparison_hook": "Use 'vs' or 'comparison' to tap into decision-making mindset",
            "review_hook": "Use 'review' or 'unboxing' for product-focused content",
            "number_hook": "Include specific numbers (5, 10, etc.) to promise structured content"
        }
        
        return recommendations.get(top_pattern, "Use engaging questions or curiosity-driven hooks")
    
    def _detect_emotional_triggers(self, viral_content: List[Dict]) -> Dict:
        """Map emotional journeys in viral videos"""
        emotional_stages = {
            "curiosity": ["wonder", "question", "mystery", "secret", "hidden"],
            "surprise": ["amazing", "incredible", "unexpected", "shocking", "wow"],
            "satisfaction": ["solution", "answer", "result", "success", "works"],
            "urgency": ["now", "today", "limited", "don't miss", "hurry"],
            "fear": ["avoid", "mistake", "warning", "danger", "problem"]
        }
        
        emotional_journey = defaultdict(int)
        
        for content in viral_content:
            text = f"{content.get('title', '')} {content.get('snippet', '')}".lower()
            
            for emotion, keywords in emotional_stages.items():
                if any(kw in text for kw in keywords):
                    emotional_journey[emotion] += 1
        
        # Identify most common journey
        sorted_emotions = sorted(emotional_journey.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "emotional_triggers": dict(emotional_journey),
            "recommended_journey": " → ".join([e[0] for e in sorted_emotions[:3]]) if sorted_emotions else "curiosity → surprise → satisfaction",
            "top_emotion": sorted_emotions[0][0] if sorted_emotions else "curiosity"
        }
    
    def _deconstruct_formats(self, viral_content: List[Dict]) -> Dict:
        """Analyze editing patterns, cuts, text overlays, and pacing"""
        format_analysis = {
            "video_length_patterns": defaultdict(int),
            "title_length": [],
            "common_words": defaultdict(int),
            "format_types": defaultdict(int)
        }
        
        for content in viral_content:
            title = content.get("title", "")
            
            # Title length
            format_analysis["title_length"].append(len(title))
            
            # Common words
            words = title.lower().split()
            for word in words:
                if len(word) > 3:  # Ignore short words
                    format_analysis["common_words"][word] += 1
            
            # Format detection
            if "review" in title.lower():
                format_analysis["format_types"]["review"] += 1
            if "tutorial" in title.lower() or "how to" in title.lower():
                format_analysis["format_types"]["tutorial"] += 1
            if "vs" in title.lower() or "comparison" in title.lower():
                format_analysis["format_types"]["comparison"] += 1
        
        # Calculate averages
        avg_title_length = sum(format_analysis["title_length"]) / len(format_analysis["title_length"]) if format_analysis["title_length"] else 0
        
        # Top common words
        top_words = sorted(format_analysis["common_words"].items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "average_title_length": round(avg_title_length, 1),
            "optimal_title_length": "40-60 characters",
            "top_words": [{"word": w[0], "frequency": w[1]} for w in top_words],
            "format_distribution": dict(format_analysis["format_types"]),
            "recommendations": {
                "title_length": f"Keep titles between 40-60 characters (current avg: {avg_title_length:.1f})",
                "format": f"Focus on {max(format_analysis['format_types'].items(), key=lambda x: x[1])[0] if format_analysis['format_types'] else 'review'} format for highest engagement",
                "keywords": f"Include these high-performing words: {', '.join([w[0] for w in top_words[:5]])}"
            }
        }
    
    def _map_audience_reactions(self, viral_content: List[Dict]) -> Dict:
        """Correlate specific content moments with comment sentiment spikes"""
        # This would ideally analyze comments, but for now we'll use engagement metrics
        reaction_patterns = {
            "high_engagement_content": [],
            "engagement_insights": {}
        }
        
        for content in viral_content:
            engagement_rate = 0
            if content.get("views", 0) > 0:
                engagement_rate = (content.get("likes", 0) + content.get("comments", 0)) / content.get("views", 1)
            
            if engagement_rate > 0.05:  # 5% engagement rate
                reaction_patterns["high_engagement_content"].append({
                    "title": content.get("title", ""),
                    "engagement_rate": engagement_rate,
                    "platform": content.get("platform", "")
                })
        
        # Identify patterns
        if reaction_patterns["high_engagement_content"]:
            avg_engagement = sum(c["engagement_rate"] for c in reaction_patterns["high_engagement_content"]) / len(reaction_patterns["high_engagement_content"])
            reaction_patterns["engagement_insights"] = {
                "average_engagement_rate": round(avg_engagement * 100, 2),
                "target_engagement_rate": "5%+",
                "insight": "Content with clear value propositions and comparisons show higher engagement"
            }
        
        return reaction_patterns
    
    def _generate_viral_recipes(self, viral_content: List[Dict]) -> List[Dict]:
        """Generate actionable viral recipes for Atomberg's content team"""
        recipes = []
        
        # Recipe 1: Question-based Hook
        recipes.append({
            "recipe_name": "Curiosity-Driven Question Hook",
            "structure": "Start with 'How' or 'Why' question → Present problem → Reveal solution → Show results",
            "example": "How to Choose the Best Smart Fan? (Complete Guide 2024)",
            "expected_engagement": "High",
            "effort": "Medium"
        })
        
        # Recipe 2: Comparison Format
        recipes.append({
            "recipe_name": "Comparison Format",
            "structure": "Brand A vs Brand B → Feature comparison → Pros/Cons → Winner",
            "example": "Atomberg vs Havells: Which Smart Fan is Better?",
            "expected_engagement": "Very High",
            "effort": "Medium"
        })
        
        # Recipe 3: Number-based List
        recipes.append({
            "recipe_name": "Numbered List Format",
            "structure": "Top N Reasons/Features → Detailed explanation → Call to action",
            "example": "5 Reasons Why Atomberg Fans Save More Energy",
            "expected_engagement": "High",
            "effort": "Low"
        })
        
        return recipes
    
    def _score_atomberg_content(self, platform_data: Dict) -> Dict:
        """Rate Atomberg's existing content for viral potential"""
        atomberg_content = []
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    if self.config.BRAND_NAME.lower() in text:
                        views = result.get("views_count", 0) or result.get("views", "0")
                        if isinstance(views, str):
                            views = int(views.replace(",", "").replace(" views", "")) if views.replace(",", "").replace(" views", "").isdigit() else 0
                        
                        atomberg_content.append({
                            "title": result.get("title", ""),
                            "views": views,
                            "platform": platform,
                            "viral_score": self._calculate_viral_potential(result)
                        })
        
        if not atomberg_content:
            return {
                "average_viral_score": 0,
                "recommendations": ["Create more content to analyze viral potential"]
            }
        
        avg_score = sum(c["viral_score"] for c in atomberg_content) / len(atomberg_content)
        
        return {
            "content_analyzed": len(atomberg_content),
            "average_viral_score": round(avg_score, 2),
            "top_performers": sorted(atomberg_content, key=lambda x: x["viral_score"], reverse=True)[:5],
            "improvement_suggestions": self._generate_improvement_suggestions(atomberg_content, avg_score)
        }
    
    def _calculate_viral_potential(self, content: Dict) -> float:
        """Calculate viral potential score (0-100)"""
        score = 0
        
        title = content.get("title", "")
        
        # Hook quality (0-30 points)
        if any(word in title.lower() for word in ["how", "why", "what", "best", "top"]):
            score += 20
        if "vs" in title.lower() or "comparison" in title.lower():
            score += 10
        
        # Title length (0-20 points)
        title_len = len(title)
        if 40 <= title_len <= 60:
            score += 20
        elif 30 <= title_len <= 70:
            score += 10
        
        # Engagement indicators (0-30 points)
        views = content.get("views_count", 0) or 0
        if views > 100000:
            score += 30
        elif views > 50000:
            score += 20
        elif views > 10000:
            score += 10
        
        # Format (0-20 points)
        if any(word in title.lower() for word in ["review", "tutorial", "guide"]):
            score += 20
        
        return min(100, score)
    
    def _generate_improvement_suggestions(self, content: List[Dict], avg_score: float) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        if avg_score < 50:
            suggestions.append("Improve hook quality - use question-based or curiosity-driven openings")
            suggestions.append("Optimize title length to 40-60 characters")
        
        if avg_score < 70:
            suggestions.append("Add comparison formats to increase engagement")
            suggestions.append("Include specific numbers or lists in titles")
        
        suggestions.append("Focus on formats that show highest engagement: reviews and tutorials")
        
        return suggestions

