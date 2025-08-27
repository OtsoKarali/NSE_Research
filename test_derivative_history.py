#!/usr/bin/env python3
"""
Test nsepython derivative_history for historical options data
"""

import nsepython as nse
import pandas as pd
from datetime import datetime, date, timedelta
import time

def test_derivative_history():
    """Test derivative_history function for options data"""
    print("🔍 Testing nsepython derivative_history for Options Data...")
    print("=" * 70)
    
    try:
        # Test 1: Get current NIFTY options structure
        print("1. Getting current NIFTY options structure...")
        nifty_options = nse.nse_optionchain_scrapper('NIFTY')
        
        if nifty_options and 'records' in nifty_options:
            records = nifty_options['records']
            if 'data' in records:
                data = records['data']
                
                print("   ✅ NIFTY options structure retrieved")
                print(f"   Available keys: {list(data.keys())}")
                
                if 'CE' in data and 'PE' in data:
                    ce_data = data['CE']
                    pe_data = data['PE']
                    
                    print(f"   Call Options: {len(ce_data) if ce_data else 0} contracts")
                    print(f"   Put Options: {len(pe_data) if pe_data else 0} contracts")
                    
                    # Get sample strike and expiry for testing
                    if ce_data and len(ce_data) > 0:
                        sample_ce = ce_data[0]
                        print(f"   Sample Call Option: {sample_ce}")
                        
                        # Extract key fields for derivative history
                        if 'strikePrice' in sample_ce and 'expiryDate' in sample_ce:
                            strike = sample_ce['strikePrice']
                            expiry = sample_ce['expiryDate']
                            print(f"   Testing with Strike: {strike}, Expiry: {expiry}")
                            
                            # Test derivative history
                            print(f"\n2. Testing derivative_history for NIFTY...")
                            try:
                                # Try to get historical data for this option
                                hist_data = nse.derivative_history(
                                    symbol='NIFTY',
                                    instrument_type='OPTIDX',
                                    expiry_date=expiry,
                                    strike_price=strike,
                                    option_type='CE'
                                )
                                
                                if hist_data is not None and not hist_data.empty:
                                    print(f"   ✅ Historical options data retrieved!")
                                    print(f"   Records: {len(hist_data)}")
                                    print(f"   Columns: {list(hist_data.columns)}")
                                    print(f"   Date range: {hist_data.index.min()} to {hist_data.index.max()}")
                                    
                                    # Save sample data
                                    hist_data.to_csv('sample_historical_options.csv')
                                    print(f"   💾 Sample data saved to: sample_historical_options.csv")
                                    
                                    return True
                                else:
                                    print(f"   ⚠️  No historical data returned")
                                    
                            except Exception as e:
                                print(f"   ❌ derivative_history error: {e}")
                        else:
                            print(f"   ⚠️  Could not extract strike/expiry from sample data")
                    else:
                        print(f"   ⚠️  No call options data available")
                else:
                    print(f"   ⚠️  No CE/PE data in options structure")
            else:
                print(f"   ⚠️  No 'data' key in records")
        else:
            print(f"   ⚠️  No 'records' key in options data")
            
        return False
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_multiple_symbols():
    """Test derivative history for multiple symbols"""
    print("\n3. Testing multiple symbols...")
    print("=" * 70)
    
    test_cases = [
        {'symbol': 'NIFTY', 'instrument': 'OPTIDX'},
        {'symbol': 'BANKNIFTY', 'instrument': 'OPTIDX'},
        {'symbol': 'RELIANCE', 'instrument': 'OPTSTK'},
        {'symbol': 'TCS', 'instrument': 'OPTSTK'}
    ]
    
    for test_case in test_cases:
        try:
            print(f"\nTesting {test_case['symbol']} ({test_case['instrument']})...")
            
            # Get current options to find valid strike/expiry
            options = nse.nse_optionchain_scrapper(test_case['symbol'])
            
            if options and 'records' in options:
                records = options['records']
                if 'data' in records:
                    data = records['data']
                    
                    if 'CE' in data and data['CE']:
                        sample = data['CE'][0]
                        if 'strikePrice' in sample and 'expiryDate' in sample:
                            strike = sample['strikePrice']
                            expiry = sample['expiryDate']
                            
                            print(f"   Strike: {strike}, Expiry: {expiry}")
                            
                            try:
                                hist = nse.derivative_history(
                                    symbol=test_case['symbol'],
                                    instrument_type=test_case['instrument'],
                                    expiry_date=expiry,
                                    strike_price=strike,
                                    option_type='CE'
                                )
                                
                                if hist is not None and not hist.empty:
                                    print(f"   ✅ Historical data: {len(hist)} records")
                                else:
                                    print(f"   ⚠️  No historical data")
                                    
                            except Exception as e:
                                print(f"   ❌ Error: {e}")
                        else:
                            print(f"   ⚠️  No strike/expiry data")
                    else:
                        print(f"   ⚠️  No call options data")
                else:
                    print(f"   ⚠️  No data structure")
            else:
                print(f"   ⚠️  No options data available")
                
        except Exception as e:
            print(f"   ❌ Symbol test error: {e}")

def main():
    """Main test function"""
    print("🚀 NSE Python Derivative History Test")
    print("=" * 70)
    
    # Test 1: Basic derivative history
    success = test_derivative_history()
    
    if success:
        print("\n🎉 Successfully retrieved historical options data!")
        print("We can now build a historical data collection system.")
    else:
        print("\n⚠️  Basic test failed, trying alternative approaches...")
        test_multiple_symbols()
    
    print("\n" + "=" * 70)
    print("TEST COMPLETED")

if __name__ == "__main__":
    main()
