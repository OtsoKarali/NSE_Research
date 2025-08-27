#!/usr/bin/env python3
"""
Test OpenChart for historical NSE options data
Clean Python interface for NSE F&O data
"""

import openchart
import pandas as pd
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

def test_openchart_basic():
    """Test basic OpenChart functionality"""
    print("🔍 Testing OpenChart for NSE Options Data...")
    print("=" * 60)
    
    try:
        print("✅ OpenChart imported successfully")
        
        # Test 1: Get NSE data object
        print("\n1. Testing NSEData object...")
        try:
            nse_data = openchart.NSEData()
            print(f"   ✅ NSEData object created successfully")
            print(f"   Type: {type(nse_data)}")
            print(f"   Available methods: {[x for x in dir(nse_data) if not x.startswith('_')]}")
        except Exception as e:
            print(f"   ❌ NSEData creation error: {e}")
            return False
        
        # Test 2: Get available symbols
        print("\n2. Testing symbol availability...")
        try:
            # Try to get available symbols
            symbols = nse_data.get_symbols()
            print(f"   ✅ Symbols retrieved")
            print(f"   Type: {type(symbols)}")
            if hasattr(symbols, '__len__'):
                print(f"   Length: {len(symbols)}")
                if len(symbols) > 0:
                    print(f"   Sample symbols: {list(symbols[:5])}")
        except Exception as e:
            print(f"   ❌ Symbols error: {e}")
        
        # Test 3: Get historical data
        print("\n3. Testing historical data...")
        try:
            # Try to get historical data for NIFTY
            end_date = date.today()
            start_date = end_date - timedelta(days=30)  # Last month for testing
            
            print(f"   Date range: {start_date} to {end_date}")
            
            hist_data = nse_data.get_history('NIFTY', start_date, end_date, 'daily')
            print(f"   ✅ Historical data retrieved")
            print(f"   Type: {type(hist_data)}")
            if hasattr(hist_data, '__len__'):
                print(f"   Length: {len(hist_data)}")
                if len(hist_data) > 0:
                    print(f"   Shape: {hist_data.shape}")
                    print(f"   Columns: {list(hist_data.columns)}")
        except Exception as e:
            print(f"   ❌ Historical data error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenChart error: {e}")
        return False

def test_options_data():
    """Test options-specific data"""
    print("\n🎯 Testing Options Data...")
    print("=" * 60)
    
    try:
        nse_data = openchart.NSEData()
        
        # Test getting options data
        print("Testing options data retrieval...")
        
        try:
            # Try to get options data for NIFTY
            end_date = date.today()
            start_date = end_date - timedelta(days=7)  # Last week for testing
            
            print(f"Date range: {start_date} to {end_date}")
            
            # Try different granularities
            for granularity in ['daily', 'weekly', '1min']:
                try:
                    print(f"\n   Testing {granularity} granularity...")
                    
                    options_data = nse_data.get_history('NIFTY', start_date, end_date, granularity)
                    
                    if options_data is not None and len(options_data) > 0:
                        print(f"     ✅ {granularity} data: {len(options_data)} records")
                        print(f"     Shape: {options_data.shape}")
                        print(f"     Columns: {list(options_data.columns)}")
                        
                        # Save sample data
                        output_path = f'openchart_{granularity}_sample.csv'
                        options_data.to_csv(output_path, index=False)
                        print(f"     💾 Sample data saved to: {output_path}")
                        
                        return True
                    else:
                        print(f"     ⚠️  No {granularity} data")
                        
                except Exception as e:
                    print(f"     ❌ {granularity} error: {e}")
            
            return False
            
        except Exception as e:
            print(f"❌ Options data error: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Options test error: {e}")
        return False

def test_futures_options():
    """Test futures and options data"""
    print("\n📊 Testing Futures & Options (NFO) Data...")
    print("=" * 60)
    
    try:
        nse_data = openchart.NSEData()
        
        # Test different instrument types
        test_instruments = ['NIFTY', 'BANKNIFTY', 'RELIANCE', 'TCS']
        
        for instrument in test_instruments:
            try:
                print(f"\nTesting {instrument}...")
                
                # Try to get data
                end_date = date.today()
                start_date = end_date - timedelta(days=7)
                
                data = nse_data.get_history(instrument, start_date, end_date, 'daily')
                
                if data is not None and len(data) > 0:
                    print(f"   ✅ {instrument}: {len(data)} records")
                    print(f"   Columns: {list(data.columns)}")
                else:
                    print(f"   ⚠️  {instrument}: No data")
                    
            except Exception as e:
                print(f"   ❌ {instrument} error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ F&O test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 OpenChart Test for NSE Options Data")
    print("=" * 60)
    
    # Test 1: Basic functionality
    basic_success = test_openchart_basic()
    
    if basic_success:
        # Test 2: Options data
        options_success = test_options_data()
        
        # Test 3: Futures & Options
        fo_success = test_futures_options()
        
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Basic Functionality: {'✅ PASS' if basic_success else '❌ FAIL'}")
        print(f"Options Data: {'✅ PASS' if options_success else '❌ FAIL'}")
        print(f"Futures & Options: {'✅ PASS' if fo_success else '❌ FAIL'}")
        
        if basic_success and options_success:
            print("\n🎉 OpenChart is working! We can now collect historical options data.")
            print("This will give you the 3-5 year analysis you need!")
        else:
            print("\n⚠️  Some tests failed. We may need to try other approaches.")
    else:
        print("\n❌ Basic functionality failed. OpenChart may not be working properly.")

if __name__ == "__main__":
    main()
