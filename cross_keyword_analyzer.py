"""
Cross-Keyword Analysis Module
Analyzes patterns across multiple keywords to identify opportunities and gaps
"""
from typing import Dict, List
from collections import defaultdict


class CrossKeywordAnalyzer:
    """Analyze performance across multiple keywords"""
    
    def __init__(self, config):
        self.config = config
        self.brand_name = config.BRAND_NAME
        self.competitors = config.COMPETITOR_BRANDS
        self.all_brands = [self.brand_name] + self.competitors
    
    def analyze_keyword_performance(self, platform_data: Dict) -> Dict:
        """
        Analyze brand performance across different keywords
        Returns insights on keyword-level SoV distribution
        """
        keyword_performance = defaultdict(lambda: defaultdict(float))
        keyword_sov = defaultdict(dict)
        
        # Group results by keyword
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    keyword = result.get("keyword", "unknown")
                    # Extract brand mentions per keyword
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    
                    for brand in self.all_brands:
                        if brand.lower() in text:
                            keyword_performance[keyword][brand] += 1
        
        # Calculate SoV per keyword
        for keyword, brand_counts in keyword_performance.items():
            total = sum(brand_counts.values())
            if total > 0:
                for brand in self.all_brands:
                    keyword_sov[keyword][brand] = (brand_counts[brand] / total) * 100
        
        return {
            "keyword_performance": dict(keyword_performance),
            "keyword_sov": dict(keyword_sov)
        }
    
    def identify_content_gaps(self, keyword_analysis: Dict) -> List[Dict]:
        """
        Identify content gaps where competitors lead
        """
        gaps = []
        keyword_sov = keyword_analysis.get("keyword_sov", {})
        
        for keyword, brand_sovs in keyword_sov.items():
            brand_sov = brand_sovs.get(self.brand_name, 0)
            
            # Find top competitor for this keyword
            competitor_sovs = {
                comp: brand_sovs.get(comp, 0) 
                for comp in self.competitors
            }
            if competitor_sovs:
                top_competitor = max(competitor_sovs.items(), key=lambda x: x[1])
                competitor_sov = top_competitor[1]
                
                # If competitor leads significantly
                if competitor_sov > brand_sov + 10:  # 10% threshold
                    gaps.append({
                        "keyword": keyword,
                        "atomberg_sov": brand_sov,
                        "top_competitor": top_competitor[0],
                        "competitor_sov": competitor_sov,
                        "gap": competitor_sov - brand_sov,
                        "opportunity": "high" if competitor_sov - brand_sov > 20 else "medium"
                    })
        
        # Sort by gap size
        gaps.sort(key=lambda x: x["gap"], reverse=True)
        return gaps
    
    def analyze_keyword_associations(self, platform_data: Dict) -> Dict:
        """
        Analyze which keywords are most associated with each brand
        """
        brand_keyword_assoc = defaultdict(lambda: defaultdict(int))
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    keyword = result.get("keyword", "unknown")
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    
                    for brand in self.all_brands:
                        if brand.lower() in text:
                            brand_keyword_assoc[brand][keyword] += 1
        
        # Normalize associations
        normalized_assoc = {}
        for brand, keywords in brand_keyword_assoc.items():
            total = sum(keywords.values())
            if total > 0:
                normalized_assoc[brand] = {
                    kw: (count / total) * 100 
                    for kw, count in keywords.items()
                }
        
        return normalized_assoc
    
    def identify_opportunity_areas(self, keyword_analysis: Dict, gaps: List[Dict]) -> List[Dict]:
        """
        Identify specific opportunity areas for content creation
        """
        opportunities = []
        
        # Analyze keyword groups by intent
        technical_keywords = ["BLDC fan", "energy efficient fan"]
        commercial_keywords = ["smart fan", "smart ceiling fan", "WiFi fan"]
        
        technical_gaps = [g for g in gaps if g["keyword"] in technical_keywords]
        commercial_gaps = [g for g in gaps if g["keyword"] in commercial_keywords]
        
        if technical_gaps:
            avg_gap = sum(g["gap"] for g in technical_gaps) / len(technical_gaps)
            opportunities.append({
                "area": "Technical Content",
                "keywords": technical_keywords,
                "average_gap": avg_gap,
                "recommendation": "Create more technical content around BLDC technology and energy efficiency",
                "priority": "high" if avg_gap > 15 else "medium"
            })
        
        if commercial_gaps:
            avg_gap = sum(g["gap"] for g in commercial_gaps) / len(commercial_gaps)
            opportunities.append({
                "area": "Commercial/Product Content",
                "keywords": commercial_keywords,
                "average_gap": avg_gap,
                "recommendation": "Increase product-focused content showcasing smart features and WiFi connectivity",
                "priority": "high" if avg_gap > 15 else "medium"
            })
        
        return opportunities
    
    def generate_cross_keyword_insights(self, platform_data: Dict) -> Dict:
        """
        Generate comprehensive cross-keyword insights
        """
        keyword_analysis = self.analyze_keyword_performance(platform_data)
        gaps = self.identify_content_gaps(keyword_analysis)
        associations = self.analyze_keyword_associations(platform_data)
        opportunities = self.identify_opportunity_areas(keyword_analysis, gaps)
        
        return {
            "keyword_performance": keyword_analysis,
            "content_gaps": gaps,
            "brand_keyword_associations": associations,
            "opportunity_areas": opportunities,
            "summary": {
                "total_keywords_analyzed": len(keyword_analysis.get("keyword_sov", {})),
                "gaps_identified": len(gaps),
                "high_priority_opportunities": len([o for o in opportunities if o.get("priority") == "high"])
            }
        }

