#!/usr/bin/env python3
"""
Simple test script to verify nsepy functionality and handle NSE website issues.
"""

import requests
import ssl
from nsepy import get_history
from datetime import date
import pandas as pd

def test_nse_connection():
    """Test basic connection to NSE website"""
    print("Testing NSE website connection...")
    
    # Test basic HTTPS connection
    try:
        response = requests.get('https://www.nseindia.com', timeout=10)
        print(f"✅ NSE main site accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ NSE main site error: {e}")
    
    # Test with custom SSL context
    try:
        session = requests.Session()
        session.verify = False  # Disable SSL verification for testing
        response = session.get('https://www.nseindia.com', timeout=10)
        print(f"✅ NSE with custom SSL: {response.status_code}")
    except Exception as e:
        print(f"❌ NSE custom SSL error: {e}")

def test_nsepy_basic():
    """Test basic nsepy functionality"""
    print("\nTesting nsepy basic functionality...")
    
    try:
        # Try to get NIFTY index data for a recent date
        df = get_history(symbol="NIFTY 50", 
                        start=date(2025, 8, 1), 
                        end=date(2025, 8, 26),
                        index=True)
        
        if df is not None and not df.empty:
            print(f"✅ NIFTY data retrieved: {len(df)} rows")
            print(f"   Columns: {list(df.columns)}")
            print(f"   Date range: {df.index.min()} to {df.index.max()}")
        else:
            print("⚠️  NIFTY data returned empty")
            
    except Exception as e:
        print(f"❌ nsepy error: {e}")
        print("   This might be due to NSE website issues or rate limiting")

def test_options_data():
    """Test options data retrieval"""
    print("\nTesting options data retrieval...")
    
    try:
        # Try to get a simple options contract
        df = get_history(symbol="NIFTY",
                        start=date(2025, 8, 1),
                        end=date(2025, 8, 26),
                        option_type="CE",
                        strike_price=20000,
                        expiry_date=date(2025, 8, 28),
                        index=True)
        
        if df is not None and not df.empty:
            print(f"✅ Options data retrieved: {len(df)} rows")
            print(f"   Columns: {list(df.columns)}")
        else:
            print("⚠️  Options data returned empty")
            
    except Exception as e:
        print(f"❌ Options data error: {e}")

def main():
    print("🔍 NSE Data Access Test")
    print("=" * 50)
    
    test_nse_connection()
    test_nsepy_basic()
    test_options_data()
    
    print("\n" + "=" * 50)
    print("Test completed. Check results above.")

if __name__ == "__main__":
    main()
