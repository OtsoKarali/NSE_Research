#!/usr/bin/env python3
"""
Main analysis runner for NSE options market analysis.
Orchestrates the entire analysis pipeline.
"""

import yaml
import logging
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_loader import NSEDataLoader
from liquidity_analysis import LiquidityAnalyzer

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main analysis pipeline."""
    logger.info("🚀 Starting NSE Options Market Analysis Pipeline")
    
    try:
        # Load configuration
        config_path = Path(__file__).parent / 'config.yaml'
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        logger.info("Configuration loaded successfully")
        
        # Set random seed
        np.random.seed(config['analysis']['random_seed'])
        logger.info(f"Random seed set to: {config['analysis']['random_seed']}")
        
        # Create output directories
        outputs_dir = Path(__file__).parent / 'outputs'
        figures_dir = Path(__file__).parent / 'figures'
        outputs_dir.mkdir(exist_ok=True)
        figures_dir.mkdir(exist_ok=True)
        
        logger.info("Output directories created")
        
        # Initialize data loader
        data_loader = NSEDataLoader(config)
        logger.info("Data loader initialized")
        
        # Load and process data
        logger.info("Loading options data...")
        df = data_loader.load_options_data(config['data']['options_file'])
        
        # Validate data quality
        logger.info("Validating data quality...")
        validation_report = data_loader.validate_data_quality(df)
        
        # Generate data summary
        logger.info("Generating data summary...")
        data_summary = data_loader.get_data_summary(df)
        
        # Initialize liquidity analyzer
        liquidity_analyzer = LiquidityAnalyzer(config)
        logger.info("Liquidity analyzer initialized")
        
        # Compute liquidity metrics
        logger.info("Computing liquidity metrics...")
        liquidity_metrics = liquidity_analyzer.compute_liquidity_metrics(df)
        
        # Create visualizations
        logger.info("Creating visualizations...")
        liquidity_analyzer.create_liquidity_dashboard(df, str(figures_dir / 'liquidity_dashboard.png'))
        
        if 'moneyness' in df.columns and 'expiry' in df.columns:
            liquidity_analyzer.create_liquidity_heatmaps(df, str(figures_dir / 'liquidity_heatmaps.png'))
        
        # Export results
        logger.info("Exporting results...")
        liquidity_analyzer.export_liquidity_tables(liquidity_metrics, str(outputs_dir / 'liquidity_metrics'))
        
        # Save processed data
        df.to_csv(outputs_dir / 'processed_options_data.csv', index=False)
        
        # Save summary statistics
        summary_df = pd.DataFrame([
            {'metric': 'total_records', 'value': len(df)},
            {'metric': 'unique_underlyings', 'value': df['underlying'].nunique()},
            {'metric': 'unique_expiries', 'value': df['expiry'].nunique()},
            {'metric': 'total_volume', 'value': df['volume'].sum()},
            {'metric': 'call_options', 'value': len(df[df['option_type'] == 'CE'])},
            {'metric': 'put_options', 'value': len(df[df['option_type'] == 'PE'])},
            {'metric': 'data_quality_score', 'value': validation_report['quality_score']}
        ])
        summary_df.to_csv(outputs_dir / 'data_summary.csv', index=False)
        
        # Generate final report
        generate_final_report(data_summary, validation_report, liquidity_metrics, outputs_dir)
        
        logger.info("✅ Analysis pipeline completed successfully!")
        
        # Print key findings
        print("\n" + "="*60)
        print("NSE OPTIONS MARKET ANALYSIS - KEY FINDINGS")
        print("="*60)
        print(f"📊 Total Records: {len(df):,}")
        print(f"🏢 Unique Underlyings: {df['underlying'].nunique()}")
        print(f"📅 Unique Expiries: {df['expiry'].nunique()}")
        print(f"📈 Call Options: {len(df[df['option_type'] == 'CE']):,}")
        print(f"📉 Put Options: {len(df[df['option_type'] == 'PE']):,}")
        print(f"💰 Total Volume: {df['volume'].sum()/1e6:.1f}M contracts")
        print(f"🎯 Data Quality Score: {validation_report['quality_score']:.2f}")
        print(f"📏 Median Spread: {liquidity_metrics['spread_metrics']['median_spread_bps']:.1f} bps")
        
        print(f"\n📁 Results saved to: {outputs_dir}")
        print(f"🖼️  Figures saved to: {figures_dir}")
        
    except Exception as e:
        logger.error(f"❌ Analysis pipeline failed: {e}")
        raise

def generate_final_report(data_summary, validation_report, liquidity_metrics, outputs_dir):
    """Generate final analysis report."""
    logger.info("Generating final report...")
    
    report_content = f"""
# NSE Options Market Analysis Report
*Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Executive Summary

This report presents a comprehensive analysis of the Indian National Stock Exchange (NSE) options market based on data from August 26, 2025.

## Data Overview

### Dataset Statistics
- **Total Records**: {data_summary['overview']['total_records']:,}
- **Unique Underlyings**: {data_summary['overview']['unique_underlyings']}
- **Unique Expiries**: {data_summary['overview']['unique_expiries']}
- **Data Quality Score**: {validation_report['quality_score']:.2f}

### Options Distribution
- **Call Options**: {data_summary['options_distribution']['call_options']:,}
- **Put Options**: {data_summary['options_distribution']['put_options']:,}
- **Call-Put Ratio**: {data_summary['options_distribution']['call_put_ratio']:.2f}

### Volume Analysis
- **Total Volume**: {data_summary['volume_analysis']['total_volume']/1e6:.1f}M contracts
- **Average Volume per Contract**: {data_summary['volume_analysis']['avg_volume_per_contract']:,.0f}

## Liquidity Analysis

### Spread Metrics
- **Median Spread**: {liquidity_metrics['spread_metrics']['median_spread_bps']:.1f} bps
- **Mean Spread**: {liquidity_metrics['spread_metrics']['mean_spread_bps']:.1f} bps
- **95th Percentile Spread**: {liquidity_metrics['spread_metrics']['spread_95th_percentile']:.1f} bps

### Top Underlyings by Volume
"""
    
    # Add top underlyings
    if 'top_underlyings' in liquidity_metrics['liquidity_rankings']:
        for i, (underlying, data) in enumerate(list(liquidity_metrics['liquidity_rankings']['top_underlyings'].items())[:10], 1):
            volume = data['volume'] / 1e6
            report_content += f"- **{i}. {underlying}**: {volume:.1f}M contracts\n"
    
    report_content += f"""
## Data Quality Assessment

### Validation Results
- **Quality Score**: {validation_report['quality_score']:.2f}
- **Total Records**: {validation_report['total_records']:,}
- **Data Issues**: {len(validation_report['data_issues'])}

### Missing Data Analysis
"""
    
    # Add missing data analysis
    for col, pct in validation_report['missing_data'].items():
        if pct > 0:
            report_content += f"- **{col}**: {pct:.1f}% missing\n"
    
    if validation_report['data_issues']:
        report_content += "\n### Data Issues Found\n"
        for issue in validation_report['data_issues']:
            report_content += f"- {issue}\n"
    
    report_content += f"""
## Recommendations

### For Market Participants
1. **Focus on Liquid Instruments**: Prioritize options with high volume and tight spreads
2. **Monitor Spread Dynamics**: Track spread changes across different expiries and moneyness levels
3. **Risk Management**: Use proper position sizing based on liquidity metrics

### For Further Analysis
1. **Microstructure Analysis**: Investigate intraday patterns and order flow
2. **Volatility Surface**: Build implied volatility surfaces for pricing models
3. **Event Studies**: Analyze market behavior around expiry and regulatory events

## Technical Notes

- **Analysis Date**: {pd.Timestamp.now().strftime('%Y-%m-%d')}
- **Data Source**: NSE Options Market Data
- **Processing**: Automated pipeline with quality validation
- **Visualizations**: Generated using matplotlib with publication-quality settings

---

*This report is generated automatically from the NSE options market analysis pipeline. For detailed methodology and additional analysis, refer to the individual analysis notebooks.*
"""
    
    # Save report
    with open(outputs_dir / 'analysis_report.md', 'w') as f:
        f.write(report_content)
    
    logger.info("Final report generated successfully")

if __name__ == "__main__":
    main()
