#!/usr/bin/env python3
"""
Collect 5 Years of NSE Derivatives Data (2020-2024)
Simplified version with better error handling and smaller chunks
"""

from jugaad_data import nse
import pandas as pd
from datetime import date, timedelta
import os
import time
import json

def get_monthly_expiries(year):
    """Get monthly expiry dates for a year (last Thursday of each month)"""
    expiries = []
    
    for month in range(1, 13):
        # Start from last day of month
        last_day = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
        
        # Find last Thursday
        while last_day.weekday() != 3:  # Thursday = 3
            last_day -= timedelta(days=1)
        
        expiries.append(last_day)
    
    return sorted(expiries)

def collect_single_expiry(symbol, expiry_date, year):
    """Collect data for a single expiry date"""
    try:
        # Get futures data
        futures_data = None
        try:
            futures_data = nse.derivatives_df(
                symbol=symbol,
                from_date=expiry_date - timedelta(days=30),
                to_date=expiry_date,
                expiry_date=expiry_date,
                instrument_type='FUTIDX'
            )
        except Exception as e:
            print(f"   ⚠️  Futures error for {expiry_date}: {str(e)[:50]}...")
        
        # Get options data for a few key strikes
        options_data_list = []
        
        # Define strikes based on year
        if year <= 2021:
            strikes = [15000, 16000]  # Fewer strikes for older years
        elif year <= 2022:
            strikes = [17000, 18000]
        elif year <= 2023:
            strikes = [19000, 20000]
        else:
            strikes = [21000, 22000]
        
        for strike in strikes:
            for option_type in ['CE', 'PE']:
                try:
                    options_data = nse.derivatives_df(
                        symbol=symbol,
                        from_date=expiry_date - timedelta(days=30),
                        to_date=expiry_date,
                        expiry_date=expiry_date,
                        instrument_type='OPTIDX',
                        strike_price=strike,
                        option_type=option_type
                    )
                    
                    if options_data is not None and len(options_data) > 0:
                        # Add metadata
                        options_data['OPTION_TYPE'] = option_type
                        options_data['STRIKE_PRICE'] = strike
                        options_data['INSTRUMENT_TYPE'] = 'OPTIDX'
                        options_data['YEAR'] = year
                        options_data_list.append(options_data)
                        
                except Exception as e:
                    continue  # Silently continue for individual options
        
        # Process futures data
        if futures_data is not None and len(futures_data) > 0:
            futures_data['INSTRUMENT_TYPE'] = 'FUTIDX'
            futures_data['YEAR'] = year
            futures_data['OPTION_TYPE'] = ''
            futures_data['STRIKE_PRICE'] = ''
        
        # Combine all data
        all_data = []
        if futures_data is not None and len(futures_data) > 0:
            all_data.append(futures_data)
        all_data.extend(options_data_list)
        
        if all_data:
            combined = pd.concat(all_data, ignore_index=True)
            return combined
        else:
            return None
            
    except Exception as e:
        print(f"   ❌ Error collecting {symbol} {expiry_date}: {str(e)[:50]}...")
        return None

def collect_year_data(symbol, year, output_dir):
    """Collect data for a specific year"""
    print(f"\n📊 Collecting {symbol} data for {year}")
    print("=" * 50)
    
    # Get monthly expiries only (more reliable than weekly)
    expiry_dates = get_monthly_expiries(year)
    print(f"📅 Found {len(expiry_dates)} monthly expiry dates for {year}")
    
    all_data = []
    successful_expiries = 0
    failed_expiries = 0
    
    for i, expiry in enumerate(expiry_dates):
        print(f"  📅 Processing {expiry} ({i+1}/{len(expiry_dates)})")
        
        data = collect_single_expiry(symbol, expiry, year)
        
        if data is not None and len(data) > 0:
            all_data.append(data)
            successful_expiries += 1
            print(f"    ✅ Collected {len(data)} records")
        else:
            failed_expiries += 1
            print(f"    ❌ No data collected")
        
        # Small delay between requests
        time.sleep(0.5)
    
    if all_data:
        # Combine all data
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Save to file
        output_file = os.path.join(output_dir, f'{symbol}_{year}_monthly.csv')
        combined_data.to_csv(output_file, index=False)
        
        print(f"\n✅ {symbol} {year}: Collected {len(combined_data)} records")
        print(f"   Successful expiries: {successful_expiries}")
        print(f"   Failed expiries: {failed_expiries}")
        print(f"   Saved to: {output_file}")
        
        return combined_data
    else:
        print(f"\n❌ {symbol} {year}: No data collected")
        return None

def main():
    """Main function"""
    print("🚀 Starting 5-Year NSE Derivatives Data Collection (Monthly Only)")
    print("=" * 70)
    print("This will collect monthly expiry data for years: 2020, 2021, 2022, 2023, 2024")
    print("Symbols: NIFTY, BANKNIFTY")
    print("Strategy: Monthly expiries only (more reliable than weekly)")
    print("=" * 70)
    
    # Create output directory
    output_dir = "monthly_5year_derivatives"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created output directory: {output_dir}")
    
    # Define years to collect
    years = [2020, 2021, 2022, 2023, 2024]
    symbols = ['NIFTY', 'BANKNIFTY']
    
    all_years_data = {}
    
    # Collect data year by year
    for year in years:
        print(f"\n{'='*80}")
        print(f"📅 COLLECTING YEAR: {year}")
        print(f"{'='*80}")
        
        year_data = {}
        
        for symbol in symbols:
            data = collect_year_data(symbol, year, output_dir)
            if data is not None:
                year_data[symbol] = data
                all_years_data[f"{symbol}_{year}"] = data
        
        # Save year summary
        if year_data:
            year_summary = {
                'year': year,
                'symbols': list(year_data.keys()),
                'total_records': sum(len(data) for data in year_data.values()),
                'symbol_records': {symbol: len(data) for symbol, data in year_data.items()}
            }
            
            summary_file = os.path.join(output_dir, f'{year}_summary.json')
            with open(summary_file, 'w') as f:
                json.dump(year_summary, f, indent=2, default=str)
            
            print(f"\n📊 {year} Summary:")
            print(f"   Total Records: {year_summary['total_records']}")
            print(f"   Symbols: {year_summary['symbols']}")
            print(f"   Summary saved to: {summary_file}")
    
    # Create combined dataset
    print(f"\n{'='*80}")
    print("🔗 CREATING COMBINED DATASET")
    print(f"{'='*80}")
    
    if all_years_data:
        # Combine all years for each symbol
        for symbol in symbols:
            symbol_data = []
            for year in years:
                key = f"{symbol}_{year}"
                if key in all_years_data:
                    symbol_data.append(all_years_data[key])
            
            if symbol_data:
                combined_symbol_data = pd.concat(symbol_data, ignore_index=True)
                
                # Save combined data
                combined_file = os.path.join(output_dir, f'{symbol}_5year_monthly_combined.csv')
                combined_symbol_data.to_csv(combined_file, index=False)
                
                print(f"✅ {symbol} 5-Year Combined:")
                print(f"   Total Records: {len(combined_symbol_data)}")
                print(f"   Date Range: {combined_symbol_data['DATE'].min()} to {combined_symbol_data['DATE'].max()}")
                print(f"   Years: {sorted(combined_symbol_data['YEAR'].unique())}")
                print(f"   Saved to: {combined_file}")
        
        # Create overall summary
        total_records = sum(len(data) for data in all_years_data.values())
        print(f"\n🎉 5-YEAR COLLECTION COMPLETE!")
        print(f"   Total Records: {total_records}")
        print(f"   Years Covered: {years}")
        print(f"   Symbols: {symbols}")
        print(f"   Output Directory: {output_dir}")
        
        return True
    else:
        print(f"\n❌ No data collected for any year")
        return False

if __name__ == "__main__":
    main()
