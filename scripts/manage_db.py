# ==================== Database Management Script ====================
# Save as: scripts/manage_db.py

"""
Database management utility script
Usage: python scripts/manage_db.py [command]
Commands: init, seed, reset, backup, migrate
"""

import sys
import os
from datetime import datetime
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db, drop_db, SessionLocal
from sqlalchemy import text


def init_database():
    """Initialize database tables"""
    print("Initializing database...")
    try:
        init_db()
        print("✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        return False


def seed_database():
    """Seed database with sample data"""
    print("Seeding database...")
    try:
        db = SessionLocal()
        
        # Read and execute seed file
        with open('database/seed_data.sql', 'r') as f:
            sql_commands = f.read()
        
        # Split by semicolon and execute each command
        for command in sql_commands.split(';'):
            if command.strip():
                db.execute(text(command))
        
        db.commit()
        db.close()
        print("✓ Database seeded successfully")
        return True
    except Exception as e:
        print(f"✗ Error seeding database: {e}")
        return False


def reset_database():
    """Reset database (drop and recreate)"""
    print("⚠ WARNING: This will delete all data!")
    confirm = input("Type 'yes' to confirm: ")
    
    if confirm.lower() != 'yes':
        print("Operation cancelled")
        return False
    
    print("Resetting database...")
    try:
        drop_db()
        init_db()
        print("✓ Database reset successfully")
        return True
    except Exception as e:
        print(f"✗ Error resetting database: {e}")
        return False


def backup_database():
    """Create database backup"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backups/airsense_backup_{timestamp}.sql"
    
    print(f"Creating backup: {backup_file}")
    
    try:
        os.makedirs('backups', exist_ok=True)
        
        # Use pg_dump for PostgreSQL
        db_url = os.getenv("DATABASE_URL", "postgresql://admin:secure_password@localhost:5432/airsense")
        
        # Parse connection string
        # Format: postgresql://user:pass@host:port/dbname
        parts = db_url.replace("postgresql://", "").split("@")
        user_pass = parts[0].split(":")
        host_port_db = parts[1].split("/")
        host_port = host_port_db[0].split(":")
        
        user = user_pass[0]
        password = user_pass[1]
        host = host_port[0]
        port = host_port[1] if len(host_port) > 1 else "5432"
        dbname = host_port_db[1]
        
        # Set password for pg_dump
        os.environ['PGPASSWORD'] = password
        
        cmd = f"pg_dump -h {host} -p {port} -U {user} {dbname} > {backup_file}"
        subprocess.run(cmd, shell=True, check=True)
        
        print(f"✓ Backup created: {backup_file}")
        return True
    except Exception as e:
        print(f"✗ Error creating backup: {e}")
        return False


def show_stats():
    """Show database statistics"""
    try:
        db = SessionLocal()
        
        from database import AQIReading, CommunityReport, UserProfile, Policy
        
        stats = {
            "AQI Readings": db.query(AQIReading).count(),
            "Community Reports": db.query(CommunityReport).count(),
            "User Profiles": db.query(UserProfile).count(),
            "Policies": db.query(Policy).count()
        }
        
        print("\n" + "="*40)
        print("DATABASE STATISTICS")
        print("="*40)
        for key, value in stats.items():
            print(f"{key:20s}: {value:>10,}")
        print("="*40 + "\n")
        
        db.close()
        return True
    except Exception as e:
        print(f"✗ Error fetching stats: {e}")
        return False


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python scripts/manage_db.py [command]")
        print("\nAvailable commands:")
        print("  init    - Initialize database tables")
        print("  seed    - Seed database with sample data")
        print("  reset   - Reset database (drop and recreate)")
        print("  backup  - Create database backup")
        print("  stats   - Show database statistics")
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        'init': init_database,
        'seed': seed_database,
        'reset': reset_database,
        'backup': backup_database,
        'stats': show_stats
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: init, seed, reset, backup, stats")


if __name__ == "__main__":
    main()


# ==================== API Testing Script ====================
# Save as: scripts/test_endpoints.py

"""
Quick API endpoint testing script
Usage: python scripts/test_endpoints.py
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


def test_endpoint(method, endpoint, data=None, params=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            return False, "Invalid method"
        
        status = "✓" if response.status_code < 400 else "✗"
        return True, {
            "status": status,
            "code": response.status_code,
            "time": response.elapsed.total_seconds()
        }
    except Exception as e:
        return False, str(e)


def run_tests():
    """Run all endpoint tests"""
    print("="*60)
    print(f"TESTING AIRSENSE INDIA API - {datetime.now()}")
    print("="*60 + "\n")
    
    tests = [
        ("GET", "/", None, None, "Root endpoint"),
        ("GET", "/health", None, None, "Health check"),
        ("GET", "/stats", None, None, "System statistics"),
        ("GET", "/api/v1/realtime", None, None, "Real-time data"),
        ("GET", "/api/v1/realtime", None, {"cities": "Delhi"}, "Real-time (filtered)"),
        ("POST", "/api/v1/predictions", {"city": "Delhi", "hours_ahead": 24}, None, "Predictions"),
        ("POST", "/api/v1/historical", {"city": "Mumbai", "days": 7}, None, "Historical data"),
        ("GET", "/api/v1/community/reports", None, {"limit": 10}, "Community reports"),
        ("GET", "/api/v1/policy/impact", None, None, "Policy impact"),
        ("GET", "/api/v1/source-attribution/Delhi", None, None, "Source attribution"),
        ("GET", "/api/v1/health-impact/Delhi", None, None, "Health impact"),
        ("GET", "/api/v1/leaderboard", None, {"limit": 5}, "Leaderboard"),
    ]
    
    passed = 0
    failed = 0
    
    for method, endpoint, data, params, description in tests:
        success, result = test_endpoint(method, endpoint, data, params)
        
        if success:
            print(f"{result['status']} {description:30s} | "
                  f"Status: {result['code']} | Time: {result['time']:.3f}s")
            if result['status'] == "✓":
                passed += 1
            else:
                failed += 1
        else:
            print(f"✗ {description:30s} | Error: {result}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_tests()








