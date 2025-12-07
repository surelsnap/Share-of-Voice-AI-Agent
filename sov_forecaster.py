"""
Predictive SoV Forecasting Engine
Forecasts future Share of Voice trends 3-6 months ahead
"""
from typing import Dict, List
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict


class SoVForecaster:
    """Predict future SoV trends using time-series analysis"""
    
    def __init__(self, config):
        self.config = config
        self.brand_name = config.BRAND_NAME
        self.competitors = config.COMPETITOR_BRANDS
    
    def forecast_sov(self, historical_data: List[Dict], months_ahead: int = 3) -> Dict:
        """
        Forecast SoV for the next N months
        Uses linear regression and trend analysis
        """
        if not historical_data or len(historical_data) < 2:
            # If no historical data, use current data with trend estimation
            return self._estimate_from_current(historical_data, months_ahead)
        
        # Extract SoV values over time
        sov_timeline = self._extract_timeline(historical_data)
        
        forecasts = {}
        
        for brand in [self.brand_name] + self.competitors:
            if brand in sov_timeline:
                brand_data = sov_timeline[brand]
                forecast = self._predict_trend(brand_data, months_ahead)
                forecasts[brand] = forecast
        
        return {
            "forecast_period_months": months_ahead,
            "forecast_date": (datetime.now() + timedelta(days=months_ahead*30)).isoformat(),
            "brand_forecasts": forecasts,
            "confidence_intervals": self._calculate_confidence_intervals(forecasts)
        }
    
    def _extract_timeline(self, historical_data: List[Dict]) -> Dict:
        """Extract SoV values over time from historical data"""
        timeline = defaultdict(list)
        
        for data_point in historical_data:
            overall_sov = data_point.get("overall_sov", {})
            sov_percentage = overall_sov.get("sov_percentage", {})
            date = data_point.get("analysis_date", datetime.now().isoformat())
            
            for brand, sov_value in sov_percentage.items():
                timeline[brand].append({
                    "date": date,
                    "sov": sov_value
                })
        
        return dict(timeline)
    
    def _predict_trend(self, brand_data: List[Dict], months_ahead: int) -> Dict:
        """Predict future trend using linear regression"""
        if len(brand_data) < 2:
            return {"predicted_sov": brand_data[0]["sov"] if brand_data else 0, "trend": "stable"}
        
        # Extract values
        sov_values = [d["sov"] for d in brand_data]
        
        # Simple linear regression
        x = np.arange(len(sov_values))
        y = np.array(sov_values)
        
        # Calculate trend
        slope = np.polyfit(x, y, 1)[0]
        intercept = np.polyfit(x, y, 1)[1]
        
        # Predict future value
        future_x = len(sov_values) + months_ahead
        predicted_sov = slope * future_x + intercept
        
        # Determine trend direction
        if slope > 0.5:
            trend = "increasing"
        elif slope < -0.5:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "predicted_sov": max(0, predicted_sov),  # Ensure non-negative
            "current_sov": sov_values[-1],
            "trend": trend,
            "trend_strength": abs(slope),
            "change_expected": predicted_sov - sov_values[-1]
        }
    
    def _estimate_from_current(self, current_data: List[Dict], months_ahead: int) -> Dict:
        """Estimate forecast when no historical data available"""
        forecasts = {}
        
        if current_data:
            latest = current_data[-1]
            overall_sov = latest.get("overall_sov", {})
            sov_percentage = overall_sov.get("sov_percentage", {})
            
            for brand, sov_value in sov_percentage.items():
                # Estimate based on competitor activity patterns
                forecasts[brand] = {
                    "predicted_sov": sov_value,  # Assume stable
                    "current_sov": sov_value,
                    "trend": "stable",
                    "trend_strength": 0.0,
                    "change_expected": 0.0
                }
        
        return {
            "forecast_period_months": months_ahead,
            "forecast_date": (datetime.now() + timedelta(days=months_ahead*30)).isoformat(),
            "brand_forecasts": forecasts,
            "confidence_intervals": {}
        }
    
    def _calculate_confidence_intervals(self, forecasts: Dict) -> Dict:
        """Calculate confidence intervals for predictions"""
        intervals = {}
        
        for brand, forecast in forecasts.items():
            trend_strength = forecast.get("trend_strength", 0)
            predicted = forecast.get("predicted_sov", 0)
            
            # Higher uncertainty for stronger trends
            uncertainty = min(5, trend_strength * 2)
            
            intervals[brand] = {
                "lower_bound": max(0, predicted - uncertainty),
                "upper_bound": predicted + uncertainty,
                "confidence_level": "medium" if uncertainty < 3 else "low"
            }
        
        return intervals
    
    def predict_competitor_movements(self, historical_data: List[Dict], platform_data: Dict) -> Dict:
        """Predict which competitors will gain/lose SoV based on content velocity"""
        movements = {}
        
        # Analyze content velocity (frequency of new content)
        for competitor in self.competitors:
            # Estimate content velocity from platform data
            content_count = self._estimate_content_velocity(competitor, platform_data)
            
            # Higher content velocity = likely SoV increase
            if content_count > 10:
                movement = "gaining"
                expected_change = min(5, content_count * 0.3)
            elif content_count < 3:
                movement = "losing"
                expected_change = -max(2, 5 - content_count)
            else:
                movement = "stable"
                expected_change = 0
            
            movements[competitor] = {
                "expected_movement": movement,
                "expected_change": expected_change,
                "content_velocity": content_count,
                "reasoning": f"Based on {content_count} content pieces found"
            }
        
        return movements
    
    def _estimate_content_velocity(self, brand: str, platform_data: Dict) -> int:
        """Estimate content creation velocity"""
        count = 0
        
        for platform, results in platform_data.items():
            if isinstance(results, list):
                for result in results:
                    text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
                    if brand.lower() in text:
                        count += 1
        
        return count
    
    def model_seasonal_impact(self, current_month: int = None) -> Dict:
        """Model seasonal variations in fan demand"""
        if current_month is None:
            current_month = datetime.now().month
        
        # Summer months (April-June) typically have higher fan demand
        seasonal_multipliers = {
            1: 0.8,  # January - low
            2: 0.8,  # February - low
            3: 0.9,  # March - building
            4: 1.2,  # April - peak season starts
            5: 1.3,  # May - peak
            6: 1.3,  # June - peak
            7: 1.1,  # July - high
            8: 1.0,  # August - moderate
            9: 0.9,  # September - declining
            10: 0.9, # October - low
            11: 0.8, # November - low
            12: 0.8  # December - low
        }
        
        multiplier = seasonal_multipliers.get(current_month, 1.0)
        
        return {
            "current_month": current_month,
            "seasonal_multiplier": multiplier,
            "impact": "high" if multiplier > 1.1 else "low" if multiplier < 0.9 else "moderate",
            "recommendation": "Increase content during peak season months (April-June)" if multiplier > 1.1 else "Maintain baseline content"
        }
    
    def simulate_what_if_scenarios(self, base_sov: float, scenarios: List[Dict]) -> Dict:
        """Simulate impact of different marketing strategies"""
        results = {}
        
        for scenario in scenarios:
            scenario_name = scenario.get("name", "Unknown")
            action = scenario.get("action", "")
            expected_impact = scenario.get("expected_impact", 0)
            
            # Calculate projected SoV
            projected_sov = base_sov + expected_impact
            
            results[scenario_name] = {
                "action": action,
                "current_sov": base_sov,
                "projected_sov": projected_sov,
                "expected_change": expected_impact,
                "time_to_impact_weeks": scenario.get("time_to_impact", 4),
                "feasibility": scenario.get("feasibility", "medium")
            }
        
        return results

