#!/usr/bin/env python3
"""
Test nsepython for historical options data access
Alternative approach to get historical NSE options data
"""

import nsepython as nse
import pandas as pd
from datetime import datetime, date, timedelta
import time

def test_nsepython_basic():
    """Test basic nsepython functionality"""
    print("🔍 Testing nsepython for NSE Options Data...")
    print("=" * 60)
    
    try:
        # Test 1: Get current NIFTY options chain
        print("1. Testing NIFTY options chain...")
        nifty_options = nse.nse_optionchain_scrapper('NIFTY')
        print(f"   ✅ NIFTY options data retrieved")
        print(f"   Records: {len(nifty_options) if isinstance(nifty_options, list) else 'N/A'}")
        
        # Test 2: Get current BANKNIFTY options chain
        print("\n2. Testing BANKNIFTY options chain...")
        banknifty_options = nse.nse_optionchain_scrapper('BANKNIFTY')
        print(f"   ✅ BANKNIFTY options data retrieved")
        print(f"   Records: {len(banknifty_options) if isinstance(banknifty_options, list) else 'N/A'}")
        
        # Test 3: Get historical NIFTY data
        print("\n3. Testing historical NIFTY data...")
        nifty_hist = nse.get_history(symbol='NIFTY', start=date(2024, 1, 1), end=date(2024, 12, 31))
        print(f"   ✅ Historical NIFTY data retrieved")
        print(f"   Records: {len(nifty_hist) if nifty_hist is not None else 'N/A'}")
        
        return True
        
    except Exception as e:
        print(f"❌ nsepython error: {e}")
        return False

def test_options_data_structure():
    """Test the structure of options data"""
    print("\n📊 Testing Options Data Structure...")
    print("=" * 60)
    
    try:
        # Get NIFTY options
        nifty_options = nse.nse_optionchain_scrapper('NIFTY')
        
        if nifty_options and 'records' in nifty_options:
            records = nifty_options['records']
            if 'data' in records:
                data = records['data']
                
                print("Available data keys:")
                for key in data.keys():
                    print(f"   - {key}")
                
                if 'CE' in data and 'PE' in data:
                    ce_data = data['CE']
                    pe_data = data['PE']
                    
                    print(f"\nCall Options (CE): {len(ce_data) if ce_data else 0} contracts")
                    print(f"Put Options (PE): {len(pe_data) if pe_data else 0} contracts")
                    
                    if ce_data and len(ce_data) > 0:
                        print("\nSample Call Option Structure:")
                        sample_ce = ce_data[0]
                        for key, value in sample_ce.items():
                            print(f"   {key}: {value}")
                
        return True
        
    except Exception as e:
        print(f"❌ Structure test error: {e}")
        return False

def test_historical_options():
    """Test for historical options data"""
    print("\n📈 Testing Historical Options Data...")
    print("=" * 60)
    
    try:
        # Try to get options data for a specific date
        print("Attempting to get historical options data...")
        
        # Test different approaches
        test_symbols = ['NIFTY', 'BANKNIFTY', 'RELIANCE', 'TCS']
        
        for symbol in test_symbols:
            try:
                print(f"\nTesting {symbol}...")
                
                # Try current options
                current_options = nse.nse_optionchain_scrapper(symbol)
                print(f"   ✅ Current options available for {symbol}")
                
                # Try historical data
                hist_data = nse.get_history(symbol=symbol, start=date(2024, 1, 1), end=date(2024, 12, 31))
                if hist_data is not None:
                    print(f"   ✅ Historical data available for {symbol}")
                else:
                    print(f"   ⚠️  No historical data for {symbol}")
                    
            except Exception as e:
                print(f"   ❌ Error with {symbol}: {e}")
                
        return True
        
    except Exception as e:
        print(f"❌ Historical test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 NSE Python Options Data Test")
    print("=" * 60)
    
    # Test 1: Basic functionality
    basic_success = test_nsepython_basic()
    
    if basic_success:
        # Test 2: Data structure
        structure_success = test_options_data_structure()
        
        # Test 3: Historical data
        historical_success = test_historical_options()
        
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Basic Functionality: {'✅ PASS' if basic_success else '❌ FAIL'}")
        print(f"Data Structure: {'✅ PASS' if structure_success else '❌ FAIL'}")
        print(f"Historical Data: {'✅ PASS' if historical_success else '❌ FAIL'}")
        
        if basic_success and structure_success:
            print("\n🎉 nsepython is working! We can proceed with historical options data collection.")
        else:
            print("\n⚠️  Some tests failed. We may need alternative approaches.")
    else:
        print("\n❌ Basic functionality failed. nsepython may not be working properly.")

if __name__ == "__main__":
    main()
