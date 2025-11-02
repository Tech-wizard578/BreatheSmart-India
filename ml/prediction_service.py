import asyncio
from typing import Dict, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.ml_models import AQIPredictionModel
from backend.data_fetcher import CPCBDataFetcher, WeatherDataFetcher

class PredictionService:
    """Service for managing AQI predictions"""
    
    def __init__(self):
        self.model = AQIPredictionModel(model_path='models/')
        self.cpcb_fetcher = CPCBDataFetcher()
        self.weather_fetcher = WeatherDataFetcher()
        self.cache = {}
        self.cache_duration = 3600  # 1 hour cache
    
    async def get_predictions(self, city: str, hours: int = 48) -> Dict:
        """Get AQI predictions for a city"""
        
        # Check cache
        cache_key = f"{city}_{hours}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if (asyncio.get_event_loop().time() - timestamp) < self.cache_duration:
                return cached_data
        
        # Fetch data
        historical_data = await self.cpcb_fetcher.fetch_historical(city, days=30)
        weather_forecast = await self.weather_fetcher.fetch_forecast(city, hours=hours)
        
        # Generate predictions
        predictions = await self.model.predict(
            historical_data=historical_data,
            weather_forecast=weather_forecast,
            hours=hours
        )
        
        result = {
            "city": city,
            "predictions": predictions,
            "model_accuracy": self.model.get_accuracy(),
            "confidence_interval": self.model.get_confidence_interval(),
            "generated_at": asyncio.get_event_loop().time()
        }
        
        # Update cache
        self.cache[cache_key] = (result, asyncio.get_event_loop().time())
        
        return result
    
    async def get_alerts(self, city: str, threshold: float = 200) -> List[Dict]:
        """Get pollution alerts for a city"""
        predictions = await self.get_predictions(city, hours=48)
        
        alerts = []
        for pred in predictions['predictions']:
            if pred['predicted_aqi'] > threshold:
                alerts.append({
                    "timestamp": pred['timestamp'],
                    "hour": pred['hour'],
                    "predicted_aqi": pred['predicted_aqi'],
                    "severity": "High" if pred['predicted_aqi'] > 300 else "Moderate",
                    "recommendation": self._get_recommendation(pred['predicted_aqi'])
                })
        
        return alerts
    
    def _get_recommendation(self, aqi: float) -> str:
        """Get health recommendation based on AQI"""
        if aqi > 300:
            return "Stay indoors. Avoid all outdoor activities. Use air purifiers."
        elif aqi > 200:
            return "Limit outdoor exposure. Wear N95 masks if you must go out."
        elif aqi > 150:
            return "Sensitive groups should reduce outdoor activities."
        else:
            return "Moderate air quality. Take usual precautions."
    
    async def batch_predict(self, cities: List[str], hours: int = 48) -> Dict[str, Dict]:
        """Get predictions for multiple cities"""
        tasks = [self.get_predictions(city, hours) for city in cities]
        results = await asyncio.gather(*tasks)
        
        return {result['city']: result for result in results}

# Example usage
async def main():
    service = PredictionService()
    
    # Get predictions for Delhi
    predictions = await service.get_predictions("Delhi", hours=48)
    print(f"Predictions for {predictions['city']}:")
    print(f"Model Accuracy: {predictions['model_accuracy']}%")
    print(f"\nFirst 5 predictions:")
    for pred in predictions['predictions'][:5]:
        print(f"Hour {pred['hour']}: {pred['predicted_aqi']} AQI (Confidence: {pred['confidence']}%)")
    
    # Get alerts
    alerts = await service.get_alerts("Delhi", threshold=200)
    print(f"\n{len(alerts)} alerts found")

if __name__ == "__main__":
    asyncio.run(main())