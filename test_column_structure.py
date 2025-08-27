#!/usr/bin/env python3
"""
Test script to check the actual column structure returned by jugaad_data
"""

from jugaad_data import nse
import pandas as pd
from datetime import date

def test_column_structure():
    """Test the column structure of derivatives_df"""
    print("🔍 Testing jugaad_data column structure...")
    
    # Test with a recent date
    test_date = date(2024, 12, 26)
    expiry_date = date(2024, 12, 26)
    
    print(f"\n📅 Testing with date: {test_date}")
    print("=" * 50)
    
    try:
        # Test futures
        print("\n📊 Testing FUTIDX...")
        futures_data = nse.derivatives_df(
            symbol='NIFTY',
            from_date=test_date,
            to_date=test_date,
            expiry_date=expiry_date,
            instrument_type='FUTIDX'
        )
        
        if futures_data is not None and len(futures_data) > 0:
            print(f"✅ Futures data shape: {futures_data.shape}")
            print(f"📋 Futures columns: {list(futures_data.columns)}")
            print(f"📄 Sample data:")
            print(futures_data.head(2))
        else:
            print("❌ No futures data returned")
        
        # Test options
        print("\n📊 Testing OPTIDX...")
        options_data = nse.derivatives_df(
            symbol='NIFTY',
            from_date=test_date,
            to_date=test_date,
            expiry_date=expiry_date,
            instrument_type='OPTIDX',
            strike_price=21000,
            option_type='CE'
        )
        
        if options_data is not None and len(options_data) > 0:
            print(f"✅ Options data shape: {options_data.shape}")
            print(f"📋 Options columns: {list(options_data.columns)}")
            print(f"📄 Sample data:")
            print(options_data.head(2))
        else:
            print("❌ No options data returned")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_column_structure()
