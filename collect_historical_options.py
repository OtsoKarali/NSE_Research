#!/usr/bin/env python3
"""
Collect Historical NSE Options Data using nsepython
This script will collect historical options data for analysis
"""

import nsepython as nse
import pandas as pd
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import time
import json
from pathlib import Path

def get_current_options_structure(symbol):
    """Get current options structure to understand available strikes and expiries"""
    try:
        options = nse.nse_optionchain_scrapper(symbol)
        
        if options and 'records' in options:
            records = options['records']
            
            # Get expiry dates
            expiry_dates = records.get('expiryDates', [])
            
            # Get strike prices
            strike_prices = records.get('strikePrices', [])
            
            # Get underlying value
            underlying_value = records.get('underlyingValue', 0)
            
            print(f"✅ {symbol} Options Structure:")
            print(f"   Expiry Dates: {len(expiry_dates)} available")
            print(f"   Strike Prices: {len(strike_prices)} available")
            print(f"   Underlying Value: {underlying_value}")
            
            return {
                'expiry_dates': expiry_dates,
                'strike_prices': strike_prices,
                'underlying_value': underlying_value
            }
        else:
            print(f"❌ No options structure found for {symbol}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting options structure for {symbol}: {e}")
        return None

def collect_historical_options_data(symbol, instrument_type, expiry_date, strike_price, option_type):
    """Collect historical data for a specific option"""
    try:
        print(f"   Collecting {symbol} {option_type} {strike_price} {expiry_date}...")
        
        # Use derivative_history to get historical data
        hist_data = nse.derivative_history(
            symbol=symbol,
            instrument_type=instrument_type,
            expiry_date=expiry_date,
            strike_price=strike_price,
            option_type=option_type
        )
        
        if hist_data is not None and not hist_data.empty:
            print(f"     ✅ Retrieved {len(hist_data)} records")
            return hist_data
        else:
            print(f"     ⚠️  No historical data returned")
            return None
            
    except Exception as e:
        print(f"     ❌ Error collecting data: {e}")
        return None

def collect_comprehensive_options_data(symbol, instrument_type, start_date, end_date):
    """Collect comprehensive historical options data"""
    print(f"\n🚀 Collecting Historical Options Data for {symbol}")
    print("=" * 70)
    
    # Get current options structure
    structure = get_current_options_structure(symbol)
    if not structure:
        return None
    
    # Create output directory
    output_dir = Path("historical_options_data")
    output_dir.mkdir(exist_ok=True)
    
    all_data = []
    total_requests = 0
    successful_requests = 0
    
    # Focus on recent expiries and ATM strikes for efficiency
    recent_expiries = structure['expiry_dates'][:3]  # First 3 expiries
    atm_strikes = [strike for strike in structure['strike_prices'] 
                   if abs(strike - structure['underlying_value']) < 1000]  # ATM ±1000
    
    print(f"\n📅 Using {len(recent_expiries)} recent expiries")
    print(f"🎯 Using {len(atm_strikes)} ATM strikes")
    
    for expiry in recent_expiries:
        print(f"\n📅 Processing expiry: {expiry}")
        
        for strike in atm_strikes[:5]:  # Limit to 5 strikes per expiry for testing
            for option_type in ['CE', 'PE']:
                total_requests += 1
                
                hist_data = collect_historical_options_data(
                    symbol, instrument_type, expiry, strike, option_type
                )
                
                if hist_data is not None:
                    # Add metadata
                    hist_data['symbol'] = symbol
                    hist_data['expiry'] = expiry
                    hist_data['strike'] = strike
                    hist_data['option_type'] = option_type
                    hist_data['instrument_type'] = instrument_type
                    
                    all_data.append(hist_data)
                    successful_requests += 1
                
                # Rate limiting
                time.sleep(0.5)
    
    print(f"\n📊 Collection Summary:")
    print(f"   Total Requests: {total_requests}")
    print(f"   Successful: {successful_requests}")
    print(f"   Success Rate: {successful_requests/total_requests*100:.1f}%")
    
    if all_data:
        # Combine all data
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Save data
        csv_path = output_dir / f"{symbol}_historical_options.csv"
        parquet_path = output_dir / f"{symbol}_historical_options.parquet"
        
        combined_data.to_csv(csv_path, index=False)
        combined_data.to_parquet(parquet_path, index=False)
        
        print(f"\n💾 Data saved:")
        print(f"   CSV: {csv_path}")
        print(f"   Parquet: {parquet_path}")
        print(f"   Total Records: {len(combined_data)}")
        
        return combined_data
    else:
        print(f"\n❌ No data collected for {symbol}")
        return None

def main():
    """Main function to collect historical options data"""
    print("🚀 NSE Historical Options Data Collector")
    print("=" * 70)
    
    # Test symbols
    test_symbols = [
        {'symbol': 'NIFTY', 'instrument': 'OPTIDX'},
        {'symbol': 'BANKNIFTY', 'instrument': 'OPTIDX'}
    ]
    
    collected_data = {}
    
    for test_case in test_symbols:
        symbol = test_case['symbol']
        instrument = test_case['instrument']
        
        print(f"\n{'='*70}")
        print(f"Processing {symbol} ({instrument})")
        print(f"{'='*70}")
        
        # Set date range (last 6 months for testing)
        end_date = date.today()
        start_date = end_date - relativedelta(months=6)
        
        print(f"Date Range: {start_date} to {end_date}")
        
        # Collect data
        data = collect_comprehensive_options_data(symbol, instrument, start_date, end_date)
        
        if data is not None:
            collected_data[symbol] = data
            
            # Show sample of collected data
            print(f"\n📊 Sample Data for {symbol}:")
            print(f"   Shape: {data.shape}")
            print(f"   Columns: {list(data.columns)}")
            print(f"   Date Range: {data['date'].min()} to {data['date'].max()}")
            
            # Show first few records
            print(f"\nFirst few records:")
            print(data.head())
    
    print(f"\n{'='*70}")
    print("COLLECTION COMPLETED")
    print(f"{'='*70}")
    
    if collected_data:
        print(f"✅ Successfully collected data for {len(collected_data)} symbols:")
        for symbol, data in collected_data.items():
            print(f"   {symbol}: {len(data)} records")
        
        print(f"\n📁 All data saved to: historical_options_data/")
        print(f"🎯 You now have HISTORICAL options data for analysis!")
    else:
        print(f"❌ No data was collected. Check the errors above.")

if __name__ == "__main__":
    main()
