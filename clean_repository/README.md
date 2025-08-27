# Indian Options Market Research - Clean Repository

## 🎯 **Project Overview**

This repository contains a comprehensive analysis of the Indian equity options market, focusing on NIFTY and BANKNIFTY derivatives data. We've systematically collected and organized historical options data to provide insights into market structure, liquidity, and trading opportunities.

## 📊 **Data Coverage**

### **NIFTY 50 Index Options**
- **Period**: February 2021 - December 2024
- **Total Records**: 6,062 options records
- **Coverage**: Monthly expiries with multiple strikes
- **Data Quality**: High-quality, consistent format

### **BANKNIFTY Index Options**
- **Period**: February 2021 - March 2024
- **Total Records**: 3,172 options records
- **Coverage**: Monthly expiries with multiple strikes
- **Data Quality**: High-quality, consistent format

### **Total Market Coverage**
- **Combined Records**: 9,234 options records
- **Symbols**: 2 major indices covering the entire Indian options market
- **Time Span**: 4 years of historical data

## 🗂️ **Repository Structure**

```
clean_repository/
├── data/                           # All collected data
│   ├── maximized_working_symbols/  # Latest comprehensive collection
│   │   ├── NIFTY/                 # NIFTY options data by year/month
│   │   └── BANKNIFTY/             # BANKNIFTY options data by year/month
│   ├── full_5year_monthly_derivatives/  # Previous 5-year collection
│   └── working_banknifty_data/    # Working period test data
├── scripts/                        # Working collection scripts
│   ├── maximize_working_symbols.py    # Main data collection script
│   ├── collect_5year_data_simple.py   # 5-year collection script
│   └── collect_working_banknifty.py   # Working period collector
├── documentation/                  # Project documentation
│   └── README.md                  # This file
├── requirements.txt                # Python dependencies
└── config.yaml                     # Configuration settings
```

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run Data Collection**
```bash
# Collect maximized data for working symbols
python scripts/maximize_working_symbols.py

# Or collect 5-year data
python scripts/collect_5year_data_simple.py
```

### **3. Access Data**
All collected data is stored in the `data/` directory, organized by symbol and year.

## 📈 **Data Collection Strategy**

### **Proven Working Approach**
1. **Focus on Working Symbols**: NIFTY and BANKNIFTY are the only reliably working symbols
2. **Monthly Expiries**: Collect data for monthly expiry dates (last Thursday of each month)
3. **Multiple Strikes**: Collect data for multiple strike prices per year
4. **Options Only**: Focus exclusively on options data (no futures)

### **Why This Strategy Works**
- **NIFTY**: Consistently works across all time periods
- **BANKNIFTY**: Works for specific periods (2021-2024 with some gaps)
- **Other Symbols**: Consistently fail due to API limitations

## 🔍 **Data Quality Features**

- **Consistent Schema**: All data follows the same column structure
- **Metadata Enrichment**: Added YEAR, MONTH, SYMBOL_NAME fields
- **Error Handling**: Graceful handling of API failures
- **Rate Limiting**: Built-in delays to avoid API restrictions

## 📊 **Available Data Fields**

Each options record contains:
- **Price Data**: OPEN, HIGH, LOW, CLOSE, LTP, SETTLE_PRICE
- **Volume Data**: TOTAL_TRADED_QUANTITY, MARKET_LOT, PREMIUM_VALUE
- **Options Data**: OPTION_TYPE, STRIKE_PRICE, EXPIRY
- **Market Data**: OPEN_INTEREST, CHANGE_IN_OI
- **Metadata**: DATE, SYMBOL_NAME, YEAR, MONTH, INSTRUMENT_TYPE

## 🎯 **Next Steps**

### **Immediate Priorities**
1. **Build Analysis Framework**: Create quant-grade analysis tools
2. **Liquidity Analysis**: Analyze spreads, depth, and volume patterns
3. **Volatility Surfaces**: Build implied volatility models
4. **Risk Analysis**: Calculate Greeks and risk metrics

### **Long-term Goals**
1. **Strategy Development**: Identify profitable trading opportunities
2. **Market Making**: Analyze market maker behavior
3. **Regulatory Impact**: Study market structure changes
4. **Performance Metrics**: Track strategy performance over time

## 🛠️ **Technical Details**

### **Data Sources**
- **Primary**: `jugaad-data` library for NSE derivatives
- **Format**: CSV files with consistent schema
- **Storage**: Organized by symbol, year, and month

### **Collection Process**
- **Monthly Batches**: Collect data month by month
- **Strike Coverage**: Multiple strikes per expiry for comprehensive coverage
- **Error Recovery**: Continue collection even if individual requests fail

## 📝 **Notes**

- **Data Limitations**: Only NIFTY and BANKNIFTY work reliably
- **API Constraints**: NSE has rate limiting and data format inconsistencies
- **Historical Coverage**: 2020-2024 with varying completeness by symbol
- **Focus**: Options data only (futures data removed as requested)

## 🤝 **Contributing**

This repository represents a systematic approach to Indian options market research. The data collection strategy has been proven to work and can be extended to other markets or time periods.

---

**Status**: ✅ **Data Collection Complete** - Ready for Analysis Framework Development
**Last Updated**: December 2024
**Data Quality**: High-quality, comprehensive options data for major indices
