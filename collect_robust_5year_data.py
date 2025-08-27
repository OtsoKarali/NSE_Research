#!/usr/bin/env python3
"""
Collect Full 5 Years of NSE Derivatives Data (2020-2024)
Robust version with proper column handling and error recovery
"""

from jugaad_data import nse
import pandas as pd
from datetime import date, timedelta
import os
from tqdm import tqdm
import time

def get_expiry_dates_for_year(year):
    """Get all expiry dates for a specific year"""
    expiries = []
    
    # Start from January 1st of the year
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    
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

def standardize_columns(df, instrument_type, year):
    """Standardize column names and add metadata"""
    if df is None or len(df) == 0:
        return None
    
    # Create a copy to avoid modifying original
    df = df.copy()
    
    # Add metadata columns
    df['INSTRUMENT_TYPE'] = instrument_type
    df['YEAR'] = year
    
    # Standardize column names based on what we actually get
    column_mapping = {
        # Common columns
        'FH_TIMESTAMP': 'DATE',
        'FH_EXPIRY_DT': 'EXPIRY',
        'FH_OPENING_PRICE': 'OPEN',
        'FH_TRADE_HIGH_PRICE': 'HIGH',
        'FH_TRADE_LOW_PRICE': 'LOW',
        'FH_CLOSING_PRICE': 'CLOSE',
        'FH_LAST_TRADED_PRICE': 'LTP',
        'FH_SETTLE_PRICE': 'SETTLE_PRICE',
        'FH_TOT_TRADED_QTY': 'TOTAL_TRADED_QUANTITY',
        'FH_MARKET_LOT': 'MARKET_LOT',
        'FH_TOT_TRADED_VAL': 'TOTAL_TRADED_VALUE',
        'FH_OPEN_INT': 'OPEN_INTEREST',
        'FH_CHANGE_IN_OI': 'CHANGE_IN_OI',
        'FH_SYMBOL': 'SYMBOL',
        
        # Alternative column names
        'DATE': 'DATE',
        'EXPIRY': 'EXPIRY',
        'OPEN': 'OPEN',
        'HIGH': 'HIGH',
        'LOW': 'LOW',
        'CLOSE': 'CLOSE',
        'LTP': 'LTP',
        'SETTLEMENT': 'SETTLE_PRICE',
        'VOLUME': 'TOTAL_TRADED_QUANTITY',
        'OPEN_INTEREST': 'OPEN_INTEREST',
        'SYMBOL': 'SYMBOL'
    }
    
    # Rename columns that exist
    for old_name, new_name in column_mapping.items():
        if old_name in df.columns:
            df = df.rename(columns={old_name: new_name})
    
    return df

def collect_year_data(symbol, year, output_dir):
    """Collect data for a specific year"""
    print(f"\n📊 Collecting {symbol} data for {year}")
    print("=" * 60)
    
    # Get expiry dates for this year
    expiry_dates = get_expiry_dates_for_year(year)
    print(f"📅 Found {len(expiry_dates)} expiry dates for {year}")
    
    all_data = []
    successful_expiries = 0
    failed_expiries = 0
    
    # Collect data for each expiry
    for expiry in tqdm(expiry_dates, desc=f"Collecting {symbol} {year}"):
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
                futures_data = standardize_columns(futures_data, 'FUTIDX', year)
                if futures_data is not None:
                    all_data.append(futures_data)
            
            # Get options data for ATM strikes
            # Adjust strikes based on the year (NIFTY levels were different)
            if year <= 2021:
                atm_strikes = [12000, 13000, 14000, 15000, 16000]
            elif year <= 2022:
                atm_strikes = [15000, 16000, 17000, 18000, 19000]
            elif year <= 2023:
                atm_strikes = [18000, 19000, 20000, 21000, 22000]
            else:  # 2024+
                atm_strikes = [20000, 21000, 22000, 23000, 24000]
            
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
                            options_data = standardize_columns(options_data, 'OPTIDX', year)
                            if options_data is not None:
                                # Add option-specific metadata
                                options_data['OPTION_TYPE'] = option_type
                                options_data['STRIKE_PRICE'] = strike
                                all_data.append(options_data)
                            
                    except Exception as e:
                        # Silently continue for individual option failures
                        continue
            
            successful_expiries += 1
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.2)
            
        except Exception as e:
            failed_expiries += 1
            print(f"   ❌ {symbol} {expiry} error: {str(e)[:100]}...")
            continue
    
    if all_data:
        # Combine all data
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Save to file
        output_file = os.path.join(output_dir, f'{symbol}_{year}_derivatives.csv')
        combined_data.to_csv(output_file, index=False)
        
        print(f"✅ {symbol} {year}: Collected {len(combined_data)} records")
        print(f"   Successful expiries: {successful_expiries}")
        print(f"   Failed expiries: {failed_expiries}")
        print(f"   Saved to: {output_file}")
        
        return combined_data
    else:
        print(f"❌ {symbol} {year}: No data collected")
        return None

def collect_full_5year_data():
    """Collect 5 years of data (2020-2024)"""
    print("🚀 Full 5-Year NSE Derivatives Data Collection")
    print("=" * 60)
    
    # Create output directory
    output_dir = "full_5year_derivatives"
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
            import json
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
                combined_file = os.path.join(output_dir, f'{symbol}_5year_combined.csv')
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

def main():
    """Main function"""
    print("🚀 Starting Full 5-Year NSE Derivatives Data Collection")
    print("=" * 80)
    print("This will collect data for years: 2020, 2021, 2022, 2023, 2024")
    print("Symbols: NIFTY, BANKNIFTY")
    print("Estimated time: 30-60 minutes")
    print("=" * 80)
    
    success = collect_full_5year_data()
    
    if success:
        print(f"\n🎉 SUCCESS! Full 5-year data collection complete!")
        print(f"📁 Check the 'full_5year_derivatives' directory for your data!")
        print(f"\nNext steps:")
        print(f"1. Review the collected data")
        print(f"2. Run data quality checks")
        print(f"3. Begin your analysis framework")
    else:
        print(f"\n❌ Data collection failed. Check the logs above.")

if __name__ == "__main__":
    main()
