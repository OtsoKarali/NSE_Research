#!/usr/bin/env python3
"""
Test jugaad-data for historical NSE options data
Using the correct module structure
"""

from jugaad_data import nse
import pandas as pd
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

def test_jugaad_basic():
    """Test basic jugaad-data functionality"""
    print("🔍 Testing jugaad-data for NSE Options Data...")
    print("=" * 60)
    
    try:
        print("✅ jugaad-data imported successfully")
        
        # Test 1: Get derivatives data
        print("\n1. Testing derivatives data...")
        try:
            # Try to get derivatives data for today
            today = date.today()
            derivatives_data = nse.derivatives_df(today)
            print(f"   ✅ Derivatives data retrieved")
            print(f"   Type: {type(derivatives_data)}")
            if hasattr(derivatives_data, '__len__'):
                print(f"   Length: {len(derivatives_data)}")
                if len(derivatives_data) > 0:
                    print(f"   Shape: {derivatives_data.shape}")
                    print(f"   Columns: {list(derivatives_data.columns)}")
        except Exception as e:
            print(f"   ❌ Derivatives data error: {e}")
        
        # Test 2: Get options data specifically
        print("\n2. Testing options data...")
        try:
            # Try to get options data
            options_data = nse.derivatives_df(today, instrument_type='OPTIDX')
            print(f"   ✅ Options data retrieved")
            print(f"   Type: {type(options_data)}")
            if hasattr(options_data, '__len__'):
                print(f"   Length: {len(options_data)}")
                if len(options_data) > 0:
                    print(f"   Shape: {options_data.shape}")
                    print(f"   Columns: {list(options_data.columns)}")
        except Exception as e:
            print(f"   ❌ Options data error: {e}")
        
        # Test 3: Get futures data
        print("\n3. Testing futures data...")
        try:
            futures_data = nse.derivatives_df(today, instrument_type='FUTIDX')
            print(f"   ✅ Futures data retrieved")
            print(f"   Type: {type(futures_data)}")
            if hasattr(futures_data, '__len__'):
                print(f"   Length: {len(futures_data)}")
        except Exception as e:
            print(f"   ❌ Futures data error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ jugaad-data error: {e}")
        return False

def test_historical_data():
    """Test historical data collection"""
    print("\n📈 Testing Historical Data Collection...")
    print("=" * 60)
    
    try:
        # Test getting data for multiple dates
        end_date = date.today()
        start_date = end_date - timedelta(days=7)  # Last week for testing
        
        print(f"Date range: {start_date} to {end_date}")
        
        all_data = []
        current_date = start_date
        
        while current_date <= end_date:
            try:
                print(f"\n   Collecting data for {current_date}...")
                
                # Get derivatives data for this date
                derivatives = nse.derivatives_df(current_date)
                
                if derivatives is not None and len(derivatives) > 0:
                    print(f"     ✅ Retrieved {len(derivatives)} records")
                    
                    # Add date column
                    derivatives['date'] = current_date
                    all_data.append(derivatives)
                else:
                    print(f"     ⚠️  No data for {current_date}")
                
                current_date += timedelta(days=1)
                
            except Exception as e:
                print(f"     ❌ Error for {current_date}: {e}")
                current_date += timedelta(days=1)
        
        if all_data:
            # Combine all data
            combined_data = pd.concat(all_data, ignore_index=True)
            
            print(f"\n📊 Historical Data Summary:")
            print(f"   Total Records: {len(combined_data)}")
            print(f"   Date Range: {combined_data['date'].min()} to {combined_data['date'].max()}")
            print(f"   Columns: {list(combined_data.columns)}")
            
            # Save sample data
            output_path = 'jugaad_historical_sample.csv'
            combined_data.to_csv(output_path, index=False)
            print(f"   💾 Sample data saved to: {output_path}")
            
            return True
        else:
            print(f"\n❌ No historical data collected")
            return False
        
    except Exception as e:
        print(f"❌ Historical test error: {e}")
        return False

def test_options_analysis():
    """Test options-specific analysis"""
    print("\n🎯 Testing Options Analysis...")
    print("=" * 60)
    
    try:
        # Get today's data
        today = date.today()
        
        # Get options data
        options_data = nse.derivatives_df(today, instrument_type='OPTIDX')
        
        if options_data is not None and len(options_data) > 0:
            print(f"✅ Options data retrieved: {len(options_data)} records")
            
            # Analyze options data
            print(f"\n📊 Options Analysis:")
            print(f"   Total Options: {len(options_data)}")
            
            # Check for call/put options
            if 'OPTION_TYP' in options_data.columns:
                call_options = options_data[options_data['OPTION_TYP'] == 'CE']
                put_options = options_data[options_data['OPTION_TYP'] == 'PE']
                print(f"   Call Options: {len(call_options)}")
                print(f"   Put Options: {len(put_options)}")
            
            # Check for different symbols
            if 'SYMBOL' in options_data.columns:
                symbols = options_data['SYMBOL'].unique()
                print(f"   Unique Symbols: {len(symbols)}")
                print(f"   Sample Symbols: {list(symbols[:5])}")
            
            # Check for expiry dates
            if 'EXPIRY_DT' in options_data.columns:
                expiries = options_data['EXPIRY_DT'].unique()
                print(f"   Unique Expiries: {len(expiries)}")
                print(f"   Sample Expiries: {list(expiries[:5])}")
            
            # Show sample data
            print(f"\n📋 Sample Options Data:")
            print(options_data.head())
            
            return True
        else:
            print(f"❌ No options data available")
            return False
        
    except Exception as e:
        print(f"❌ Options analysis error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Jugaad-Data Test for NSE Options (Corrected)")
    print("=" * 60)
    
    # Test 1: Basic functionality
    basic_success = test_jugaad_basic()
    
    if basic_success:
        # Test 2: Historical data
        historical_success = test_historical_data()
        
        # Test 3: Options analysis
        options_success = test_options_analysis()
        
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Basic Functionality: {'✅ PASS' if basic_success else '❌ FAIL'}")
        print(f"Historical Data: {'✅ PASS' if historical_success else '❌ FAIL'}")
        print(f"Options Analysis: {'✅ PASS' if options_success else '❌ FAIL'}")
        
        if basic_success and historical_success:
            print("\n🎉 jugaad-data is working! We can now collect historical options data.")
            print("This will give you the 3-5 year analysis you need!")
        else:
            print("\n⚠️  Some tests failed. We may need to try OpenChart.")
    else:
        print("\n❌ Basic functionality failed. jugaad-data may not be working properly.")

if __name__ == "__main__":
    main()
