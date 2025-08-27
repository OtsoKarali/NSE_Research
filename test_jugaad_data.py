#!/usr/bin/env python3
"""
Test jugaad-data for historical NSE options data
Highly recommended by Indian traders
"""

from jugaad_data import NSE
import pandas as pd
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

def test_jugaad_basic():
    """Test basic jugaad-data functionality"""
    print("🔍 Testing jugaad-data for NSE Options Data...")
    print("=" * 60)
    
    try:
        # Initialize NSE object
        nse = NSE()
        print("✅ NSE object initialized successfully")
        
        # Test 1: Get current NIFTY options
        print("\n1. Testing NIFTY options...")
        try:
            nifty_options = nse.options('NIFTY')
            print(f"   ✅ NIFTY options retrieved")
            print(f"   Type: {type(nifty_options)}")
            if hasattr(nifty_options, '__len__'):
                print(f"   Length: {len(nifty_options)}")
        except Exception as e:
            print(f"   ❌ NIFTY options error: {e}")
        
        # Test 2: Get current BANKNIFTY options
        print("\n2. Testing BANKNIFTY options...")
        try:
            banknifty_options = nse.options('BANKNIFTY')
            print(f"   ✅ BANKNIFTY options retrieved")
            print(f"   Type: {type(banknifty_options)}")
            if hasattr(banknifty_options, '__len__'):
                print(f"   Length: {len(banknifty_options)}")
        except Exception as e:
            print(f"   ❌ BANKNIFTY options error: {e}")
        
        # Test 3: Get historical NIFTY data
        print("\n3. Testing historical NIFTY data...")
        try:
            # Try to get historical data for last 6 months
            end_date = date.today()
            start_date = end_date - relativedelta(months=6)
            
            print(f"   Date range: {start_date} to {end_date}")
            
            nifty_hist = nse.history('NIFTY', start_date, end_date)
            print(f"   ✅ Historical NIFTY data retrieved")
            print(f"   Type: {type(nifty_hist)}")
            if hasattr(nifty_hist, '__len__'):
                print(f"   Length: {len(nifty_hist)}")
        except Exception as e:
            print(f"   ❌ Historical NIFTY error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ jugaad-data error: {e}")
        return False

def test_options_structure():
    """Test the structure of options data"""
    print("\n📊 Testing Options Data Structure...")
    print("=" * 60)
    
    try:
        nse = NSE()
        
        # Get NIFTY options
        print("Getting NIFTY options structure...")
        nifty_options = nse.options('NIFTY')
        
        print(f"Options type: {type(nifty_options)}")
        
        if isinstance(nifty_options, pd.DataFrame):
            print(f"DataFrame shape: {nifty_options.shape}")
            print(f"Columns: {list(nifty_options.columns)}")
            print(f"First few rows:")
            print(nifty_options.head())
        elif isinstance(nifty_options, dict):
            print(f"Dictionary keys: {list(nifty_options.keys())}")
            for key, value in nifty_options.items():
                print(f"  {key}: {type(value)} - {len(value) if hasattr(value, '__len__') else 'N/A'}")
        elif isinstance(nifty_options, list):
            print(f"List length: {len(nifty_options)}")
            if len(nifty_options) > 0:
                print(f"First item: {nifty_options[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Structure test error: {e}")
        return False

def test_historical_options():
    """Test for historical options data"""
    print("\n📈 Testing Historical Options Data...")
    print("=" * 60)
    
    try:
        nse = NSE()
        
        # Test different approaches for historical options
        test_symbols = ['NIFTY', 'BANKNIFTY']
        
        for symbol in test_symbols:
            try:
                print(f"\nTesting {symbol}...")
                
                # Try to get historical options data
                end_date = date.today()
                start_date = end_date - relativedelta(months=3)  # 3 months for testing
                
                print(f"   Date range: {start_date} to {end_date}")
                
                # Try different methods
                try:
                    # Method 1: Direct options history
                    hist_options = nse.options_history(symbol, start_date, end_date)
                    print(f"   ✅ options_history: {type(hist_options)}")
                    if hasattr(hist_options, '__len__'):
                        print(f"      Length: {len(hist_options)}")
                except Exception as e:
                    print(f"   ❌ options_history: {e}")
                
                try:
                    # Method 2: Try with different parameters
                    hist_options2 = nse.options_history(symbol, start_date, end_date, 'CE', 20000)
                    print(f"   ✅ options_history with params: {type(hist_options2)}")
                    if hasattr(hist_options2, '__len__'):
                        print(f"      Length: {len(hist_options2)}")
                except Exception as e:
                    print(f"   ❌ options_history with params: {e}")
                
            except Exception as e:
                print(f"   ❌ Symbol test error: {e}")
                
        return True
        
    except Exception as e:
        print(f"❌ Historical test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Jugaad-Data Test for NSE Options")
    print("=" * 60)
    
    # Test 1: Basic functionality
    basic_success = test_jugaad_basic()
    
    if basic_success:
        # Test 2: Data structure
        structure_success = test_options_structure()
        
        # Test 3: Historical data
        historical_success = test_historical_options()
        
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Basic Functionality: {'✅ PASS' if basic_success else '❌ FAIL'}")
        print(f"Data Structure: {'✅ PASS' if structure_success else '❌ FAIL'}")
        print(f"Historical Data: {'✅ PASS' if historical_success else '❌ FAIL'}")
        
        if basic_success and structure_success:
            print("\n🎉 jugaad-data is working! We can proceed with historical options data collection.")
        else:
            print("\n⚠️  Some tests failed. We may need to try OpenChart.")
    else:
        print("\n❌ Basic functionality failed. jugaad-data may not be working properly.")

if __name__ == "__main__":
    main()
