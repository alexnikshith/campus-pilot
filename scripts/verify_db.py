#!/usr/bin/env python3
"""
Database connectivity verification script for PlacementPilot.
Checks if the configured PostgreSQL instance is accessible.
"""

import sys
import os

# Add backend directory to sys.path
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, backend_dir)

from app.db.session import check_db_connection
from app.core.config import settings

def main():
    print("=" * 60)
    print(" PlacementPilot - Database Connectivity Verifier")
    print("=" * 60)
    
    # Mask database URL credentials for security
    url = settings.DATABASE_URL
    if "@" in url:
        prefix = url.split("@")[0]
        schema_user = prefix.split(":")[0] + "://***:***@"
        masked_url = schema_user + url.split("@")[1]
    else:
        masked_url = url
        
    print(f"Target Database URL: {masked_url}")
    print("Checking connection...")
    
    ok, message = check_db_connection()
    if ok:
        print("[SUCCESS] PostgreSQL connection verified successfully!")
        print(f"Status: {message}")
        print("=" * 60)
        sys.exit(0)
    else:
        print("[ERROR] Could not connect to PostgreSQL instance.")
        print(f"Reason: {message}")
        print("\nTroubleshooting tips:")
        print("1. If using Docker: Ensure Docker Desktop is started and run `docker compose up -d postgres`.")
        print("2. If using local PostgreSQL: Ensure the Windows PostgreSQL service is running on port 5432.")
        print("3. Check credentials in your .env file matches the running PostgreSQL instance.")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
