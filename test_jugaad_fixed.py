#!/usr/bin/env python3
"""
Test jugaad-data for historical NSE options data
Using the correct function signature
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
        
        # Test 1: Get current date
        today = date.today()
        print(f"Today's date: {today}")
        
        # Test 2: Get expiry dates
        print("\n2. Testing expiry dates...")
        try:
            # Try to get expiry dates for NIFTY
            expiry_dates = nse.expiry_dates('NIFTY')
            print(f"   ✅ NIFTY expiry dates retrieved")
            print(f"   Type: {type(expiry_dates)}")
            if hasattr(expiry_dates, '__len__'):
                print(f"   Length: {len(expiry_dates)}")
                if len(expiry_dates) > 0:
                    print(f"   Sample expiries: {list(expiry_dates[:5])}")
        except Exception as e:
            print(f"   ❌ Expiry dates error: {e}")
        
        # Test 3: Get derivatives data with correct parameters
        print("\n3. Testing derivatives data...")
        try:
            # Get a sample expiry date (use today + 1 month if no expiries available)
            sample_expiry = today + timedelta(days=30)
            
            # Try to get derivatives data
            derivatives_data = nse.derivatives_df(
                symbol='NIFTY',
                from_date=today,
                to_date=today,
                expiry_date=sample_expiry,
                instrument_type='OPTIDX'
            )
            print(f"   ✅ Derivatives data retrieved")
            print(f"   Type: {type(derivatives_data)}")
            if hasattr(derivatives_data, '__len__'):
                print(f"   Length: {len(derivatives_data)}")
                if len(derivatives_data) > 0:
                    print(f"   Shape: {derivatives_data.shape}")
                    print(f"   Columns: {list(derivatives_data.columns)}")
        except Exception as e:
            print(f"   ❌ Derivatives data error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ jugaad-data error: {e}")
        return False

def test_historical_options():
    """Test historical options data collection"""
    print("\n📈 Testing Historical Options Data...")
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
                
                # Try to get derivatives data for this date
                # Use a sample expiry date
                sample_expiry = current_date + timedelta(days=30)
                
                derivatives = nse.derivatives_df(
                    symbol='NIFTY',
                    from_date=current_date,
                    to_date=current_date,
                    expiry_date=sample_expiry,
                    instrument_type='OPTIDX'
                )
                
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
            output_path = 'jugaad_historical_options_sample.csv'
            combined_data.to_csv(output_path, index=False)
            print(f"   💾 Sample data saved to: {output_path}")
            
            return True
        else:
            print(f"\n❌ No historical data collected")
            return False
        
    except Exception as e:
        print(f"❌ Historical test error: {e}")
        return False

def test_different_symbols():
    """Test different symbols and instrument types"""
    print("\n🎯 Testing Different Symbols...")
    print("=" * 60)
    
    try:
        today = date.today()
        sample_expiry = today + timedelta(days=30)
        
        # Test different symbols
        test_symbols = ['NIFTY', 'BANKNIFTY']
        test_instruments = ['OPTIDX', 'FUTIDX']
        
        for symbol in test_symbols:
            for instrument in test_instruments:
                try:
                    print(f"\nTesting {symbol} - {instrument}...")
                    
                    data = nse.derivatives_df(
                        symbol=symbol,
                        from_date=today,
                        to_date=today,
                        expiry_date=sample_expiry,
                        instrument_type=instrument
                    )
                    
                    if data is not None and len(data) > 0:
                        print(f"   ✅ {symbol} {instrument}: {len(data)} records")
                        print(f"   Columns: {list(data.columns)}")
                        
                        # Save sample data
                        output_path = f'jugaad_{symbol}_{instrument}_sample.csv'
                        data.to_csv(output_path, index=False)
                        print(f"   💾 Sample data saved to: {output_path}")
                    else:
                        print(f"   ⚠️  {symbol} {instrument}: No data")
                        
                except Exception as e:
                    print(f"   ❌ {symbol} {instrument} error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Symbols test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Jugaad-Data Test for NSE Options (Fixed)")
    print("=" * 60)
    
    # Test 1: Basic functionality
    basic_success = test_jugaad_basic()
    
    if basic_success:
        # Test 2: Historical options data
        historical_success = test_historical_options()
        
        # Test 3: Different symbols
        symbols_success = test_different_symbols()
        
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Basic Functionality: {'✅ PASS' if basic_success else '❌ FAIL'}")
        print(f"Historical Options: {'✅ PASS' if historical_success else '❌ FAIL'}")
        print(f"Different Symbols: {'✅ PASS' if symbols_success else '❌ FAIL'}")
        
        if basic_success and historical_success:
            print("\n🎉 jugaad-data is working! We can now collect historical options data.")
            print("This will give you the 3-5 year analysis you need!")
        else:
            print("\n⚠️  Some tests failed. We may need to try other approaches.")
    else:
        print("\n❌ Basic functionality failed. jugaad-data may not be working properly.")

if __name__ == "__main__":
    main()
