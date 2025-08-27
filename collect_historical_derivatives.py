#!/usr/bin/env python3
"""
Collect Historical NSE Derivatives Data
Using the working jugaad-data derivatives_df function
"""

from jugaad_data import nse
import pandas as pd
from datetime import date, timedelta
import os
from tqdm import tqdm

def get_expiry_dates(start_date, end_date):
    """Get list of expiry dates (monthly and weekly)"""
    expiries = []
    current_date = start_date
    
    while current_date <= end_date:
        # Add monthly expiry (last Thursday)
        month_end = current_date.replace(day=28)
        while month_end.weekday() != 3:  # Thursday = 3
            month_end -= timedelta(days=1)
        if month_end >= start_date and month_end <= end_date:
            expiries.append(month_end)
        
        # Add weekly expiry (every Thursday)
        week_start = current_date - timedelta(days=current_date.weekday())
        for i in range(4):  # 4 weeks
            thursday = week_start + timedelta(days=3 + i*7)
            if thursday >= start_date and thursday <= end_date and thursday not in expiries:
                expiries.append(thursday)
        
        current_date += timedelta(days=30)
    
    return sorted(list(set(expiries)))

def collect_historical_data(symbol, start_date, end_date, output_dir):
    """Collect historical derivatives data for a symbol"""
    print(f"📊 Collecting {symbol} data from {start_date} to {end_date}")
    
    # Get expiry dates
    expiry_dates = get_expiry_dates(start_date, end_date)
    print(f"📅 Found {len(expiry_dates)} expiry dates")
    
    all_data = []
    
    # Collect data for each expiry
    for expiry in tqdm(expiry_dates, desc=f"Collecting {symbol} data"):
        try:
            # Get futures data
            futures_data = nse.derivatives_df(
                symbol=symbol,
                from_date=expiry - timedelta(days=30),  # Month before expiry
                to_date=expiry,
                expiry_date=expiry,
                instrument_type='FUTIDX'
            )
            
            if futures_data is not None and len(futures_data) > 0:
                futures_data['INSTRUMENT_TYPE'] = 'FUTIDX'
                all_data.append(futures_data)
            
            # Get options data for ATM strikes
            atm_strikes = [20000, 21000, 22000, 23000, 24000]  # Sample strikes
            
            for strike in atm_strikes:
                for option_type in ['CE', 'PE']:
                    try:
                        options_data = nse.derivatives_df(
                            symbol=symbol,
                            from_date=expiry - timedelta(days=30),
                            to_date=expiry,
                            expiry_date=expiry,
                            instrument_type='OPTIDX',
                            strike_price=strike,
                            option_type=option_type
                        )
                        
                        if options_data is not None and len(options_data) > 0:
                            options_data['INSTRUMENT_TYPE'] = 'OPTIDX'
                            all_data.append(options_data)
                            
                    except Exception as e:
                        print(f"   ⚠️  {symbol} {option_type} {strike} error: {e}")
                        continue
            
        except Exception as e:
            print(f"   ❌ {symbol} {expiry} error: {e}")
            continue
    
    if all_data:
        # Combine all data
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Save to file
        output_file = os.path.join(output_dir, f'{symbol}_historical_derivatives.csv')
        combined_data.to_csv(output_file, index=False)
        
        print(f"✅ {symbol}: Collected {len(combined_data)} records")
        print(f"   Saved to: {output_file}")
        
        return combined_data
    else:
        print(f"❌ {symbol}: No data collected")
        return None

def main():
    """Main function to collect historical derivatives data"""
    print("🚀 Historical NSE Derivatives Data Collection")
    print("=" * 60)
    
    # Create output directory
    output_dir = "historical_derivatives"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created output directory: {output_dir}")
    
    # Define date range (last 1 year)
    end_date = date.today() - timedelta(days=1)  # Yesterday
    start_date = end_date - timedelta(days=365)  # 1 year ago
    
    print(f"📅 Date range: {start_date} to {end_date}")
    
    # Collect data for NIFTY and BANKNIFTY
    symbols = ['NIFTY', 'BANKNIFTY']
    
    for symbol in symbols:
        print(f"\n{'='*60}")
        data = collect_historical_data(symbol, start_date, end_date, output_dir)
        
        if data is not None:
            print(f"\n📊 {symbol} Data Summary:")
            print(f"   Total Records: {len(data)}")
            print(f"   Date Range: {data['DATE'].min()} to {data['DATE'].max()}")
            print(f"   Instrument Types: {data['INSTRUMENT_TYPE'].unique()}")
            
            if 'OPTION TYPE' in data.columns:
                option_types = data['OPTION TYPE'].unique()
                print(f"   Option Types: {option_types}")
    
    print(f"\n🎉 Data collection complete!")
    print(f"📁 Check the '{output_dir}' directory for your historical derivatives data.")

if __name__ == "__main__":
    main()
