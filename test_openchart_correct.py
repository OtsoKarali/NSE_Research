#!/usr/bin/env python3
"""
Test OpenChart for historical NSE options data
Using the correct method names
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
        
        # Test 2: Get timeframes
        print("\n2. Testing timeframes...")
        try:
            timeframes = nse_data.timeframes()
            print(f"   ✅ Timeframes retrieved")
            print(f"   Type: {type(timeframes)}")
            if hasattr(timeframes, '__len__'):
                print(f"   Available timeframes: {list(timeframes)}")
        except Exception as e:
            print(f"   ❌ Timeframes error: {e}")
        
        # Test 3: Test NFO data
        print("\n3. Testing NFO data...")
        try:
            # Try to get NFO data
            nfo_data = nse_data.nfo_data()
            print(f"   ✅ NFO data retrieved")
            print(f"   Type: {type(nfo_data)}")
            if hasattr(nfo_data, '__len__'):
                print(f"   Length: {len(nfo_data)}")
                if len(nfo_data) > 0:
                    print(f"   Shape: {nfo_data.shape}")
                    print(f"   Columns: {list(nfo_data.columns)}")
        except Exception as e:
            print(f"   ❌ NFO data error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenChart error: {e}")
        return False

def test_historical_data():
    """Test historical data collection"""
    print("\n📈 Testing Historical Data Collection...")
    print("=" * 60)
    
    try:
        nse_data = openchart.NSEData()
        
        # Test getting historical data for different symbols
        test_symbols = ['NIFTY', 'BANKNIFTY', 'RELIANCE']
        
        for symbol in test_symbols:
            try:
                print(f"\nTesting {symbol}...")
                
                # Try to get historical data
                end_date = date.today()
                start_date = end_date - timedelta(days=30)  # Last month for testing
                
                print(f"   Date range: {start_date} to {end_date}")
                
                # Try different timeframes
                for timeframe in ['1D', '1W', '1M']:
                    try:
                        print(f"     Testing {timeframe} timeframe...")
                        
                        hist_data = nse_data.historical(symbol, start_date, end_date, timeframe)
                        
                        if hist_data is not None and len(hist_data) > 0:
                            print(f"       ✅ {timeframe} data: {len(hist_data)} records")
                            print(f"       Shape: {hist_data.shape}")
                            print(f"       Columns: {list(hist_data.columns)}")
                            
                            # Save sample data
                            output_path = f'openchart_{symbol}_{timeframe}_sample.csv'
                            hist_data.to_csv(output_path, index=False)
                            print(f"       💾 Sample data saved to: {output_path}")
                            
                            return True
                        else:
                            print(f"       ⚠️  No {timeframe} data")
                            
                    except Exception as e:
                        print(f"       ❌ {timeframe} error: {e}")
                
            except Exception as e:
                print(f"   ❌ {symbol} error: {e}")
        
        return False
        
    except Exception as e:
        print(f"❌ Historical test error: {e}")
        return False

def test_nfo_options():
    """Test NFO options data specifically"""
    print("\n🎯 Testing NFO Options Data...")
    print("=" * 60)
    
    try:
        nse_data = openchart.NSEData()
        
        # Test NFO data
        print("Testing NFO data retrieval...")
        
        try:
            nfo_data = nse_data.nfo_data()
            
            if nfo_data is not None and len(nfo_data) > 0:
                print(f"✅ NFO data retrieved: {len(nfo_data)} records")
                print(f"Shape: {nfo_data.shape}")
                print(f"Columns: {list(nfo_data.columns)}")
                
                # Show sample data
                print(f"\n📋 Sample NFO Data:")
                print(nfo_data.head())
                
                # Save NFO data
                output_path = 'openchart_nfo_sample.csv'
                nfo_data.to_csv(output_path, index=False)
                print(f"\n💾 NFO data saved to: {output_path}")
                
                # Check if it contains options data
                if 'OPTION_TYP' in nfo_data.columns or 'INSTRUMENT' in nfo_data.columns:
                    print(f"\n🎉 Found options data in NFO!")
                    
                    # Filter for options if possible
                    if 'INSTRUMENT' in nfo_data.columns:
                        options_data = nfo_data[nfo_data['INSTRUMENT'].str.contains('OPT', na=False)]
                        print(f"Options records: {len(options_data)}")
                        
                        if len(options_data) > 0:
                            options_output = 'openchart_options_sample.csv'
                            options_data.to_csv(options_output, index=False)
                            print(f"💾 Options data saved to: {options_output}")
                
                return True
            else:
                print(f"❌ No NFO data available")
                return False
                
        except Exception as e:
            print(f"❌ NFO data error: {e}")
            return False
        
    except Exception as e:
        print(f"❌ NFO test error: {e}")
        return False

def test_search_functionality():
    """Test search functionality"""
    print("\n🔍 Testing Search Functionality...")
    print("=" * 60)
    
    try:
        nse_data = openchart.NSEData()
        
        # Test search
        print("Testing symbol search...")
        
        try:
            # Search for NIFTY
            search_results = nse_data.search('NIFTY')
            print(f"✅ Search results for NIFTY:")
            print(f"   Type: {type(search_results)}")
            if hasattr(search_results, '__len__'):
                print(f"   Length: {len(search_results)}")
                if len(search_results) > 0:
                    print(f"   Results: {search_results}")
            
            # Search for BANKNIFTY
            search_results2 = nse_data.search('BANKNIFTY')
            print(f"\n✅ Search results for BANKNIFTY:")
            print(f"   Type: {type(search_results2)}")
            if hasattr(search_results2, '__len__'):
                print(f"   Length: {len(search_results2)}")
                if len(search_results2) > 0:
                    print(f"   Results: {search_results2}")
            
            return True
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Search test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 OpenChart Test for NSE Options Data (Corrected)")
    print("=" * 60)
    
    # Test 1: Basic functionality
    basic_success = test_openchart_basic()
    
    if basic_success:
        # Test 2: Historical data
        historical_success = test_historical_data()
        
        # Test 3: NFO options data
        nfo_success = test_nfo_options()
        
        # Test 4: Search functionality
        search_success = test_search_functionality()
        
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Basic Functionality: {'✅ PASS' if basic_success else '❌ FAIL'}")
        print(f"Historical Data: {'✅ PASS' if historical_success else '❌ FAIL'}")
        print(f"NFO Options Data: {'✅ PASS' if nfo_success else '❌ FAIL'}")
        print(f"Search Functionality: {'✅ PASS' if search_success else '❌ FAIL'}")
        
        if basic_success and nfo_success:
            print("\n🎉 OpenChart is working! We can now collect NFO options data.")
            print("This will give you the historical options data you need!")
        else:
            print("\n⚠️  Some tests failed. We may need to try other approaches.")
    else:
        print("\n❌ Basic functionality failed. OpenChart may not be working properly.")

if __name__ == "__main__":
    main()
