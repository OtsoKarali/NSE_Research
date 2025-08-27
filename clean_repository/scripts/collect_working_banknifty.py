#!/usr/bin/env python3
"""
Small-scale collection for BANKNIFTY during working period
Working period: December 2023 - March 2024
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

def collect_single_expiry_options(symbol, expiry_date, year, month):
    """Collect options data for a single expiry date"""
    try:
        print(f"    📅 Processing {expiry_date}")
        
        # Get options data for key strikes
        options_data_list = []
        
        # Define strikes for BANKNIFTY during this period
        strikes = [45000, 46000, 47000]
        
        successful_strikes = 0
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
                        options_data['INSTRUMENT_TYPE'] = 'OPTIDX'
                        options_data['YEAR'] = year
                        options_data['MONTH'] = month
                        options_data['SYMBOL_NAME'] = symbol
                        options_data_list.append(options_data)
                        successful_strikes += 1
                        
                except Exception as e:
                    print(f"      ⚠️  {option_type} {strike} error: {str(e)[:50]}...")
                    continue
        
        if options_data_list:
            # Combine all options data
            combined = pd.concat(options_data_list, ignore_index=True)
            print(f"      ✅ Collected options for {successful_strikes} strikes ({len(combined)} records)")
            return combined
        else:
            print(f"      ❌ No options data collected")
            return None
            
    except Exception as e:
        print(f"   ❌ Error collecting {symbol} {expiry_date}: {str(e)[:50]}...")
        return None

def collect_working_period_data():
    """Collect data for the working period (Dec 2023 - Mar 2024)"""
    print("🚀 Collecting BANKNIFTY Data for Working Period")
    print("=" * 60)
    print("Working Period: December 2023 - March 2024")
    print("Strategy: Monthly expiries only")
    print("=" * 60)
    
    # Create output directory
    output_dir = "working_banknifty_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created output directory: {output_dir}")
    
    # Define working period
    working_periods = [
        (2023, 12),
        (2024, 1),
        (2024, 2),
        (2024, 3)
    ]
    
    all_data = []
    successful_months = 0
    failed_months = 0
    
    for year, month in working_periods:
        print(f"\n📅 Processing {year}-{month:02d}")
        print("-" * 40)
        
        try:
            # Get expiry date for this month
            expiry_date = get_monthly_expiries(year, month)
            print(f"   📅 Expiry date: {expiry_date}")
            
            # Collect data for this expiry
            data = collect_single_expiry_options('BANKNIFTY', expiry_date, year, month)
            
            if data is not None and len(data) > 0:
                all_data.append(data)
                successful_months += 1
                
                # Save individual month data
                month_file = os.path.join(output_dir, f'BANKNIFTY_{year}_{month:02d}_options.csv')
                data.to_csv(month_file, index=False)
                print(f"   💾 Saved to: {month_file}")
            else:
                failed_months += 1
                print(f"   ❌ No data collected for {year}-{month:02d}")
            
            # Small delay between months
            time.sleep(1)
            
        except Exception as e:
            failed_months += 1
            print(f"   ❌ Error processing {year}-{month:02d}: {str(e)[:50]}...")
            continue
    
    # Combine all data
    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Save combined data
        combined_file = os.path.join(output_dir, 'BANKNIFTY_working_period_combined.csv')
        combined_data.to_csv(combined_file, index=False)
        
        print(f"\n🎉 COLLECTION COMPLETE!")
        print(f"   Total Records: {len(combined_data)}")
        print(f"   Successful Months: {successful_months}")
        print(f"   Failed Months: {failed_months}")
        print(f"   Date Range: {combined_data['DATE'].min()} to {combined_data['DATE'].max()}")
        print(f"   Saved to: {combined_file}")
        
        # Create summary
        summary = {
            'symbol': 'BANKNIFTY',
            'working_period': 'Dec 2023 - Mar 2024',
            'total_records': len(combined_data),
            'successful_months': successful_months,
            'failed_months': failed_months,
            'date_range': f"{combined_data['DATE'].min()} to {combined_data['DATE'].max()}",
            'output_directory': output_dir
        }
        
        summary_file = os.path.join(output_dir, 'collection_summary.json')
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"   📊 Summary saved to: {summary_file}")
        
        return True
    else:
        print(f"\n❌ No data collected for any month")
        return False

def main():
    """Main function"""
    print("🚀 BANKNIFTY Working Period Data Collection")
    print("=" * 80)
    print("This will collect data for the period when BANKNIFTY works")
    print("Working Period: December 2023 - March 2024")
    print("=" * 80)
    
    success = collect_working_period_data()
    
    if success:
        print(f"\n🎉 SUCCESS! Working period data collection complete!")
        print(f"📁 Check the 'working_banknifty_data' directory for your data!")
    else:
        print(f"\n❌ Data collection failed. Check the logs above.")

if __name__ == "__main__":
    main()
