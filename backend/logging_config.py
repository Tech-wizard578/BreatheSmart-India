# ==================== Logging Configuration ====================
# Save as: backend/logging_config.py

"""
Centralized logging configuration
"""

import logging
import logging.handlers
import os
from datetime import datetime
import json


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        
        return json.dumps(log_data)


def setup_logging(log_level=None, log_dir='logs'):
    """Setup application logging"""
    
    # Create logs directory
    os.makedirs(log_dir, exist_ok=True)
    
    # Get log level from environment or parameter
    if log_level is None:
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Console handler (colored for development)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (JSON for production)
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'airsense.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(file_handler)
    
    # Error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'errors.log'),
        maxBytes=10*1024*1024,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(error_handler)
    
    # Suppress noisy loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    
    logging.info(f"Logging initialized at {log_level} level")


# ==================== Performance Monitoring ====================
# Save as: backend/monitoring.py

"""
Performance monitoring and metrics collection
"""

import time
import psutil
import logging
from functools import wraps
from collections import defaultdict
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Track application performance metrics"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.start_time = time.time()
    
    def record_request(self, endpoint, duration, status_code):
        """Record API request metrics"""
        self.metrics['requests'].append({
            'endpoint': endpoint,
            'duration': duration,
            'status': status_code,
            'timestamp': datetime.now()
        })
    
    def record_prediction(self, city, duration, accuracy):
        """Record prediction metrics"""
        self.metrics['predictions'].append({
            'city': city,
            'duration': duration,
            'accuracy': accuracy,
            'timestamp': datetime.now()
        })
    
    def get_system_metrics(self):
        """Get current system metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'uptime_seconds': time.time() - self.start_time
        }
    
    def get_api_metrics(self, hours=1):
        """Get API performance metrics"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        recent_requests = [
            r for r in self.metrics['requests']
            if r['timestamp'] > cutoff
        ]
        
        if not recent_requests:
            return {
                'total_requests': 0,
                'avg_response_time': 0,
                'success_rate': 0
            }
        
        total = len(recent_requests)
        avg_time = sum(r['duration'] for r in recent_requests) / total
        successes = sum(1 for r in recent_requests if r['status'] < 400)
        
        return {
            'total_requests': total,
            'avg_response_time': round(avg_time, 3),
            'success_rate': round((successes / total) * 100, 2),
            'requests_per_minute': round(total / (hours * 60), 2)
        }
    
    def get_summary(self):
        """Get comprehensive metrics summary"""
        return {
            'system': self.get_system_metrics(),
            'api': self.get_api_metrics(),
            'timestamp': datetime.now().isoformat()
        }


# Global monitor instance
monitor = PerformanceMonitor()


def track_performance(func):
    """Decorator to track function performance"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start
            
            logger.info(f"{func.__name__} completed in {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start
            logger.error(f"{func.__name__} failed after {duration:.3f}s: {e}")
            raise
    return wrapper


# ==================== Health Check System ====================
# Save as: backend/health_check.py

"""
Comprehensive health check system
"""

import asyncio
from datetime import datetime
from typing import Dict, List
import aiohttp


class HealthChecker:
    """System health checker"""
    
    def __init__(self):
        self.checks = []
    
    async def check_database(self):
        """Check database connectivity"""
        try:
            from database import SessionLocal
            db = SessionLocal()
            db.execute("SELECT 1")
            db.close()
            return True, "Database is healthy"
        except Exception as e:
            return False, f"Database error: {str(e)}"
    
    async def check_external_apis(self):
        """Check external API availability"""
        checks = {}
        
        # Check CPCB API
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.data.gov.in",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    checks['cpcb'] = response.status < 500
        except:
            checks['cpcb'] = False
        
        # Check OpenWeather API
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.openweathermap.org",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    checks['openweather'] = response.status < 500
        except:
            checks['openweather'] = False
        
        all_healthy = all(checks.values())
        return all_healthy, checks
    
    async def check_ml_models(self):
        """Check ML model availability"""
        try:
            from ml_models import AQIPredictionModel
            model = AQIPredictionModel()
            has_model = model.lstm_model is not None
            return has_model, "ML models loaded" if has_model else "ML models not loaded"
        except Exception as e:
            return False, f"ML model error: {str(e)}"
    
    async def check_disk_space(self):
        """Check available disk space"""
        try:
            import psutil
            disk = psutil.disk_usage('/')
            percent_used = disk.percent
            
            if percent_used > 90:
                return False, f"Disk usage critical: {percent_used}%"
            elif percent_used > 80:
                return True, f"Disk usage warning: {percent_used}%"
            else:
                return True, f"Disk usage normal: {percent_used}%"
        except Exception as e:
            return False, f"Disk check error: {str(e)}"
    
    async def run_all_checks(self) -> Dict:
        """Run all health checks"""
        results = {}
        
        # Database check
        db_healthy, db_msg = await self.check_database()
        results['database'] = {'healthy': db_healthy, 'message': db_msg}
        
        # External APIs check
        api_healthy, api_checks = await self.check_external_apis()
        results['external_apis'] = {'healthy': api_healthy, 'checks': api_checks}
        
        # ML models check
        ml_healthy, ml_msg = await self.check_ml_models()
        results['ml_models'] = {'healthy': ml_healthy, 'message': ml_msg}
        
        # Disk space check
        disk_healthy, disk_msg = await self.check_disk_space()
        results['disk_space'] = {'healthy': disk_healthy, 'message': disk_msg}
        
        # Overall health
        overall_healthy = all(
            results[key]['healthy']
            for key in ['database', 'ml_models', 'disk_space']
        )
        
        return {
            'status': 'healthy' if overall_healthy else 'degraded',
            'timestamp': datetime.now().isoformat(),
            'checks': results
        }


# Global health checker
health_checker = HealthChecker()


# ==================== Rate Limiting ====================
# Save as: backend/rate_limiter.py

"""
Rate limiting middleware
"""

from fastapi import Request, HTTPException, status
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio


class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, requests_per_minute=60, requests_per_hour=1000):
        self.rpm_limit = requests_per_minute
        self.rph_limit = requests_per_hour
        
        self.minute_buckets = defaultdict(list)
        self.hour_buckets = defaultdict(list)
        
        # Start cleanup task
        asyncio.create_task(self._cleanup_task())
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier from request"""
        # Use X-Forwarded-For if behind proxy
        forwarded = request.headers.get('X-Forwarded-For')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.client.host
    
    def _cleanup_old_requests(self):
        """Remove old request records"""
        now = datetime.now()
        
        # Cleanup minute buckets (keep last 2 minutes)
        cutoff_minute = now - timedelta(minutes=2)
        for client_id in list(self.minute_buckets.keys()):
            self.minute_buckets[client_id] = [
                ts for ts in self.minute_buckets[client_id]
                if ts > cutoff_minute
            ]
            if not self.minute_buckets[client_id]:
                del self.minute_buckets[client_id]
        
        # Cleanup hour buckets (keep last 2 hours)
        cutoff_hour = now - timedelta(hours=2)
        for client_id in list(self.hour_buckets.keys()):
            self.hour_buckets[client_id] = [
                ts for ts in self.hour_buckets[client_id]
                if ts > cutoff_hour
            ]
            if not self.hour_buckets[client_id]:
                del self.hour_buckets[client_id]
    
    async def _cleanup_task(self):
        """Periodic cleanup task"""
        while True:
            await asyncio.sleep(60)  # Run every minute
            self._cleanup_old_requests()
    
    async def check_rate_limit(self, request: Request):
        """Check if request exceeds rate limits"""
        client_id = self._get_client_id(request)
        now = datetime.now()
        
        # Check minute limit
        minute_requests = [
            ts for ts in self.minute_buckets[client_id]
            if ts > now - timedelta(minutes=1)
        ]
        
        if len(minute_requests) >= self.rpm_limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {self.rpm_limit} requests per minute"
            )
        
        # Check hour limit
        hour_requests = [
            ts for ts in self.hour_buckets[client_id]
            if ts > now - timedelta(hours=1)
        ]
        
        if len(hour_requests) >= self.rph_limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {self.rph_limit} requests per hour"
            )
        
        # Add current request
        self.minute_buckets[client_id].append(now)
        self.hour_buckets[client_id].append(now)


# Global rate limiter
rate_limiter = RateLimiter()


# ==================== Caching System ====================
# Save as: backend/cache.py

"""
Simple in-memory caching system
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Optional
import json
import hashlib


class Cache:
    """In-memory cache with TTL support"""
    
    def __init__(self, default_ttl=3600):
        self.cache = {}
        self.default_ttl = default_ttl
        
        # Start cleanup task
        asyncio.create_task(self._cleanup_task())
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = json.dumps({
            'args': args,
            'kwargs': sorted(kwargs.items())
        }, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set cache value with TTL"""
        if ttl is None:
            ttl = self.default_ttl
        
        expiry = datetime.now() + timedelta(seconds=ttl)
        self.cache[key] = {
            'value': value,
            'expiry': expiry
        }
    
    def get(self, key: str) -> Optional[Any]:
        """Get cache value if not expired"""
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        if datetime.now() > entry['expiry']:
            del self.cache[key]
            return None
        
        return entry['value']
    
    def delete(self, key: str):
        """Delete cache entry"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
    
    async def _cleanup_task(self):
        """Periodic cleanup of expired entries"""
        while True:
            await asyncio.sleep(60)
            now = datetime.now()
            
            expired_keys = [
                key for key, entry in self.cache.items()
                if now > entry['expiry']
            ]
            
            for key in expired_keys:
                del self.cache[key]
    
    def cached(self, ttl: Optional[int] = None):
        """Decorator for caching function results"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                cache_key = self._generate_key(func.__name__, *args, **kwargs)
                
                # Check cache
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    return cached_value
                
                # Call function
                result = await func(*args, **kwargs)
                
                # Store in cache
                self.set(cache_key, result, ttl)
                
                return result
            return wrapper
        return decorator


# Global cache instance
cache = Cache()