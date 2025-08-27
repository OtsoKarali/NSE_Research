#!/usr/bin/env python3
"""
Maximize Working Symbols Data Collection
Focus on NIFTY and BANKNIFTY - the symbols we know work reliably
"""

from jugaad_data import nse
import pandas as pd
from datetime import date, timedelta
import os
import time
import json

def get_monthly_expiries(year, month):
    """Get monthly expiry date for a specific year and month (last Thursday)"""
    # Start from last day of month
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)
    
    # Find last Thursday
    while last_day.weekday() != 3:  # Thursday = 3
        last_day -= timedelta(days=1)
    
    return last_day

def collect_nifty_full_coverage():
    """Collect NIFTY data for full 5-year period with enhanced strikes"""
    print("🚀 Collecting NIFTY Full Coverage (2020-2024)")
    print("=" * 60)
    
    output_dir = "maximized_working_symbols/NIFTY"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Enhanced strikes for better coverage
    strikes_by_year = {
        2020: [14000, 15000, 16000, 17000],
        2021: [15000, 16000, 17000, 18000],
        2022: [16000, 17000, 18000, 19000, 20000],
        2023: [18000, 19000, 20000, 21000, 22000],
        2024: [20000, 21000, 22000, 23000, 24000]
    }
    
    all_data = []
    successful_years = 0
    
    for year in range(2020, 2025):
        print(f"\n📅 Processing {year}")
        print("-" * 40)
        
        year_data = []
        successful_months = 0
        
        for month in range(1, 13):
            try:
                expiry_date = get_monthly_expiries(year, month)
                strikes = strikes_by_year.get(year, [20000, 21000])
                
                print(f"   📅 {month:02d} (expiry: {expiry_date})")
                
                month_data = []
                for strike in strikes:
                    for option_type in ['CE', 'PE']:
                        try:
                            options_data = nse.derivatives_df(
                                symbol='NIFTY',
                                from_date=expiry_date - timedelta(days=30),
                                to_date=expiry_date,
                                expiry_date=expiry_date,
                                instrument_type='OPTIDX',
                                strike_price=strike,
                                option_type=option_type
                            )
                            
                            if options_data is not None and len(options_data) > 0:
                                # Add metadata
                                options_data['INSTRUMENT_TYPE'] = 'OPTIDX'
                                options_data['YEAR'] = year
                                options_data['MONTH'] = month
                                options_data['SYMBOL_NAME'] = 'NIFTY'
                                month_data.append(options_data)
                                
                        except Exception as e:
                            continue
                
                if month_data:
                    # Combine month data
                    combined_month = pd.concat(month_data, ignore_index=True)
                    year_data.append(combined_month)
                    successful_months += 1
                    
                    # Save individual month
                    month_file = os.path.join(output_dir, f'NIFTY_{year}_{month:02d}_options.csv')
                    combined_month.to_csv(month_file, index=False)
                    print(f"      ✅ {len(combined_month)} records")
                else:
                    print(f"      ❌ No data")
                
                time.sleep(0.5)  # Small delay
                
            except Exception as e:
                print(f"      ❌ Error: {str(e)[:50]}...")
                continue
        
        if year_data:
            # Combine year data
            combined_year = pd.concat(year_data, ignore_index=True)
            all_data.append(combined_year)
            successful_years += 1
            
            # Save year data
            year_file = os.path.join(output_dir, f'NIFTY_{year}_full_options.csv')
            combined_year.to_csv(year_file, index=False)
            print(f"\n   📊 {year}: {len(combined_year)} records, {successful_months}/12 months")
        
        time.sleep(1)  # Delay between years
    
    if all_data:
        # Combine all years
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Save combined data
        combined_file = os.path.join(output_dir, 'NIFTY_5year_maximized_options.csv')
        combined_data.to_csv(combined_file, index=False)
        
        print(f"\n🎉 NIFTY Collection Complete:")
        print(f"   Total Records: {len(combined_data)}")
        print(f"   Successful Years: {successful_years}")
        print(f"   Date Range: {combined_data['DATE'].min()} to {combined_data['DATE'].max()}")
        print(f"   Saved to: {combined_file}")
        
        return combined_data
    else:
        print(f"\n❌ No NIFTY data collected")
        return None

def collect_banknifty_working_periods():
    """Collect BANKNIFTY data for all working periods"""
    print("\n🚀 Collecting BANKNIFTY Working Periods")
    print("=" * 60)
    
    output_dir = "maximized_working_symbols/BANKNIFTY"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Define working periods based on our testing
    working_periods = [
        # 2020-2023: Full years (based on our earlier success)
        (2020, 1, 12),
        (2021, 1, 12),
        (2022, 1, 12),
        (2023, 1, 12),
        # 2024: Partial (Jan-Mar only, based on our testing)
        (2024, 1, 3)
    ]
    
    strikes_by_year = {
        2020: [30000, 32000, 34000],
        2021: [32000, 35000, 38000],
        2022: [35000, 38000, 41000],
        2023: [40000, 43000, 46000],
        2024: [45000, 47000, 49000]
    }
    
    all_data = []
    successful_periods = 0
    
    for year, start_month, end_month in working_periods:
        print(f"\n📅 Processing {year} (months {start_month}-{end_month})")
        print("-" * 50)
        
        year_data = []
        successful_months = 0
        
        for month in range(start_month, end_month + 1):
            try:
                expiry_date = get_monthly_expiries(year, month)
                strikes = strikes_by_year.get(year, [40000, 45000])
                
                print(f"   📅 {month:02d} (expiry: {expiry_date})")
                
                month_data = []
                for strike in strikes:
                    for option_type in ['CE', 'PE']:
                        try:
                            options_data = nse.derivatives_df(
                                symbol='BANKNIFTY',
                                from_date=expiry_date - timedelta(days=30),
                                to_date=expiry_date,
                                expiry_date=expiry_date,
                                instrument_type='OPTIDX',
                                strike_price=strike,
                                option_type=option_type
                            )
                            
                            if options_data is not None and len(options_data) > 0:
                                # Add metadata
                                options_data['INSTRUMENT_TYPE'] = 'OPTIDX'
                                options_data['YEAR'] = year
                                options_data['MONTH'] = month
                                options_data['SYMBOL_NAME'] = 'BANKNIFTY'
                                month_data.append(options_data)
                                
                        except Exception as e:
                            continue
                
                if month_data:
                    # Combine month data
                    combined_month = pd.concat(month_data, ignore_index=True)
                    year_data.append(combined_month)
                    successful_months += 1
                    
                    # Save individual month
                    month_file = os.path.join(output_dir, f'BANKNIFTY_{year}_{month:02d}_options.csv')
                    combined_month.to_csv(month_file, index=False)
                    print(f"      ✅ {len(combined_month)} records")
                else:
                    print(f"      ❌ No data")
                
                time.sleep(0.5)  # Small delay
                
            except Exception as e:
                print(f"      ❌ Error: {str(e)[:50]}...")
                continue
        
        if year_data:
            # Combine year data
            combined_year = pd.concat(year_data, ignore_index=True)
            all_data.append(combined_year)
            successful_periods += 1
            
            # Save year data
            year_file = os.path.join(output_dir, f'BANKNIFTY_{year}_full_options.csv')
            combined_year.to_csv(year_file, index=False)
            print(f"\n   📊 {year}: {len(combined_year)} records, {successful_months} months")
        
        time.sleep(1)  # Delay between years
    
    if all_data:
        # Combine all periods
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Save combined data
        combined_file = os.path.join(output_dir, 'BANKNIFTY_working_periods_options.csv')
        combined_data.to_csv(combined_file, index=False)
        
        print(f"\n🎉 BANKNIFTY Collection Complete:")
        print(f"   Total Records: {len(combined_data)}")
        print(f"   Successful Periods: {successful_periods}")
        print(f"   Date Range: {combined_data['DATE'].min()} to {combined_data['DATE'].max()}")
        print(f"   Saved to: {combined_file}")
        
        return combined_data
    else:
        print(f"\n❌ No BANKNIFTY data collected")
        return None

def main():
    """Main function - maximize working symbols"""
    print("🚀 MAXIMIZING WORKING SYMBOLS DATA COLLECTION")
    print("=" * 80)
    print("Focus: NIFTY and BANKNIFTY - the symbols we know work reliably")
    print("Strategy: Maximize coverage for working symbols rather than force broken ones")
    print("=" * 80)
    
    # Create main output directory
    main_output_dir = "maximized_working_symbols"
    if not os.path.exists(main_output_dir):
        os.makedirs(main_output_dir)
        print(f"📁 Created main output directory: {main_output_dir}")
    
    results = {}
    
    # Collect NIFTY data
    print(f"\n{'='*80}")
    print("📊 PHASE 1: NIFTY FULL COVERAGE")
    print(f"{'='*80}")
    
    nifty_data = collect_nifty_full_coverage()
    if nifty_data is not None:
        results['NIFTY'] = {
            'status': 'SUCCESS',
            'total_records': len(nifty_data),
            'date_range': f"{nifty_data['DATE'].min()} to {nifty_data['DATE'].max()}",
            'years': sorted(nifty_data['YEAR'].unique())
        }
    
    # Collect BANKNIFTY data
    print(f"\n{'='*80}")
    print("📊 PHASE 2: BANKNIFTY WORKING PERIODS")
    print(f"{'='*80}")
    
    banknifty_data = collect_banknifty_working_periods()
    if banknifty_data is not None:
        results['BANKNIFTY'] = {
            'status': 'SUCCESS',
            'total_records': len(banknifty_data),
            'date_range': f"{banknifty_data['DATE'].min()} to {banknifty_data['DATE'].max()}",
            'years': sorted(banknifty_data['YEAR'].unique())
        }
    
    # Summary
    print(f"\n{'='*80}")
    print("📊 MAXIMIZATION SUMMARY")
    print(f"{'='*80}")
    
    total_records = 0
    successful_symbols = 0
    
    for symbol, result in results.items():
        print(f"\n📊 {symbol}:")
        print(f"   Status: {result['status']}")
        print(f"   Total Records: {result['total_records']}")
        print(f"   Date Range: {result['date_range']}")
        print(f"   Years: {result['years']}")
        
        if result['status'] == 'SUCCESS':
            successful_symbols += 1
            total_records += result['total_records']
    
    print(f"\n🎯 OVERALL RESULTS:")
    print(f"   Successful Symbols: {successful_symbols}/{len(results)}")
    print(f"   Total Records Collected: {total_records}")
    print(f"   Output Directory: {main_output_dir}")
    
    # Save summary
    summary_file = os.path.join(main_output_dir, 'maximization_summary.json')
    with open(summary_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"   📊 Summary saved to: {summary_file}")
    
    if successful_symbols > 0:
        print(f"\n✅ Maximization successful! We now have comprehensive data for working symbols.")
        print(f"🎯 Next: Build analysis framework with this solid foundation!")

if __name__ == "__main__":
    main()
