#!/usr/bin/env python3
"""
Simple test of derivatives_df to see what's actually happening
"""

from jugaad_data import nse
import pandas as pd
from datetime import date, timedelta

def test_simple_derivatives():
    """Test derivatives_df with minimal parameters"""
    print("🔍 Testing derivatives_df with minimal parameters...")
    print("=" * 60)
    
    try:
        # Use a real historical date
        test_date = date(2024, 12, 20)
        expiry_date = date(2024, 12, 26)  # Friday expiry
        
        print(f"Test date: {test_date}")
        print(f"Expiry date: {expiry_date}")
        
        # Test 1: Simple futures
        print("\n1. Testing FUTIDX...")
        try:
            futures_data = nse.derivatives_df(
                symbol='NIFTY',
                from_date=test_date,
                to_date=test_date,
                expiry_date=expiry_date,
                instrument_type='FUTIDX'
            )
            
            if futures_data is not None and len(futures_data) > 0:
                print(f"   ✅ FUTIDX data: {len(futures_data)} records")
                print(f"   Columns: {list(futures_data.columns)}")
                print(f"   Sample data:")
                print(futures_data.head())
                
                # Save sample
                futures_data.to_csv('nifty_futures_sample.csv', index=False)
                print(f"   💾 Saved to: nifty_futures_sample.csv")
                
                return True
            else:
                print(f"   ⚠️  No FUTIDX data")
                
        except Exception as e:
            print(f"   ❌ FUTIDX error: {e}")
            print(f"   Error type: {type(e)}")
        
        # Test 2: Options with specific strike
        print("\n2. Testing OPTIDX with specific strike...")
        try:
            options_data = nse.derivatives_df(
                symbol='NIFTY',
                from_date=test_date,
                to_date=test_date,
                expiry_date=expiry_date,
                instrument_type='OPTIDX',
                strike_price=21000,  # ATM strike for Dec 2024
                option_type='CE'
            )
            
            if options_data is not None and len(options_data) > 0:
                print(f"   ✅ OPTIDX data: {len(options_data)} records")
                print(f"   Columns: {list(options_data.columns)}")
                print(f"   Sample data:")
                print(options_data.head())
                
                # Save sample
                options_data.to_csv('nifty_options_sample.csv', index=False)
                print(f"   💾 Saved to: nifty_options_sample.csv")
                
                return True
            else:
                print(f"   ⚠️  No OPTIDX data")
                
        except Exception as e:
            print(f"   ❌ OPTIDX error: {e}")
            print(f"   Error type: {type(e)}")
        
        return False
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Simple Derivatives Test")
    print("=" * 60)
    
    success = test_simple_derivatives()
    
    if success:
        print("\n🎉 SUCCESS! We can get derivatives data!")
        print("Now we can build a proper data collection pipeline.")
    else:
        print("\n❌ Still having issues. Let me investigate further.")

if __name__ == "__main__":
    main()
