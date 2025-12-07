"""
Content Gap Heatmap Generator
Identifies exactly where Atomberg is missing content opportunities
"""
from typing import Dict, List
from collections import defaultdict
import re


class ContentGapHeatmap:
    """Generate content gap heatmaps across topics, formats, and platforms"""
    
    def __init__(self, config):
        self.config = config
        self.brand_name = config.BRAND_NAME
        self.competitors = config.COMPETITOR_BRANDS
    
    def generate_heatmap(self, platform_data: Dict, search_results: Dict) -> Dict:
        """Generate comprehensive content gap heatmap"""
        return {
            "topic_coverage": self._analyze_topic_coverage(platform_data),
            "format_gaps": self._identify_format_gaps(platform_data),
            "platform_opportunities": self._analyze_platform_opportunities(platform_data),
            "keyword_cluster_gaps": self._find_keyword_cluster_gaps(search_results),
            "sentiment_white_spaces": self._identify_sentiment_white_spaces(platform_data),
            "priority_scored_gaps": self._score_gaps_by_priority(platform_data)
        }
    
    def _analyze_topic_coverage(self, platform_data: Dict) -> Dict:
        """Map topics discussed and identify where Atomberg has no content"""
        # Define topic categories
        topics = {
            "technical": ["BLDC", "motor", "energy efficiency", "wattage", "technology"],
            "features": ["smart", "WiFi", "app", "remote", "voice control", "IoT"],
            "comparison": ["vs", "compare", "better than", "difference", "review"],
            "installation": ["install", "setup", "mounting", "wiring", "DIY"],
            "maintenance": ["cleaning", "repair", "maintenance", "service"],
            "buying_guide": ["best", "top", "recommend", "buy", "price", "cost"]
        }
        
        brand_topics = defaultdict(int)
        competitor_topics = defaultdict(int)
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    
                    # Check which brand is mentioned
                    brand_mentioned = self.brand_name.lower() in text
                    competitor_mentioned = any(comp.lower() in text for comp in self.competitors)
                    
                    # Check which topics are covered
                    for topic_category, keywords in topics.items():
                        if any(kw in text for kw in keywords):
                            if brand_mentioned:
                                brand_topics[topic_category] += 1
                            if competitor_mentioned:
                                competitor_topics[topic_category] += 1
        
        # Identify gaps
        gaps = []
        for topic, comp_count in competitor_topics.items():
            brand_count = brand_topics.get(topic, 0)
            if comp_count > brand_count * 1.5:  # Competitors have 50% more content
                gaps.append({
                    "topic": topic,
                    "atomberg_coverage": brand_count,
                    "competitor_coverage": comp_count,
                    "gap_size": comp_count - brand_count,
                    "priority": "high" if comp_count > brand_count * 2 else "medium"
                })
        
        return {
            "brand_coverage": dict(brand_topics),
            "competitor_coverage": dict(competitor_topics),
            "identified_gaps": sorted(gaps, key=lambda x: x["gap_size"], reverse=True)
        }
    
    def _identify_format_gaps(self, platform_data: Dict) -> Dict:
        """Identify content format gaps"""
        formats = {
            "tutorial": ["how to", "tutorial", "guide", "step by step"],
            "review": ["review", "unboxing", "first impressions"],
            "comparison": ["vs", "comparison", "versus", "which is better"],
            "faq": ["FAQ", "questions", "answers", "common"],
            "testimonial": ["testimonial", "customer", "experience", "story"]
        }
        
        brand_formats = defaultdict(int)
        competitor_formats = defaultdict(int)
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    title = result.get("title", "").lower()
                    platform_type = result.get("platform", "")
                    
                    # Determine format
                    for format_type, keywords in formats.items():
                        if any(kw in title for kw in keywords):
                            text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                            
                            if self.brand_name.lower() in text:
                                brand_formats[format_type] += 1
                            elif any(comp.lower() in text for comp in self.competitors):
                                competitor_formats[format_type] += 1
        
        # Identify format gaps
        format_gaps = []
        for format_type, comp_count in competitor_formats.items():
            brand_count = brand_formats.get(format_type, 0)
            if comp_count > 0 and brand_count == 0:
                format_gaps.append({
                    "format": format_type,
                    "atomberg_count": 0,
                    "competitor_count": comp_count,
                    "gap": "complete_missing",
                    "priority": "high"
                })
            elif comp_count > brand_count * 1.5:
                format_gaps.append({
                    "format": format_type,
                    "atomberg_count": brand_count,
                    "competitor_count": comp_count,
                    "gap": "significant",
                    "priority": "medium"
                })
        
        return {
            "brand_formats": dict(brand_formats),
            "competitor_formats": dict(competitor_formats),
            "format_gaps": format_gaps
        }
    
    def _analyze_platform_opportunities(self, platform_data: Dict) -> Dict:
        """Identify platform-specific content needs"""
        platform_analysis = {}
        
        for platform, results in platform_data.items():
            if not isinstance(results, list):
                continue
            
            brand_count = sum(1 for r in results if self.brand_name.lower() in f"{r.get('title', '')} {r.get('snippet', '')}".lower())
            competitor_count = sum(1 for r in results if any(comp.lower() in f"{r.get('title', '')} {r.get('snippet', '')}".lower() for comp in self.competitors))
            
            total_results = len(results)
            brand_share = (brand_count / total_results * 100) if total_results > 0 else 0
            competitor_share = (competitor_count / total_results * 100) if total_results > 0 else 0
            
            opportunity_score = competitor_share - brand_share
            
            platform_analysis[platform] = {
                "brand_presence": brand_count,
                "competitor_presence": competitor_count,
                "brand_share": brand_share,
                "competitor_share": competitor_share,
                "opportunity_score": opportunity_score,
                "recommendation": self._get_platform_recommendation(platform, opportunity_score)
            }
        
        return platform_analysis
    
    def _get_platform_recommendation(self, platform: str, opportunity_score: float) -> str:
        """Get platform-specific recommendations"""
        if platform == "youtube":
            if opportunity_score > 20:
                return "Create more YouTube videos - focus on tutorials and product demos"
            elif opportunity_score > 10:
                return "Increase YouTube content frequency - consider series format"
            else:
                return "Maintain current YouTube strategy"
        elif platform == "google":
            if opportunity_score > 15:
                return "Improve SEO content - create blog posts and guides"
            else:
                return "Continue SEO optimization"
        else:
            return "Explore platform-specific content opportunities"
    
    def _find_keyword_cluster_gaps(self, search_results: Dict) -> Dict:
        """Find entire keyword clusters Atomberg isn't targeting"""
        # Group keywords by intent
        keyword_clusters = {
            "technical_specs": ["BLDC", "motor", "wattage", "RPM", "CFM"],
            "smart_features": ["smart", "WiFi", "app", "voice", "IoT", "Alexa", "Google Home"],
            "energy_efficiency": ["energy efficient", "power saving", "low power", "eco-friendly"],
            "installation": ["install", "mount", "ceiling", "wiring"],
            "price_range": ["budget", "affordable", "premium", "cost", "price"]
        }
        
        brand_clusters = defaultdict(int)
        competitor_clusters = defaultdict(int)
        
        for platform, results in search_results.items():
            if isinstance(results, list):
                for result in results:
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    keyword = result.get("keyword", "").lower()
                    
                    # Check which cluster this keyword belongs to
                    for cluster, keywords in keyword_clusters.items():
                        if any(kw in keyword or kw in text for kw in keywords):
                            if self.brand_name.lower() in text:
                                brand_clusters[cluster] += 1
                            elif any(comp.lower() in text for comp in self.competitors):
                                competitor_clusters[cluster] += 1
        
        # Identify cluster gaps
        cluster_gaps = []
        for cluster, comp_count in competitor_clusters.items():
            brand_count = brand_clusters.get(cluster, 0)
            if comp_count > brand_count * 1.5:
                cluster_gaps.append({
                    "cluster": cluster,
                    "atomberg_coverage": brand_count,
                    "competitor_coverage": comp_count,
                    "gap": comp_count - brand_count,
                    "priority": "high" if brand_count == 0 else "medium"
                })
        
        return {
            "brand_clusters": dict(brand_clusters),
            "competitor_clusters": dict(competitor_clusters),
            "cluster_gaps": sorted(cluster_gaps, key=lambda x: x["gap"], reverse=True)
        }
    
    def _identify_sentiment_white_spaces(self, platform_data: Dict) -> Dict:
        """Identify emotional/content angles competitors are using successfully"""
        sentiment_angles = {
            "problem_solving": ["problem", "issue", "solve", "fix", "help"],
            "aspirational": ["luxury", "premium", "upgrade", "modern", "stylish"],
            "practical": ["easy", "simple", "quick", "convenient"],
            "emotional": ["comfort", "peace", "relax", "enjoy", "love"],
            "technical_authority": ["expert", "professional", "engineered", "advanced"]
        }
        
        competitor_angles = defaultdict(int)
        brand_angles = defaultdict(int)
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    
                    for angle, keywords in sentiment_angles.items():
                        if any(kw in text for kw in keywords):
                            if self.brand_name.lower() in text:
                                brand_angles[angle] += 1
                            elif any(comp.lower() in text for comp in self.competitors):
                                competitor_angles[angle] += 1
        
        # Find white spaces
        white_spaces = []
        for angle, comp_count in competitor_angles.items():
            brand_count = brand_angles.get(angle, 0)
            if comp_count > brand_count * 2:
                white_spaces.append({
                    "angle": angle,
                    "atomberg_usage": brand_count,
                    "competitor_usage": comp_count,
                    "opportunity": f"Increase {angle} messaging in content"
                })
        
        return {
            "brand_angles": dict(brand_angles),
            "competitor_angles": dict(competitor_angles),
            "white_spaces": white_spaces
        }
    
    def _score_gaps_by_priority(self, platform_data: Dict) -> List[Dict]:
        """Score and rank gaps by potential impact and effort required"""
        all_gaps = []
        
        # Collect gaps from all analyses
        topic_gaps = self._analyze_topic_coverage(platform_data).get("identified_gaps", [])
        format_gaps = self._identify_format_gaps(platform_data).get("format_gaps", [])
        cluster_gaps = self._find_keyword_cluster_gaps(platform_data).get("cluster_gaps", [])
        
        # Score each gap
        for gap in topic_gaps:
            impact_score = gap.get("gap_size", 0) * 2
            effort_score = 3  # Medium effort for topic content
            priority_score = impact_score - effort_score
            
            all_gaps.append({
                "type": "topic",
                "name": gap.get("topic", ""),
                "impact_score": impact_score,
                "effort_required": "medium",
                "priority_score": priority_score,
                "recommendation": f"Create content covering {gap.get('topic', '')} topic"
            })
        
        for gap in format_gaps:
            impact_score = gap.get("competitor_count", 0) * 1.5
            effort_score = 2 if gap.get("format") == "tutorial" else 4
            priority_score = impact_score - effort_score
            
            all_gaps.append({
                "type": "format",
                "name": gap.get("format", ""),
                "impact_score": impact_score,
                "effort_required": "low" if effort_score < 3 else "medium",
                "priority_score": priority_score,
                "recommendation": f"Create {gap.get('format', '')} format content"
            })
        
        for gap in cluster_gaps:
            impact_score = gap.get("gap", 0) * 2.5
            effort_score = 4  # Higher effort for keyword clusters
            priority_score = impact_score - effort_score
            
            all_gaps.append({
                "type": "keyword_cluster",
                "name": gap.get("cluster", ""),
                "impact_score": impact_score,
                "effort_required": "high",
                "priority_score": priority_score,
                "recommendation": f"Target {gap.get('cluster', '')} keyword cluster"
            })
        
        # Sort by priority score
        all_gaps.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return all_gaps[:10]  # Top 10 priority gaps

