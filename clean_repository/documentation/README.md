# NSE Options Market Research

A clean, organized analysis framework for the Indian National Stock Exchange (NSE) options market.

## 🗂️ Project Structure

```
NSE_Research/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── config.yaml                        # Analysis configuration
├── CHATGPT_ANALYSIS_OUTPUT.txt        # Complete analysis for ChatGPT
├── options_data/                      # Options market data
│   └── op260825.csv                  # August 26, 2025 options data
└── analysis/                          # Analysis framework
    ├── run_analysis.py               # Main analysis runner
    ├── src/                          # Source code modules
    │   ├── __init__.py
    │   ├── data_loader.py           # Data loading and preprocessing
    │   └── liquidity_analysis.py    # Liquidity metrics and analysis
    └── notebooks/                    # Jupyter notebooks for analysis
        └── 01_eda.ipynb             # Exploratory data analysis
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the analysis:**
   ```bash
   cd analysis
   python run_analysis.py
   ```

3. **View results:**
   - Check `CHATGPT_ANALYSIS_OUTPUT.txt` for complete analysis
   - Use the analysis framework in `analysis/` for custom research

## 📊 Data Sources

- **Options Data**: `options_data/op260825.csv` - NSE options market data from August 26, 2025
- **Data Quality**: 96% quality score with 1,919 valid contracts across 395 underlying stocks
- **Volume**: 124.5M contracts with ₹13.76B turnover

## 🎯 Key Features

- **Clean Architecture**: Modular, well-organized code structure
- **Quant-Grade Analysis**: Professional-grade financial analysis tools
- **Reproducible Results**: Deterministic outputs with proper logging
- **Easy Integration**: Simple to use with ChatGPT or other AI tools

## 📈 Analysis Capabilities

- **Liquidity Analysis**: Spread metrics, volume analysis, depth assessment
- **Market Structure**: Concentration analysis, expiry dynamics
- **Risk Assessment**: Comprehensive risk metrics and recommendations
- **Investment Opportunities**: Top liquid stocks and trading strategies

## 🔧 Configuration

Edit `config.yaml` to customize:
- Data file paths
- Analysis parameters
- Fee structures
- Output settings

## 📝 Output

The main analysis output is in `CHATGPT_ANALYSIS_OUTPUT.txt` - a comprehensive report ready to copy/paste into ChatGPT for further analysis and discussion.

## 🧹 Clean Repository

This repository has been cleaned up to remove:
- ❌ All futures-related data and code
- ❌ Duplicate analysis scripts
- ❌ Old reports and outputs
- ❌ Unnecessary files

Only the essential, clean analysis framework remains.

---

*This framework provides a solid foundation for quantitative research on the Indian options market with a clean, professional structure.*
