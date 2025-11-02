import aiohttp
import asyncio
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
import json
from dotenv import load_dotenv

load_dotenv()

class CPCBDataFetcher:
    """Fetch air quality data from CPCB and other sources"""
    
    def __init__(self):
        self.cpcb_api_key = os.getenv("CPCB_API_KEY", "")
        self.base_url = "https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"
        self.cities_config = self._load_cities_config()
        
    def _load_cities_config(self):
        """Load city configurations"""
        return {
            'Delhi': {'lat': 28.7041, 'lng': 77.1025, 'population': 30000000},
            'Mumbai': {'lat': 19.0760, 'lng': 72.8777, 'population': 20000000},
            'Bangalore': {'lat': 12.9716, 'lng': 77.5946, 'population': 12000000},
            'Kolkata': {'lat': 22.5726, 'lng': 88.3639, 'population': 14500000},
            'Chennai': {'lat': 13.0827, 'lng': 80.2707, 'population': 10000000},
            'Hyderabad': {'lat': 17.3850, 'lng': 78.4867, 'population': 10000000},
            'Pune': {'lat': 18.5204, 'lng': 73.8567, 'population': 7000000},
            'Ahmedabad': {'lat': 23.0225, 'lng': 72.5714, 'population': 8000000},
            'Jaipur': {'lat': 26.9124, 'lng': 75.7873, 'population': 3500000},
            'Lucknow': {'lat': 26.8467, 'lng': 80.9462, 'population': 3200000}
        }
    
    async def fetch_realtime(self) -> List[Dict]:
        """Fetch real-time AQI data for all cities"""
        try:
            # In production, this would make actual API calls
            # For now, generating realistic mock data
            data = []
            for city, config in self.cities_config.items():
                # Generate realistic AQI based on city patterns
                base_aqi = self._get_city_base_aqi(city)
                time_factor = self._get_time_factor()
                seasonal_factor = self._get_seasonal_factor()
                
                aqi = int(base_aqi * time_factor * seasonal_factor + np.random.randint(-20, 20))
                aqi = max(50, min(450, aqi))  # Keep within realistic bounds
                
                reading = {
                    "city": city,
                    "aqi": aqi,
                    "pm25": int(aqi * 0.6 + np.random.randint(-10, 10)),
                    "pm10": int(aqi * 0.8 + np.random.randint(-15, 15)),
                    "no2": int(aqi * 0.15 + np.random.randint(-5, 5)),
                    "so2": int(aqi * 0.08 + np.random.randint(-3, 3)),
                    "co": round(aqi * 0.01 + np.random.uniform(-0.5, 0.5), 2),
                    "o3": int(aqi * 0.12 + np.random.randint(-5, 5)),
                    "timestamp": datetime.now().isoformat(),
                    "lat": config['lat'],
                    "lng": config['lng']
                }
                data.append(reading)
            
            return data
        except Exception as e:
            print(f"Error fetching real-time data: {e}")
            return []
    
    def _get_city_base_aqi(self, city: str) -> int:
        """Get base AQI for city (historical averages)"""
        city_averages = {
            'Delhi': 250, 'Mumbai': 180, 'Bangalore': 140,
            'Kolkata': 190, 'Chennai': 130, 'Hyderabad': 150,
            'Pune': 145, 'Ahmedabad': 165, 'Jaipur': 200, 'Lucknow': 220
        }
        return city_averages.get(city, 150)
    
    def _get_time_factor(self) -> float:
        """Get time-based pollution factor (traffic patterns)"""
        hour = datetime.now().hour
        if 7 <= hour <= 10 or 18 <= hour <= 21:
            return 1.3  # Peak traffic hours
        elif 11 <= hour <= 17:
            return 1.1  # Moderate traffic
        else:
            return 0.8  # Low traffic
    
    def _get_seasonal_factor(self) -> float:
        """Get seasonal pollution factor"""
        month = datetime.now().month
        if month in [11, 12, 1]:  # Winter
            return 1.5
        elif month in [2, 3]:  # Spring
            return 1.2
        elif month in [6, 7, 8]:  # Monsoon
            return 0.7
        else:
            return 1.0
    
    async def fetch_historical(self, city: str, days: int = 30) -> List[Dict]:
        """Fetch historical AQI data"""
        data = []
        base_aqi = self._get_city_base_aqi(city)
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            
            # Add realistic variation
            daily_variation = np.random.randint(-30, 30)
            trend = -0.5 * i  # Slight improving trend
            seasonal = 20 * np.sin(i * 0.2)  # Seasonal variation
            
            aqi = int(base_aqi + daily_variation + trend + seasonal)
            aqi = max(50, min(400, aqi))
            
            data.append({
                "date": date.isoformat(),
                "aqi": aqi,
                "pm25": int(aqi * 0.6),
                "pm10": int(aqi * 0.8),
                "no2": int(aqi * 0.15),
                "city": city
            })
        
        return sorted(data, key=lambda x: x['date'])
    
    async def fetch_current_aqi(self, city: str) -> float:
        """Fetch current AQI for a specific city"""
        realtime_data = await self.fetch_realtime()
        city_data = next((d for d in realtime_data if d['city'] == city), None)
        return city_data['aqi'] if city_data else 150.0


class WeatherDataFetcher:
    """Fetch weather data from OpenWeather API"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY", "")
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    async def fetch_current(self, cities: Optional[List[str]] = None) -> List[Dict]:
        """Fetch current weather data"""
        # Mock weather data
        weather_data = []
        city_configs = CPCBDataFetcher()._load_cities_config()
        
        for city, config in city_configs.items():
            if cities and city not in cities:
                continue
                
            weather_data.append({
                "city": city,
                "temp": np.random.randint(20, 35),
                "humidity": np.random.randint(40, 80),
                "wind_speed": np.random.randint(5, 20),
                "pressure": np.random.randint(1000, 1020),
                "conditions": np.random.choice(["Clear", "Cloudy", "Partly Cloudy", "Hazy"])
            })
        
        return weather_data
    
    async def fetch_forecast(self, city: str, hours: int = 48) -> List[Dict]:
        """Fetch weather forecast"""
        forecast = []
        
        for i in range(hours):
            hour_time = datetime.now() + timedelta(hours=i)
            
            forecast.append({
                "hour": i,
                "timestamp": hour_time.isoformat(),
                "temp": 20 + 10 * np.sin(i * np.pi / 12) + np.random.randint(-2, 2),
                "humidity": 50 + 20 * np.cos(i * np.pi / 12) + np.random.randint(-5, 5),
                "wind_speed": 10 + 5 * np.sin(i * np.pi / 24) + np.random.randint(-2, 2),
                "precipitation_prob": max(0, min(100, 30 + np.random.randint(-20, 20)))
            })
        
        return forecast


class NASADataFetcher:
    """Fetch satellite data from NASA EARTHDATA"""
    
    def __init__(self):
        self.api_key = os.getenv("NASA_API_KEY", "")
    
    async def fetch_satellite_data(self, lat: float, lng: float, date: str) -> Dict:
        """Fetch satellite air quality data"""
        # Mock satellite data
        return {
            "aerosol_optical_depth": round(np.random.uniform(0.1, 0.8), 3),
            "no2_column": round(np.random.uniform(1e15, 5e15), 2),
            "so2_column": round(np.random.uniform(0.1, 2.0), 2),
            "source": "NASA MODIS",
            "quality": "high"
        }