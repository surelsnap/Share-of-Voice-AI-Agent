# SoV Analysis Agent - Main agent class
# This is the main orchestrator that runs everything
# I'm learning Gen AI so this might not be perfect but it works!

import json
import os
import time
from datetime import datetime
# from typing import Dict, List, Tuple  # commented out for now, might use later
import pandas as pd
from collections import defaultdict

from search_engines import GoogleSearcher, YouTubeSearcher
from sov_calculator import SoVCalculator
from sentiment_analyzer import SentimentAnalyzer
from insights_generator import InsightsGenerator
from cross_keyword_analyzer import CrossKeywordAnalyzer
from sov_forecaster import SoVForecaster
from content_gap_heatmap import ContentGapHeatmap
from viral_deconstructor import ViralContentDeconstructor
from realtime_alerts import RealtimeAlertSystem
from roi_recommender import ROIRecommender
from perception_gap_analyzer import PerceptionGapAnalyzer


class SoVAgent:
    # Main agent class - does all the work
    
    def __init__(self, config):
        self.config = config
        
        # store results in a dict
        self.results = {
            "brand": config.BRAND_NAME,
            "competitors": config.COMPETITOR_BRANDS,
            "keywords": config.SEARCH_KEYWORDS,
            "analysis_date": datetime.now().isoformat(),
            "platforms": {},
            "overall_sov": {},
            "insights": []
        }
        
        # initialize all the modules I created
        print("Loading modules...")
        self.google_searcher = GoogleSearcher(config)
        self.youtube_searcher = YouTubeSearcher(config)
        self.sov_calculator = SoVCalculator(config)
        self.sentiment_analyzer = SentimentAnalyzer()
        self.insights_generator = InsightsGenerator(config)
        self.cross_keyword_analyzer = CrossKeywordAnalyzer(config)
        
        # advanced features I added for extra points
        self.sov_forecaster = SoVForecaster(config)
        self.content_gap_heatmap = ContentGapHeatmap(config)
        self.viral_deconstructor = ViralContentDeconstructor(config)
        self.realtime_alerts = RealtimeAlertSystem(config)
        self.roi_recommender = ROIRecommender(config)
        self.perception_analyzer = PerceptionGapAnalyzer(config)
        
        # create folders if they don't exist
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        os.makedirs(config.VISUALIZATIONS_DIR, exist_ok=True)
    
    def search_platforms(self):
        """Search across all enabled platforms"""
        print("🔍 Starting search across platforms...")
        
        all_results = {}
        
        # Google Search
        if self.config.PLATFORMS.get("google", False):
            print("\n📊 Searching Google...")
            try:
                google_results = self.google_searcher.search_all_keywords()
                all_results["google"] = google_results
                print(f"✓ Found {len(google_results)} Google results")
            except Exception as e:
                print(f"✗ Google search failed: {e}")
                all_results["google"] = []
        
        # YouTube Search
        if self.config.PLATFORMS.get("youtube", False):
            print("\n📺 Searching YouTube...")
            try:
                youtube_results = self.youtube_searcher.search_all_keywords()
                all_results["youtube"] = youtube_results
                print(f"✓ Found {len(youtube_results)} YouTube results")
            except Exception as e:
                print(f"✗ YouTube search failed: {e}")
                all_results["youtube"] = []
        
        return all_results
    
    def analyze_sov(self, search_results):
        """Calculate Share of Voice metrics"""
        print("\n📈 Calculating Share of Voice metrics...")
        
        platform_sov = {}
        
        for platform, results in search_results.items():
            if not results:
                continue
                
            print(f"\n  Analyzing {platform}...")
            
            # Calculate mentions (Presence Score)
            mentions = self.sov_calculator.count_mentions(results, platform)
            
            # Calculate engagement (Engagement Score)
            engagement = self.sov_calculator.calculate_engagement(results, platform)
            
            # Analyze sentiment (Sentiment Score)
            sentiment = self.sentiment_analyzer.analyze_sentiment(results, platform)
            
            # Calculate ranking dominance (Dominance Score)
            dominance = self.sov_calculator.calculate_ranking_dominance(results, platform)
            
            # Calculate comprehensive SoV metrics
            sov_metrics = self.sov_calculator.calculate_sov_metrics(
                mentions, engagement, sentiment, dominance
            )
            
            platform_sov[platform] = {
                "mentions": mentions,
                "engagement": engagement,
                "sentiment": sentiment,
                "dominance": dominance,
                "sov_metrics": sov_metrics
            }
            
            print(f"  ✓ {platform} analysis complete")
        
        return platform_sov
    
    def generate_insights(self, sov_data, overall_sov=None, cross_keyword=None):
        """Generate insights and recommendations"""
        print("\n💡 Generating insights and recommendations...")
        
        insights = self.insights_generator.generate_insights(sov_data, overall_sov, cross_keyword)
        
        return insights
    
    def run(self):
        # main function that runs everything
        print("=" * 60)
        print("Atomberg SoV Analysis Agent")
        print("=" * 60)
        
        # check what mode we're in
        if self.config.PRODUCTION_MODE:
            print("\nMODE: PRODUCTION (Using API keys)")
            if self.config.YOUTUBE_API_KEY:
                print("   YouTube API: OK")
            if self.config.GOOGLE_API_KEY:
                print("   Google API: OK")
        else:
            print("\nMODE: DEMO (Using mock data)")
            print("   Note: Add API keys to .env for real data")
        print()
        
        # Step 1: Search platforms
        search_results = self.search_platforms()
        self.results["platforms"] = search_results
        
        # Step 2: Analyze SoV
        sov_data = self.analyze_sov(search_results)
        self.results["platform_sov"] = sov_data
        
        # Step 3: Calculate overall SoV
        overall_sov = self.sov_calculator.calculate_overall_sov(sov_data)
        self.results["overall_sov"] = overall_sov
        
        # Step 4: Cross-keyword analysis
        print("\n🔍 Performing cross-keyword analysis...")
        cross_keyword_insights = self.cross_keyword_analyzer.generate_cross_keyword_insights(search_results)
        self.results["cross_keyword_analysis"] = cross_keyword_insights
        
        # Step 5: Generate insights
        insights = self.generate_insights(sov_data, overall_sov, cross_keyword_insights)
        self.results["insights"] = insights
        
        # Step 6: Advanced AI Features
        print("\n🤖 Running Advanced AI Features...")
        
        # 6.1: Content Gap Heatmap
        print("\n  📊 Generating Content Gap Heatmap...")
        gap_heatmap = self.content_gap_heatmap.generate_heatmap(search_results, search_results)
        self.results["content_gap_heatmap"] = gap_heatmap
        print("  ✓ Content gap analysis complete")
        
        # 6.2: Viral Content Deconstruction
        print("\n  🔍 Deconstructing Viral Content...")
        viral_analysis = self.viral_deconstructor.deconstruct_viral_content(search_results)
        self.results["viral_content_analysis"] = viral_analysis
        print("  ✓ Viral content analysis complete")
        
        # 6.3: Real-Time Alerts
        print("\n  🚨 Generating Real-Time Alerts...")
        alerts = self.realtime_alerts.generate_alerts(search_results, sov_data, 
                                                      {p: d.get("sentiment", {}) for p, d in sov_data.items()})
        formatted_alerts = [self.realtime_alerts.format_alert_card(alert) for alert in alerts]
        self.results["realtime_alerts"] = formatted_alerts
        print(f"  ✓ Generated {len(formatted_alerts)} alerts")
        
        # 6.4: ROI Recommendations
        print("\n  💰 Calculating ROI Recommendations...")
        roi_recommendations = self.roi_recommender.generate_roi_recommendations(
            search_results, sov_data, gap_heatmap
        )
        self.results["roi_recommendations"] = roi_recommendations
        print("  ✓ ROI analysis complete")
        
        # 6.5: Brand Perception Gap Analysis
        print("\n  🎯 Analyzing Brand Perception Gaps...")
        perception_gaps = self.perception_analyzer.analyze_perception_gaps(
            search_results, {p: d.get("sentiment", {}) for p, d in sov_data.items()}
        )
        self.results["perception_gap_analysis"] = perception_gaps
        print("  ✓ Perception gap analysis complete")
        
        # 6.6: SoV Forecasting (requires historical data - using current as baseline)
        print("\n  📈 Forecasting Future SoV...")
        historical_data = [self.results]  # Use current as baseline
        sov_forecast = self.sov_forecaster.forecast_sov(historical_data, months_ahead=3)
        competitor_movements = self.sov_forecaster.predict_competitor_movements(historical_data, search_results)
        seasonal_impact = self.sov_forecaster.model_seasonal_impact()
        self.results["sov_forecast"] = {
            "forecast": sov_forecast,
            "competitor_movements": competitor_movements,
            "seasonal_impact": seasonal_impact
        }
        print("  ✓ SoV forecasting complete")
        
        # Step 7: Save results
        self.save_results()
        
        # Step 8: Generate visualizations
        self.generate_visualizations()
        
        print("\n" + "=" * 60)
        print("✅ Analysis Complete!")
        print("=" * 60)
        print(f"\n📁 Results saved to: {self.config.OUTPUT_DIR}/")
        
        return self.results
    
    def save_results(self):
        """Save analysis results to JSON"""
        output_file = self.config.RESULTS_FILE
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Results saved to {output_file}")
    
    def generate_visualizations(self):
        """Generate visualization charts"""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            # SoV Comparison Chart
            if "overall_sov" in self.results:
                sov_data = self.results["overall_sov"]
                brands = [self.config.BRAND_NAME] + self.config.COMPETITOR_BRANDS
                sov_values = [
                    sov_data.get("sov_percentage", {}).get(brand, 0) 
                    for brand in brands
                ]
                
                plt.figure(figsize=(12, 6))
                bars = plt.bar(brands, sov_values, color=['#FF6B6B' if b == self.config.BRAND_NAME else '#4ECDC4' for b in brands])
                plt.title('Share of Voice (SoV) Comparison', fontsize=16, fontweight='bold')
                plt.xlabel('Brand', fontsize=12)
                plt.ylabel('SoV Percentage (%)', fontsize=12)
                plt.xticks(rotation=45, ha='right')
                plt.grid(axis='y', alpha=0.3)
                
                # Add value labels on bars
                for bar, value in zip(bars, sov_values):
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2., height,
                            f'{value:.1f}%', ha='center', va='bottom')
                
                plt.tight_layout()
                plt.savefig(f"{self.config.VISUALIZATIONS_DIR}/sov_comparison.png", dpi=300)
                plt.close()
                print(f"  ✓ Generated SoV comparison chart")
            
        except Exception as e:
            print(f"  ⚠ Visualization generation failed: {e}")

