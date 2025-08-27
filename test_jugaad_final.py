#!/usr/bin/env python3
"""
Final test for jugaad-data with correct parameters
"""

from jugaad_data import nse
import pandas as pd
from datetime import datetime, date, timedelta

def test_options_with_correct_params():
    """Test options data with correct parameters"""
    print("🔍 Testing jugaad-data Options with Correct Parameters...")
    print("=" * 60)
    
    try:
        print("✅ jugaad-data imported successfully")
        
        today = date.today()
        sample_expiry = today + timedelta(days=30)
        
        # Test options with required parameters
        print(f"\nTesting NIFTY options for {today}...")
        print(f"Expiry: {sample_expiry}")
        
        # Try different strike prices and option types
        test_strikes = [20000, 21000, 22000]  # Sample NIFTY strikes
        test_option_types = ['CE', 'PE']  # Call and Put
        
        for strike in test_strikes:
            for option_type in test_option_types:
                try:
                    print(f"\n   Testing {option_type} at strike {strike}...")
                    
                    options_data = nse.derivatives_df(
                        symbol='NIFTY',
                        from_date=today,
                        to_date=today,
                        expiry_date=sample_expiry,
                        instrument_type='OPTIDX',
                        strike_price=strike,
                        option_type=option_type
                    )
                    
                    if options_data is not None and len(options_data) > 0:
                        print(f"     ✅ {option_type} {strike}: {len(options_data)} records")
                        print(f"     Columns: {list(options_data.columns)}")
                        
                        # Save sample data
                        output_path = f'jugaad_nifty_{option_type}_{strike}_sample.csv'
                        options_data.to_csv(output_path, index=False)
                        print(f"     💾 Sample data saved to: {output_path}")
                        
                        return True
                    else:
                        print(f"     ⚠️  {option_type} {strike}: No data")
                        
                except Exception as e:
                    print(f"     ❌ {option_type} {strike} error: {e}")
        
        return False
        
    except Exception as e:
        print(f"❌ Options test error: {e}")
        return False

def test_futures_data():
    """Test futures data (simpler than options)"""
    print("\n📊 Testing Futures Data...")
    print("=" * 60)
    
    try:
        today = date.today()
        sample_expiry = today + timedelta(days=30)
        
        print(f"Testing NIFTY futures for {today}...")
        print(f"Expiry: {sample_expiry}")
        
        futures_data = nse.derivatives_df(
            symbol='NIFTY',
            from_date=today,
            to_date=today,
            expiry_date=sample_expiry,
            instrument_type='FUTIDX'
        )
        
        if futures_data is not None and len(futures_data) > 0:
            print(f"✅ Futures data retrieved: {len(futures_data)} records")
            print(f"Shape: {futures_data.shape}")
            print(f"Columns: {list(futures_data.columns)}")
            
            # Save sample data
            output_path = 'jugaad_nifty_futures_sample.csv'
            futures_data.to_csv(output_path, index=False)
            print(f"💾 Futures data saved to: {output_path}")
            
            return True
        else:
            print(f"❌ No futures data available")
            return False
        
    except Exception as e:
        print(f"❌ Futures test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Final Jugaad-Data Test for NSE Options")
    print("=" * 60)
    
    # Test 1: Options with correct parameters
    options_success = test_options_with_correct_params()
    
    # Test 2: Futures data
    futures_success = test_futures_data()
    
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Options Data: {'✅ PASS' if options_success else '❌ FAIL'}")
    print(f"Futures Data: {'✅ PASS' if futures_success else '❌ FAIL'}")
    
    if options_success:
        print("\n🎉 jugaad-data options are working! We can now collect historical options data.")
        print("This will give you the 3-5 year analysis you need!")
    elif futures_success:
        print("\n⚠️  Futures data works, but options data failed. We may need to try other approaches.")
    else:
        print("\n❌ Both tests failed. We need to try a different approach.")

if __name__ == "__main__":
    main()
