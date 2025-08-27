#!/usr/bin/env python3
"""
Download Historical NIFTY Data using Yahoo Finance
Alternative to NSE direct access when facing connectivity issues.
"""

import yfinance as yf
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def download_nifty_data():
    """Download 5 years of NIFTY index data"""
    print("📈 Downloading Historical NIFTY Data...")
    print("=" * 50)
    
    # Download NIFTY 50 data (5 years)
    print("Downloading NIFTY 50 data...")
    nifty = yf.download("^NSEI", 
                        start="2020-01-01", 
                        end="2025-08-26",
                        progress=False)
    
    print(f"✅ NIFTY 50: {len(nifty)} trading days downloaded")
    print(f"   Date range: {nifty.index.min().date()} to {nifty.index.max().date()}")
    print(f"   Columns: {list(nifty.columns)}")
    
    # Download BANKNIFTY data
    print("\nDownloading BANKNIFTY data...")
    banknifty = yf.download("^NSEBANK", 
                           start="2020-01-01", 
                           end="2025-08-26",
                           progress=False)
    
    print(f"✅ BANKNIFTY: {len(banknifty)} trading days downloaded")
    print(f"   Date range: {banknifty.index.min().date()} to {banknifty.index.max().date()}")
    
    return nifty, banknifty

def save_data(nifty, banknifty):
    """Save downloaded data to files"""
    print("\n💾 Saving Data...")
    
    # Create output directory
    output_dir = Path("historical_data")
    output_dir.mkdir(exist_ok=True)
    
    # Save NIFTY data
    nifty_csv = output_dir / "nifty_50_5y.csv"
    nifty_parquet = output_dir / "nifty_50_5y.parquet"
    
    nifty.to_csv(nifty_csv)
    nifty.to_parquet(nifty_parquet)
    
    print(f"✅ NIFTY 50 saved:")
    print(f"   CSV: {nifty_csv}")
    print(f"   Parquet: {nifty_parquet}")
    
    # Save BANKNIFTY data
    banknifty_csv = output_dir / "banknifty_5y.csv"
    banknifty_parquet = output_dir / "banknifty_5y.parquet"
    
    banknifty.to_csv(banknifty_csv)
    banknifty.to_parquet(banknifty_parquet)
    
    print(f"✅ BANKNIFTY saved:")
    print(f"   CSV: {banknifty_csv}")
    print(f"   Parquet: {banknifty_parquet}")
    
    return output_dir

def create_summary_stats(nifty, banknifty):
    """Create summary statistics for the data"""
    print("\n📊 Data Summary Statistics...")
    print("=" * 50)
    
    # NIFTY summary
    print("NIFTY 50 Summary:")
    print(f"   Total Trading Days: {len(nifty)}")
    print(f"   Date Range: {nifty.index.min().date()} to {nifty.index.max().date()}")
    print(f"   Starting Price: ₹{float(nifty['Close'].iloc[0]):.2f}")
    print(f"   Ending Price: ₹{float(nifty['Close'].iloc[-1]):.2f}")
    print(f"   Total Return: {((float(nifty['Close'].iloc[-1]) / float(nifty['Close'].iloc[0])) - 1) * 100:.2f}%")
    print(f"   Highest Price: ₹{float(nifty['High'].max()):.2f}")
    print(f"   Lowest Price: ₹{float(nifty['Low'].min()):.2f}")
    print(f"   Average Volume: {float(nifty['Volume'].mean()):,.0f}")
    
    print("\nBANKNIFTY Summary:")
    print(f"   Total Trading Days: {len(banknifty)}")
    print(f"   Date Range: {banknifty.index.min().date()} to {banknifty.index.max().date()}")
    print(f"   Starting Price: ₹{float(banknifty['Close'].iloc[0]):.2f}")
    print(f"   Ending Price: ₹{float(banknifty['Close'].iloc[-1]):.2f}")
    print(f"   Total Return: {((float(banknifty['Close'].iloc[-1]) / float(banknifty['Close'].iloc[0])) - 1) * 100:.2f}%")
    print(f"   Highest Price: ₹{float(banknifty['High'].max()):.2f}")
    print(f"   Lowest Price: ₹{float(banknifty['Low'].min()):.2f}")
    print(f"   Average Volume: {float(banknifty['Volume'].mean()):,.0f}")

def create_visualizations(nifty, banknifty, output_dir):
    """Create basic visualizations of the data"""
    print("\n📈 Creating Visualizations...")
    
    # Set up the plot
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('NIFTY & BANKNIFTY Historical Data (2020-2025)', fontsize=16)
    
    # NIFTY Price Chart
    axes[0, 0].plot(nifty.index, nifty['Close'], color='blue', linewidth=1)
    axes[0, 0].set_title('NIFTY 50 - Closing Prices')
    axes[0, 0].set_ylabel('Price (₹)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # BANKNIFTY Price Chart
    axes[0, 1].plot(banknifty.index, banknifty['Close'], color='green', linewidth=1)
    axes[0, 1].set_title('BANKNIFTY - Closing Prices')
    axes[0, 1].set_ylabel('Price (₹)')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Volume Charts
    axes[1, 0].bar(nifty.index, nifty['Volume'], color='blue', alpha=0.6)
    axes[1, 0].set_title('NIFTY 50 - Trading Volume')
    axes[1, 0].set_ylabel('Volume')
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].bar(banknifty.index, banknifty['Volume'], color='green', alpha=0.6)
    axes[1, 1].set_title('BANKNIFTY - Trading Volume')
    axes[1, 1].set_ylabel('Volume')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    for ax in axes.flat:
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Save the plot
    plot_path = output_dir / "nifty_banknifty_5y_charts.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"✅ Charts saved to: {plot_path}")
    
    plt.show()

def main():
    """Main function to download and analyze NIFTY data"""
    print("🚀 NIFTY Historical Data Downloader")
    print("Using Yahoo Finance as alternative to NSE direct access")
    print("=" * 60)
    
    try:
        # Download data
        nifty, banknifty = download_nifty_data()
        
        # Save data
        output_dir = save_data(nifty, banknifty)
        
        # Create summary statistics
        create_summary_stats(nifty, banknifty)
        
        # Create visualizations
        create_visualizations(nifty, banknifty, output_dir)
        
        print("\n" + "=" * 60)
        print("✅ Data download and analysis completed successfully!")
        print(f"📁 All files saved to: {output_dir}")
        print("\nNext steps:")
        print("1. Use this data for trend analysis")
        print("2. Combine with options data when available")
        print("3. Build historical volatility models")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("This might be due to:")
        print("- Internet connectivity issues")
        print("- Yahoo Finance API limitations")
        print("- Data availability issues")

if __name__ == "__main__":
    main()
