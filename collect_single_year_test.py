#!/usr/bin/env python3
"""
Test script to collect data for just one year (2024) to verify the approach
"""

from jugaad_data import nse
import pandas as pd
from datetime import date, timedelta
import os
import time

def get_monthly_expiries(year):
    """Get monthly expiry dates for a year (last Thursday of each month)"""
    expiries = []
    
    for month in range(1, 13):
        # Start from last day of month
        last_day = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
        
        # Find last Thursday
        while last_day.weekday() != 3:  # Thursday = 3
            last_day -= timedelta(days=1)
        
        expiries.append(last_day)
    
    return sorted(expiries)

def test_single_expiry(symbol, expiry_date):
    """Test collecting data for a single expiry date"""
    print(f"  📅 Testing {expiry_date}")
    
    try:
        # Test futures first
        print(f"    📊 Testing FUTIDX...")
        futures_data = nse.derivatives_df(
            symbol=symbol,
            from_date=expiry_date - timedelta(days=30),
            to_date=expiry_date,
            expiry_date=expiry_date,
            instrument_type='FUTIDX'
        )
        
        if futures_data is not None and len(futures_data) > 0:
            print(f"      ✅ Futures: {len(futures_data)} records")
            print(f"      📋 Columns: {list(futures_data.columns)}")
        else:
            print(f"      ❌ No futures data")
        
        # Test one option
        print(f"    📊 Testing OPTIDX...")
        options_data = nse.derivatives_df(
            symbol=symbol,
            from_date=expiry_date - timedelta(days=30),
            to_date=expiry_date,
            expiry_date=expiry_date,
            instrument_type='OPTIDX',
            strike_price=21000,
            option_type='CE'
        )
        
        if options_data is not None and len(options_data) > 0:
            print(f"      ✅ Options: {len(options_data)} records")
            print(f"      📋 Columns: {list(options_data.columns)}")
        else:
            print(f"      ❌ No options data")
            
        return True
        
    except Exception as e:
        print(f"      ❌ Error: {str(e)[:100]}...")
        return False

def main():
    """Test with 2024 data"""
    print("🧪 Testing Single Year Data Collection (2024)")
    print("=" * 60)
    
    year = 2024
    symbol = 'NIFTY'
    
    # Get monthly expiries
    expiry_dates = get_monthly_expiries(year)
    print(f"📅 Found {len(expiry_dates)} monthly expiry dates for {year}")
    
    # Test first 3 expiries only
    test_expiries = expiry_dates[:3]
    print(f"🧪 Testing first 3 expiries: {test_expiries}")
    
    successful = 0
    for expiry in test_expiries:
        if test_single_expiry(symbol, expiry):
            successful += 1
        time.sleep(1)  # Delay between tests
    
    print(f"\n📊 Test Results:")
    print(f"   Successful: {successful}/{len(test_expiries)}")
    
    if successful > 0:
        print(f"✅ Test passed! Ready to collect full year data.")
    else:
        print(f"❌ Test failed. Need to investigate further.")

if __name__ == "__main__":
    main()
