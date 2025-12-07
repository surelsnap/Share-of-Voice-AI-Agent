"""
Brand Perception Gap Analyzer
Compares Atomberg's intended brand messaging with actual market perception
"""
from typing import Dict, List
from collections import defaultdict
import re


class PerceptionGapAnalyzer:
    """Analyze brand perception gaps"""
    
    def __init__(self, config):
        self.config = config
        self.brand_name = config.BRAND_NAME
        self.competitors = config.COMPETITOR_BRANDS
        
        # Intended brand messaging (Atomberg's advertised features)
        self.intended_messaging = {
            "energy_efficiency": ["energy efficient", "saves power", "low power", "BLDC", "wattage"],
            "smart_features": ["smart", "WiFi", "app", "voice control", "IoT", "connected"],
            "quiet_operation": ["quiet", "silent", "no noise", "peaceful"],
            "modern_design": ["modern", "sleek", "stylish", "contemporary", "design"],
            "value_proposition": ["affordable", "value", "cost-effective", "budget-friendly"]
        }
    
    def analyze_perception_gaps(self, platform_data: Dict, sentiment_data: Dict) -> Dict:
        """Comprehensive perception gap analysis"""
        return {
            "messaging_vs_reality": self._compare_messaging_reality(platform_data),
            "value_proposition_gaps": self._analyze_value_proposition_gaps(platform_data),
            "competitive_perception": self._map_competitive_perception(platform_data),
            "unexpected_associations": self._find_unexpected_associations(platform_data),
            "influencer_vs_customer_perception": self._compare_influencer_customer_perception(platform_data),
            "platform_specific_perception": self._analyze_platform_perception(platform_data),
            "alignment_recommendations": self._generate_alignment_recommendations(platform_data)
        }
    
    def _compare_messaging_reality(self, platform_data: Dict) -> Dict:
        """Compare advertised features with what customers actually discuss"""
        advertised_features = defaultdict(int)
        discussed_features = defaultdict(int)
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    
                    if self.brand_name.lower() in text:
                        # Check which intended features are mentioned
                        for feature, keywords in self.intended_messaging.items():
                            if any(kw in text for kw in keywords):
                                advertised_features[feature] += 1
                        
                        # Check what customers actually discuss
                        customer_keywords = ["quiet", "noise", "price", "cost", "quality", "durable", "reliable", "easy"]
                        for keyword in customer_keywords:
                            if keyword in text:
                                discussed_features[keyword] += 1
        
        # Identify gaps
        gaps = []
        for feature in self.intended_messaging.keys():
            advertised_count = advertised_features.get(feature, 0)
            # Check if customers discuss related terms
            discussed_count = 0
            for keyword in self.intended_messaging[feature]:
                discussed_count += discussed_features.get(keyword, 0)
            
            if advertised_count > 0 and discussed_count < advertised_count * 0.5:
                gaps.append({
                    "feature": feature,
                    "advertised_frequency": advertised_count,
                    "discussed_frequency": discussed_count,
                    "gap": "customers_not_discussing",
                    "insight": f"Atomberg advertises {feature} but customers don't discuss it much"
                })
        
        return {
            "advertised_features": dict(advertised_features),
            "discussed_features": dict(discussed_features),
            "gaps": gaps
        }
    
    def _analyze_value_proposition_gaps(self, platform_data: Dict) -> Dict:
        """Identify which promised benefits resonate vs which are ignored"""
        value_props = {
            "energy_savings": 0,
            "smart_technology": 0,
            "quiet_operation": 0,
            "modern_design": 0,
            "affordability": 0
        }
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    
                    if self.brand_name.lower() in text:
                        # Check which value props are mentioned
                        if any(kw in text for kw in ["energy", "save", "power", "efficient"]):
                            value_props["energy_savings"] += 1
                        if any(kw in text for kw in ["smart", "WiFi", "app", "connected"]):
                            value_props["smart_technology"] += 1
                        if any(kw in text for kw in ["quiet", "silent", "noise"]):
                            value_props["quiet_operation"] += 1
                        if any(kw in text for kw in ["modern", "sleek", "design", "stylish"]):
                            value_props["modern_design"] += 1
                        if any(kw in text for kw in ["affordable", "value", "price", "cost"]):
                            value_props["affordability"] += 1
        
        # Identify resonating vs ignored
        total_mentions = sum(value_props.values())
        
        resonating = []
        ignored = []
        
        for prop, count in value_props.items():
            percentage = (count / total_mentions * 100) if total_mentions > 0 else 0
            if percentage > 20:
                resonating.append({"value_prop": prop, "mention_percentage": round(percentage, 1)})
            elif percentage < 5:
                ignored.append({"value_prop": prop, "mention_percentage": round(percentage, 1)})
        
        return {
            "value_proposition_mentions": value_props,
            "resonating_props": resonating,
            "ignored_props": ignored,
            "insight": "Focus messaging on resonating value propositions"
        }
    
    def _map_competitive_perception(self, platform_data: Dict) -> Dict:
        """Show how customers perceive Atomberg vs competitors on key attributes"""
        attributes = {
            "quality": ["quality", "durable", "reliable", "build"],
            "price": ["price", "cost", "affordable", "expensive", "value"],
            "features": ["features", "smart", "technology", "advanced"],
            "design": ["design", "looks", "appearance", "stylish"],
            "performance": ["performance", "power", "airflow", "cooling"]
        }
        
        brand_perception = defaultdict(lambda: defaultdict(int))
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    
                    # Check which attributes are mentioned
                    for attr, keywords in attributes.items():
                        if any(kw in text for kw in keywords):
                            # Check sentiment context
                            if self.brand_name.lower() in text:
                                # Determine if positive or negative
                                positive_indicators = ["good", "great", "excellent", "best", "love", "amazing"]
                                negative_indicators = ["bad", "poor", "worst", "hate", "terrible"]
                                
                                if any(ind in text for ind in positive_indicators):
                                    brand_perception[self.brand_name][attr] += 1
                                elif any(ind in text for ind in negative_indicators):
                                    brand_perception[self.brand_name][f"{attr}_negative"] += 1
                                else:
                                    brand_perception[self.brand_name][attr] += 0.5
                            
                            # Check competitors
                            for competitor in self.competitors:
                                if competitor.lower() in text:
                                    positive_indicators = ["good", "great", "excellent", "best", "love", "amazing"]
                                    if any(ind in text for ind in positive_indicators):
                                        brand_perception[competitor][attr] += 1
        
        # Create comparison
        comparison = {}
        for attr in attributes.keys():
            brand_score = brand_perception[self.brand_name].get(attr, 0)
            competitor_scores = {comp: brand_perception[comp].get(attr, 0) for comp in self.competitors}
            top_competitor = max(competitor_scores.items(), key=lambda x: x[1]) if competitor_scores else ("N/A", 0)
            
            comparison[attr] = {
                "atomberg_score": brand_score,
                "top_competitor": top_competitor[0],
                "competitor_score": top_competitor[1],
                "perception_gap": brand_score - top_competitor[1],
                "status": "leading" if brand_score > top_competitor[1] else "trailing"
            }
        
        return comparison
    
    def _find_unexpected_associations(self, platform_data: Dict) -> Dict:
        """Find unplanned brand associations"""
        unexpected = []
        
        # Common unexpected associations
        unexpected_patterns = {
            "quiet": ["quiet", "silent", "no noise"],
            "premium": ["premium", "luxury", "high-end"],
            "budget": ["budget", "cheap", "affordable"],
            "reliable": ["reliable", "durable", "long-lasting"]
        }
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    
                    if self.brand_name.lower() in text:
                        for association, keywords in unexpected_patterns.items():
                            if any(kw in text for kw in keywords):
                                # Check if this is in intended messaging
                                is_intended = False
                                for feature, feature_keywords in self.intended_messaging.items():
                                    if any(kw in feature_keywords for kw in keywords):
                                        is_intended = True
                                        break
                                
                                if not is_intended:
                                    unexpected.append({
                                        "association": association,
                                        "context": text[:200],
                                        "platform": platform,
                                        "insight": f"Customers associate Atomberg with '{association}' even if not heavily advertised"
                                    })
        
        return {
            "unexpected_associations": unexpected[:10],  # Top 10
            "insight": "Leverage positive unexpected associations in messaging"
        }
    
    def _compare_influencer_customer_perception(self, platform_data: Dict) -> Dict:
        """Compare how influencers vs regular customers perceive the brand"""
        influencer_keywords = ["review", "unboxing", "sponsored", "influencer", "channel"]
        customer_keywords = ["customer", "user", "experience", "bought", "purchased"]
        
        influencer_perception = defaultdict(int)
        customer_perception = defaultdict(int)
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    
                    if self.brand_name.lower() in text:
                        is_influencer = any(kw in text for kw in influencer_keywords) or result.get("views_count", 0) > 50000
                        is_customer = any(kw in text for kw in customer_keywords)
                        
                        # Extract sentiment
                        positive_words = ["good", "great", "excellent", "love", "amazing", "best"]
                        negative_words = ["bad", "poor", "worst", "hate", "terrible"]
                        
                        if any(pw in text for pw in positive_words):
                            if is_influencer:
                                influencer_perception["positive"] += 1
                            elif is_customer:
                                customer_perception["positive"] += 1
                        elif any(nw in text for nw in negative_words):
                            if is_influencer:
                                influencer_perception["negative"] += 1
                            elif is_customer:
                                customer_perception["negative"] += 1
        
        return {
            "influencer_perception": dict(influencer_perception),
            "customer_perception": dict(customer_perception),
            "gap_analysis": {
                "influencer_positive_ratio": influencer_perception.get("positive", 0) / max(1, sum(influencer_perception.values())),
                "customer_positive_ratio": customer_perception.get("positive", 0) / max(1, sum(customer_perception.values())),
                "insight": "Compare influencer vs customer sentiment to identify messaging gaps"
            }
        }
    
    def _analyze_platform_perception(self, platform_data: Dict) -> Dict:
        """Show how brand perception differs across platforms"""
        platform_perceptions = {}
        
        for platform, results in platform_data.items():
            if not isinstance(results, list):
                continue
            
            perception_keywords = {
                "positive": ["good", "great", "excellent", "love", "amazing", "best", "recommend"],
                "negative": ["bad", "poor", "worst", "hate", "terrible", "avoid"],
                "technical": ["BLDC", "motor", "wattage", "technology", "specs"],
                "emotional": ["comfort", "peace", "relax", "enjoy", "satisfied"]
            }
            
            platform_counts = defaultdict(int)
            
            for result in results:
                text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                if self.brand_name.lower() in text:
                    for category, keywords in perception_keywords.items():
                        if any(kw in text for kw in keywords):
                            platform_counts[category] += 1
            
            platform_perceptions[platform] = {
                "perception_categories": dict(platform_counts),
                "dominant_perception": max(platform_counts.items(), key=lambda x: x[1])[0] if platform_counts else "neutral",
                "insight": f"Platform-specific perception: {max(platform_counts.items(), key=lambda x: x[1])[0] if platform_counts else 'neutral'}"
            }
        
        return platform_perceptions
    
    def _generate_alignment_recommendations(self, platform_data: Dict) -> List[Dict]:
        """Generate recommendations to align messaging with perception"""
        recommendations = []
        
        # Analyze gaps
        messaging_gaps = self._compare_messaging_reality(platform_data)
        value_prop_gaps = self._analyze_value_proposition_gaps(platform_data)
        
        # Recommendation 1: Focus on resonating value props
        resonating = value_prop_gaps.get("resonating_props", [])
        if resonating:
            recommendations.append({
                "priority": "high",
                "recommendation": f"Amplify messaging around {', '.join([r['value_prop'] for r in resonating[:2]])} as these resonate with customers",
                "rationale": "Customers already discuss these, so messaging will have higher impact"
            })
        
        # Recommendation 2: Address ignored value props
        ignored = value_prop_gaps.get("ignored_props", [])
        if ignored:
            recommendations.append({
                "priority": "medium",
                "recommendation": f"Re-evaluate messaging for {', '.join([i['value_prop'] for i in ignored])} - customers aren't discussing these",
                "rationale": "Either messaging isn't reaching customers or value prop needs repositioning"
            })
        
        # Recommendation 3: Leverage unexpected associations
        unexpected = self._find_unexpected_associations(platform_data)
        if unexpected.get("unexpected_associations"):
            top_association = unexpected["unexpected_associations"][0].get("association", "")
            recommendations.append({
                "priority": "medium",
                "recommendation": f"Leverage unexpected positive association: '{top_association}' - incorporate into messaging",
                "rationale": "Customers already associate this with Atomberg, capitalize on it"
            })
        
        return recommendations

