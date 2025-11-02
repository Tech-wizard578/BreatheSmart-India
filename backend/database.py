"""
Database connection and ORM setup using SQLAlchemy
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:secure_password@localhost:5432/airsense"
)

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


# ORM Models
class AQIReading(Base):
    __tablename__ = "aqi_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False, index=True)
    aqi = Column(Float, nullable=False)
    pm25 = Column(Float)
    pm10 = Column(Float)
    no2 = Column(Float)
    so2 = Column(Float)
    co = Column(Float)
    o3 = Column(Float)
    lat = Column(Float)
    lng = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class CommunityReport(Base):
    __tablename__ = "community_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False, index=True)
    user_name = Column(String(100))
    location = Column(String(200), nullable=False)
    pollution_type = Column(String(50))
    description = Column(Text)
    image_url = Column(String(500))
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    verified = Column(Boolean, default=False, index=True)
    votes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class Policy(Base):
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_name = Column(String(200), nullable=False)
    description = Column(Text)
    implementation_date = Column(DateTime, nullable=False)
    expected_reduction = Column(Float)
    actual_reduction = Column(Float)
    status = Column(String(50), default='active', index=True)
    effectiveness_score = Column(Float)
    city = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)


class UserActivity(Base):
    __tablename__ = "user_activity"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False, index=True)
    action_type = Column(String(50))
    points_earned = Column(Integer, default=0)
    metadata = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False, index=True)
    prediction_time = Column(DateTime, nullable=False, index=True)
    predicted_aqi = Column(Float, nullable=False)
    actual_aqi = Column(Float)
    confidence = Column(Float)
    model_version = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


class AlertSetting(Base):
    __tablename__ = "alert_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False, index=True)
    city = Column(String(100), nullable=False)
    aqi_threshold = Column(Float, default=200)
    notification_enabled = Column(Boolean, default=True)
    notification_channels = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200))
    total_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    achievements = Column(Text)
    reports_submitted = Column(Integer, default=0)
    reports_verified = Column(Integer, default=0)
    joined_at = Column(DateTime, default=datetime.utcnow)


# Database utility functions
def get_db() -> Session:
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """Context manager for database session"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")


def drop_db():
    """Drop all database tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped")


# Database operations
class DatabaseOperations:
    """Utility class for common database operations"""
    
    @staticmethod
    def store_aqi_reading(db: Session, reading_data: dict):
        """Store AQI reading in database"""
        reading = AQIReading(**reading_data)
        db.add(reading)
        db.commit()
        db.refresh(reading)
        return reading
    
    @staticmethod
    def store_community_report(db: Session, report_data: dict):
        """Store community report in database"""
        report = CommunityReport(**report_data)
        db.add(report)
        db.commit()
        db.refresh(report)
        return report
    
    @staticmethod
    def get_city_readings(db: Session, city: str, limit: int = 100):
        """Get recent AQI readings for a city"""
        return db.query(AQIReading)\
            .filter(AQIReading.city == city)\
            .order_by(AQIReading.timestamp.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_verified_reports(db: Session, limit: int = 50):
        """Get verified community reports"""
        return db.query(CommunityReport)\
            .filter(CommunityReport.verified == True)\
            .order_by(CommunityReport.votes.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def update_report_votes(db: Session, report_id: int, increment: int = 1):
        """Update votes for a community report"""
        report = db.query(CommunityReport).filter(CommunityReport.id == report_id).first()
        if report:
            report.votes += increment
            db.commit()
            return report
        return None
    
    @staticmethod
    def get_user_activity(db: Session, user_id: str, limit: int = 50):
        """Get user activity history"""
        return db.query(UserActivity)\
            .filter(UserActivity.user_id == user_id)\
            .order_by(UserActivity.created_at.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def store_prediction(db: Session, prediction_data: dict):
        """Store prediction in database"""
        prediction = Prediction(**prediction_data)
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction
    
    @staticmethod
    def get_policies(db: Session, status: str = None):
        """Get policies, optionally filtered by status"""
        query = db.query(Policy)
        if status:
            query = query.filter(Policy.status == status)
        return query.order_by(Policy.implementation_date.desc()).all()
    
    @staticmethod
    def get_user_profile(db: Session, user_id: str):
        """Get or create user profile"""
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            profile = UserProfile(user_id=user_id, username=f"User_{user_id[:8]}")
            db.add(profile)
            db.commit()
            db.refresh(profile)
        return profile
    
    @staticmethod
    def update_user_points(db: Session, user_id: str, points: int):
        """Update user points and level"""
        profile = DatabaseOperations.get_user_profile(db, user_id)
        profile.total_points += points
        
        # Calculate level (100 points per level)
        profile.level = (profile.total_points // 100) + 1
        
        db.commit()
        db.refresh(profile)
        return profile


if __name__ == "__main__":
    # Initialize database
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")