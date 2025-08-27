"""
Data loading and validation for NSE options analysis.
Handles schema mapping, data quality checks, and preprocessing.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NSEDataLoader:
    """Loads and validates NSE options data with schema mapping."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.random_seed = config['analysis']['random_seed']
        np.random.seed(self.random_seed)
        
        # Schema mapping for NSE data
        self.schema_mapping = {
            'CONTRACT_D': 'symbol',
            'PREVIOUS_S': 'prev_close',
            'OPEN_PRICE': 'open',
            'HIGH_PRICE': 'high',
            'LOW_PRICE': 'low',
            'CLOSE_PRIC': 'close',
            'SETTLEMENT': 'settlement',
            'NET_CHANGE': 'net_change',
            'OI_NO_CON': 'open_interest',
            'TRADED_QUA': 'volume',
            'TRD_NO_CON': 'trades',
            'UNDRLNG_ST': 'underlying_price',
            'NOTIONAL_V': 'notional_value',
            'PREMIUM_TR': 'premium_traded'
        }
        
    def load_options_data(self, file_path: str) -> pd.DataFrame:
        """Load and preprocess NSE options data."""
        logger.info(f"Loading options data from {file_path}")
        
        try:
            # Load raw data
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} raw records")
            
            # Rename columns using schema mapping
            df = df.rename(columns=self.schema_mapping)
            
            # Extract option details from symbol
            df = self._extract_option_details(df)
            
            # Clean and validate data
            df = self._clean_data(df)
            
            # Add derived fields
            df = self._add_derived_fields(df)
            
            logger.info(f"Final dataset: {len(df)} valid records")
            return df
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def _extract_option_details(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract option details from contract description."""
        logger.info("Extracting option details from contract descriptions")
        
        # Initialize new columns
        df['underlying'] = None
        df['expiry'] = None
        df['strike'] = None
        df['option_type'] = None
        
        for idx, contract in enumerate(df['symbol']):
            if pd.notna(contract):
                try:
                    # Pattern: OPTSTKSTOCKNAME-DATE-STRIKEPRICE-CE/PE
                    parts = contract.split('-')
                    
                    if len(parts) >= 3:
                        # Extract underlying stock
                        if 'OPTSTK' in parts[0]:
                            df.loc[idx, 'underlying'] = parts[0].replace('OPTSTK', '')
                        
                        # Extract expiry
                        if len(parts) >= 2:
                            df.loc[idx, 'expiry'] = parts[1]
                        
                        # Extract strike and option type from last part
                        for part in parts[2:]:
                            if 'CE' in part:
                                strike = part.replace('CE', '')
                                df.loc[idx, 'strike'] = float(strike)
                                df.loc[idx, 'option_type'] = 'CE'
                                break
                            elif 'PE' in part:
                                strike = part.replace('PE', '')
                                df.loc[idx, 'strike'] = float(strike)
                                df.loc[idx, 'option_type'] = 'PE'
                                break
                                
                except Exception as e:
                    logger.debug(f"Could not parse contract {contract}: {e}")
                    continue
        
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate the data."""
        logger.info("Cleaning and validating data")
        
        # Remove rows with missing critical fields
        critical_fields = ['open', 'close', 'underlying', 'option_type']
        df = df.dropna(subset=critical_fields)
        
        # Convert price columns to numeric
        price_cols = ['open', 'high', 'low', 'close', 'settlement', 'prev_close']
        for col in price_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert volume and other numeric fields
        numeric_cols = ['volume', 'trades', 'open_interest', 'strike', 'underlying_price']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove invalid prices (negative or zero)
        df = df[df['close'] > 0]
        df = df[df['open'] > 0]
        
        # Remove invalid volumes
        df = df[df['volume'] > 0]
        
        # Calculate and filter by spread
        df['spread_bps'] = ((df['high'] - df['low']) / df['close']) * 10000
        df = df[df['spread_bps'] <= self.config['analysis']['liquidity']['max_spread_bps']]
        
        return df
    
    def _add_derived_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived fields for analysis."""
        logger.info("Adding derived fields")
        
        # Calculate returns
        df['return'] = (df['close'] - df['prev_close']) / df['prev_close']
        
        # Calculate moneyness (approximate)
        if 'underlying_price' in df.columns and 'strike' in df.columns:
            df['moneyness'] = df['underlying_price'] / df['strike']
        
        # Calculate time to expiry (approximate from expiry string)
        df['days_to_expiry'] = self._calculate_days_to_expiry(df['expiry'])
        
        # Calculate implied volatility (placeholder - will be computed separately)
        df['implied_volatility'] = np.nan
        
        # Add date fields
        df['date'] = pd.Timestamp.now().date()  # Placeholder - extract from data if available
        
        return df
    
    def _calculate_days_to_expiry(self, expiry_series: pd.Series) -> pd.Series:
        """Calculate days to expiry from expiry string."""
        try:
            # Convert expiry strings to dates and calculate days
            current_date = pd.Timestamp.now()
            expiry_dates = pd.to_datetime(expiry_series, format='%d-%b-%Y', errors='coerce')
            days_to_expiry = (expiry_dates - current_date).dt.days
            
            # Replace negative values with 0 (expired options)
            days_to_expiry = days_to_expiry.clip(lower=0)
            
            return days_to_expiry
        except Exception as e:
            logger.warning(f"Could not calculate days to expiry: {e}")
            return pd.Series([np.nan] * len(expiry_series))
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict:
        """Perform data quality validation and return report."""
        logger.info("Validating data quality")
        
        validation_report = {
            'total_records': len(df),
            'missing_data': {},
            'data_issues': [],
            'quality_score': 0.0
        }
        
        # Check for missing data
        for col in df.columns:
            missing_pct = df[col].isna().sum() / len(df) * 100
            validation_report['missing_data'][col] = missing_pct
        
        # Check for data issues
        issues = []
        
        # Check for negative prices
        if 'close' in df.columns:
            negative_prices = (df['close'] < 0).sum()
            if negative_prices > 0:
                issues.append(f"Found {negative_prices} negative prices")
        
        # Check for zero volumes
        if 'volume' in df.columns:
            zero_volumes = (df['volume'] == 0).sum()
            if zero_volumes > 0:
                issues.append(f"Found {zero_volumes} zero volumes")
        
        # Check for duplicate symbols
        duplicates = df['symbol'].duplicated().sum()
        if duplicates > 0:
            issues.append(f"Found {duplicates} duplicate symbols")
        
        validation_report['data_issues'] = issues
        
        # Calculate quality score
        missing_score = 1 - np.mean(list(validation_report['missing_data'].values())) / 100
        issue_score = 1 - (len(issues) / 10)  # Penalize for issues
        validation_report['quality_score'] = max(0, (missing_score + issue_score) / 2)
        
        logger.info(f"Data quality score: {validation_report['quality_score']:.2f}")
        return validation_report
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict:
        """Generate comprehensive data summary."""
        logger.info("Generating data summary")
        
        summary = {
            'overview': {
                'total_records': len(df),
                'unique_underlyings': df['underlying'].nunique(),
                'unique_expiries': df['expiry'].nunique(),
                'date_range': f"{df['date'].min()} to {df['date'].max()}" if 'date' in df.columns else "Unknown"
            },
            'options_distribution': {
                'call_options': len(df[df['option_type'] == 'CE']),
                'put_options': len(df[df['option_type'] == 'PE']),
                'call_put_ratio': len(df[df['option_type'] == 'CE']) / len(df[df['option_type'] == 'PE'])
            },
            'volume_analysis': {
                'total_volume': df['volume'].sum(),
                'total_turnover': df['notional_value'].sum() if 'notional_value' in df.columns else np.nan,
                'avg_volume_per_contract': df['volume'].mean(),
                'top_underlyings': df.groupby('underlying')['volume'].sum().nlargest(5).to_dict()
            },
            'price_analysis': {
                'price_range': {
                    'min': df['close'].min(),
                    'max': df['close'].max(),
                    'mean': df['close'].mean(),
                    'median': df['close'].median()
                },
                'strike_range': {
                    'min': df['strike'].min(),
                    'max': df['strike'].max(),
                    'mean': df['strike'].mean()
                } if 'strike' in df.columns else None
            }
        }
        
        return summary
