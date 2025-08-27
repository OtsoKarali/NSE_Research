"""
Liquidity analysis for NSE options.
Computes spread metrics, depth analysis, and liquidity KPIs.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
import logging
from scipy import stats
from tqdm import tqdm

logger = logging.getLogger(__name__)

class LiquidityAnalyzer:
    """Analyzes liquidity metrics for options data."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.liquidity_thresholds = config['analysis']['liquidity']
        
    def compute_liquidity_metrics(self, df: pd.DataFrame) -> Dict:
        """Compute comprehensive liquidity metrics."""
        logger.info("Computing liquidity metrics")
        
        metrics = {
            'spread_metrics': self._compute_spread_metrics(df),
            'depth_metrics': self._compute_depth_metrics(df),
            'volume_metrics': self._compute_volume_metrics(df),
            'turnover_metrics': self._compute_turnover_metrics(df),
            'liquidity_rankings': self._compute_liquidity_rankings(df)
        }
        
        return metrics
    
    def _compute_spread_metrics(self, df: pd.DataFrame) -> Dict:
        """Compute spread-related metrics."""
        logger.info("Computing spread metrics")
        
        # Calculate various spread measures
        df['bid_ask_spread'] = df['high'] - df['low']
        df['relative_spread_bps'] = (df['bid_ask_spread'] / df['close']) * 10000
        
        # Effective spread (using high-low as proxy for bid-ask)
        df['effective_spread'] = df['bid_ask_spread'] / 2
        
        # Realized spread (approximation)
        df['realized_spread'] = df['effective_spread'] * 0.8  # Assumption
        
        spread_metrics = {
            'median_spread_bps': df['relative_spread_bps'].median(),
            'mean_spread_bps': df['relative_spread_bps'].mean(),
            'spread_95th_percentile': df['relative_spread_bps'].quantile(0.95),
            'spread_99th_percentile': df['relative_spread_bps'].quantile(0.99),
            'spread_distribution': {
                '0-10_bps': len(df[df['relative_spread_bps'] <= 10]),
                '10-25_bps': len(df[(df['relative_spread_bps'] > 10) & (df['relative_spread_bps'] <= 25)]),
                '25-50_bps': len(df[(df['relative_spread_bps'] > 25) & (df['relative_spread_bps'] <= 50)]),
                '50-100_bps': len(df[(df['relative_spread_bps'] > 50) & (df['relative_spread_bps'] <= 100)]),
                '100+_bps': len(df[df['relative_spread_bps'] > 100])
            }
        }
        
        return spread_metrics
    
    def _compute_depth_metrics(self, df: pd.DataFrame) -> Dict:
        """Compute depth-related metrics."""
        logger.info("Computing depth metrics")
        
        # Use volume as proxy for depth
        depth_metrics = {
            'median_depth': df['volume'].median(),
            'mean_depth': df['volume'].mean(),
            'depth_95th_percentile': df['volume'].quantile(0.95),
            'depth_99th_percentile': df['volume'].quantile(0.99),
            'depth_distribution': {
                '0-1K': len(df[df['volume'] <= 1000]),
                '1K-10K': len(df[(df['volume'] > 1000) & (df['volume'] <= 10000)]),
                '10K-100K': len(df[(df['volume'] > 10000) & (df['volume'] <= 100000)]),
                '100K-1M': len(df[(df['volume'] > 100000) & (df['volume'] <= 1000000)]),
                '1M+': len(df[df['volume'] > 1000000])
            }
        }
        
        return depth_metrics
    
    def _compute_volume_metrics(self, df: pd.DataFrame) -> Dict:
        """Compute volume-related metrics."""
        logger.info("Computing volume metrics")
        
        volume_metrics = {
            'total_volume': df['volume'].sum(),
            'total_contracts': len(df),
            'avg_volume_per_contract': df['volume'].mean(),
            'median_volume_per_contract': df['volume'].median(),
            'volume_concentration': {
                'top_10_pct_share': df['volume'].nlargest(int(len(df) * 0.1)).sum() / df['volume'].sum(),
                'top_25_pct_share': df['volume'].nlargest(int(len(df) * 0.25)).sum() / df['volume'].sum(),
                'top_50_pct_share': df['volume'].nlargest(int(len(df) * 0.5)).sum() / df['volume'].sum()
            }
        }
        
        return volume_metrics
    
    def _compute_turnover_metrics(self, df: pd.DataFrame) -> Dict:
        """Compute turnover-related metrics."""
        logger.info("Computing turnover metrics")
        
        if 'notional_value' in df.columns:
            total_turnover = df['notional_value'].sum()
            turnover_metrics = {
                'total_turnover': total_turnover,
                'avg_turnover_per_contract': df['notional_value'].mean(),
                'median_turnover_per_contract': df['notional_value'].median(),
                'turnover_concentration': {
                    'top_10_pct_share': df['notional_value'].nlargest(int(len(df) * 0.1)).sum() / total_turnover,
                    'top_25_pct_share': df['notional_value'].nlargest(int(len(df) * 0.25)).sum() / total_turnover,
                    'top_50_pct_share': df['notional_value'].nlargest(int(len(df) * 0.5)).sum() / total_turnover
                }
            }
        else:
            # Estimate turnover from volume and prices
            estimated_turnover = (df['volume'] * df['close']).sum()
            turnover_metrics = {
                'estimated_total_turnover': estimated_turnover,
                'avg_turnover_per_contract': (df['volume'] * df['close']).mean(),
                'median_turnover_per_contract': (df['volume'] * df['close']).median(),
                'note': 'Turnover estimated from volume * close price'
            }
        
        return turnover_metrics
    
    def _compute_liquidity_rankings(self, df: pd.DataFrame) -> Dict:
        """Compute liquidity rankings by underlying and expiry."""
        logger.info("Computing liquidity rankings")
        
        # By underlying
        underlying_liquidity = df.groupby('underlying').agg({
            'volume': 'sum',
            'notional_value': 'sum' if 'notional_value' in df.columns else lambda x: (x * df.loc[x.index, 'close']).sum()
        }).sort_values('volume', ascending=False)
        
        # By expiry
        expiry_liquidity = df.groupby('expiry').agg({
            'volume': 'sum',
            'notional_value': 'sum' if 'notional_value' in df.columns else lambda x: (x * df.loc[x.index, 'close']).sum()
        }).sort_values('volume', ascending=False)
        
        # By option type
        option_type_liquidity = df.groupby('option_type').agg({
            'volume': 'sum',
            'notional_value': 'sum' if 'notional_value' in df.columns else lambda x: (x * df.loc[x.index, 'close']).sum()
        }).sort_values('volume', ascending=False)
        
        rankings = {
            'top_underlyings': underlying_liquidity.head(20).to_dict('index'),
            'top_expiries': expiry_liquidity.head(10).to_dict('index'),
            'option_type_ranking': option_type_liquidity.to_dict('index')
        }
        
        return rankings
    
    def create_liquidity_heatmaps(self, df: pd.DataFrame, save_path: str) -> None:
        """Create liquidity heatmaps by expiry and moneyness."""
        logger.info("Creating liquidity heatmaps")
        
        # Prepare data for heatmaps
        if 'moneyness' in df.columns and 'expiry' in df.columns:
            # Create pivot table for volume heatmap
            volume_pivot = df.pivot_table(
                values='volume', 
                index='expiry', 
                columns='moneyness', 
                aggfunc='sum',
                fill_value=0
            )
            
            # Create pivot table for spread heatmap
            spread_pivot = df.pivot_table(
                values='relative_spread_bps', 
                index='expiry', 
                columns='moneyness', 
                aggfunc='mean',
                fill_value=np.nan
            )
            
            # Create the plots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
            
            # Volume heatmap
            im1 = ax1.imshow(volume_pivot.values, cmap='YlOrRd', aspect='auto')
            ax1.set_title('Volume by Expiry and Moneyness')
            ax1.set_xlabel('Moneyness')
            ax1.set_ylabel('Expiry')
            ax1.set_xticks(range(len(volume_pivot.columns)))
            ax1.set_xticklabels([f'{col:.2f}' for col in volume_pivot.columns], rotation=45)
            ax1.set_yticks(range(len(volume_pivot.index)))
            ax1.set_yticklabels(volume_pivot.index)
            plt.colorbar(im1, ax=ax1, label='Volume')
            
            # Spread heatmap
            im2 = ax2.imshow(spread_pivot.values, cmap='RdYlBu_r', aspect='auto')
            ax2.set_title('Average Spread (bps) by Expiry and Moneyness')
            ax2.set_xlabel('Moneyness')
            ax2.set_ylabel('Expiry')
            ax2.set_xticks(range(len(spread_pivot.columns)))
            ax2.set_xticklabels([f'{col:.2f}' for col in spread_pivot.columns], rotation=45)
            ax2.set_yticks(range(len(spread_pivot.index)))
            ax2.set_yticklabels(spread_pivot.index)
            plt.colorbar(im2, ax=ax2, label='Spread (bps)')
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Liquidity heatmaps saved to {save_path}")
        else:
            logger.warning("Cannot create heatmaps: missing moneyness or expiry data")
    
    def create_liquidity_dashboard(self, df: pd.DataFrame, save_path: str) -> None:
        """Create comprehensive liquidity dashboard."""
        logger.info("Creating liquidity dashboard")
        
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('NSE Options Liquidity Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Volume distribution by underlying
        top_underlyings = df.groupby('underlying')['volume'].sum().nlargest(15)
        axes[0, 0].barh(range(len(top_underlyings)), top_underlyings.values / 1e6)
        axes[0, 0].set_yticks(range(len(top_underlyings)))
        axes[0, 0].set_yticklabels(top_underlyings.index)
        axes[0, 0].set_xlabel('Volume (Millions)')
        axes[0, 0].set_title('Top 15 Underlyings by Volume')
        
        # 2. Spread distribution
        axes[0, 1].hist(df['relative_spread_bps'], bins=50, alpha=0.7, edgecolor='black')
        axes[0, 1].set_xlabel('Spread (bps)')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Spread Distribution')
        axes[0, 1].axvline(df['relative_spread_bps'].median(), color='red', linestyle='--', 
                           label=f'Median: {df["relative_spread_bps"].median():.1f} bps')
        axes[0, 1].legend()
        
        # 3. Volume by option type
        option_type_volume = df.groupby('option_type')['volume'].sum()
        axes[0, 2].pie(option_type_volume.values, labels=option_type_volume.index, autopct='%1.1f%%')
        axes[0, 2].set_title('Volume by Option Type')
        
        # 4. Volume by expiry
        expiry_volume = df.groupby('expiry')['volume'].sum().sort_values(ascending=False)
        axes[1, 0].bar(range(len(expiry_volume)), expiry_volume.values / 1e6)
        axes[1, 0].set_xticks(range(len(expiry_volume)))
        axes[1, 0].set_xticklabels(expiry_volume.index, rotation=45, ha='right')
        axes[1, 0].set_ylabel('Volume (Millions)')
        axes[1, 0].set_title('Volume by Expiry')
        
        # 5. Spread vs Volume scatter
        sample_df = df.sample(min(10000, len(df)))  # Sample for performance
        axes[1, 1].scatter(sample_df['volume'] / 1e6, sample_df['relative_spread_bps'], alpha=0.5)
        axes[1, 1].set_xlabel('Volume (Millions)')
        axes[1, 1].set_ylabel('Spread (bps)')
        axes[1, 1].set_title('Spread vs Volume')
        axes[1, 1].set_yscale('log')
        
        # 6. Cumulative volume distribution
        sorted_volume = df['volume'].sort_values(ascending=False)
        cumulative_volume = sorted_volume.cumsum() / sorted_volume.sum() * 100
        axes[1, 2].plot(range(len(cumulative_volume)), cumulative_volume)
        axes[1, 2].set_xlabel('Contract Rank')
        axes[1, 2].set_ylabel('Cumulative Volume (%)')
        axes[1, 2].set_title('Cumulative Volume Distribution')
        axes[1, 2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Liquidity dashboard saved to {save_path}")
    
    def export_liquidity_tables(self, metrics: Dict, save_path: str) -> None:
        """Export liquidity metrics to CSV tables."""
        logger.info("Exporting liquidity tables")
        
        # Create summary table
        summary_data = []
        
        # Spread metrics
        for metric, value in metrics['spread_metrics'].items():
            if isinstance(value, (int, float)):
                summary_data.append({'metric': metric, 'value': value, 'category': 'spread'})
        
        # Volume metrics
        for metric, value in metrics['volume_metrics'].items():
            if isinstance(value, (int, float)):
                summary_data.append({'metric': metric, 'value': value, 'category': 'volume'})
        
        # Turnover metrics
        for metric, value in metrics['turnover_metrics'].items():
            if isinstance(value, (int, float)):
                summary_data.append({'metric': metric, 'value': value, 'category': 'turnover'})
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(f"{save_path}_summary.csv", index=False)
        
        # Export rankings
        if 'top_underlyings' in metrics['liquidity_rankings']:
            top_underlyings_df = pd.DataFrame(metrics['liquidity_rankings']['top_underlyings']).T
            top_underlyings_df.to_csv(f"{save_path}_top_underlyings.csv")
        
        if 'top_expiries' in metrics['liquidity_rankings']:
            top_expiries_df = pd.DataFrame(metrics['liquidity_rankings']['top_expiries']).T
            top_expiries_df.to_csv(f"{save_path}_top_expiries.csv")
        
        logger.info(f"Liquidity tables exported to {save_path}")
