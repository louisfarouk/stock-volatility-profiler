<div align="center">

# Stock Volatility Profiler

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![yfinance](https://img.shields.io/badge/yfinance-0.2.63-orange.svg)](https://github.com/ranaroussi/yfinance)
[![Polars](https://img.shields.io/badge/Polars-1.31.0-green.svg)](https://github.com/pola-rs/polars)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

*Swift stock analysis using Polars*

</div>

## 📊 Features
- ⚡ **Fast Analysis**: Polars-powered data processing
- 📈 **Comprehensive Metrics**: Volatility, returns, price ranges, performance
- 🎯 **Rich Visualisations**: Price trends, volatility charts, returns distribution
- ⚙️ **Flexible Input**: Single files or entire directories

## 🔧 Installation
1. **Clone the repository**
   ```bash 
   git clone https://github.com/louisfarouk/stock-volatility-profiler.git
   cd stock-volatility-profiler
   ```

2. **Create and activate a virtual environment**
   ```bash 
   python -m venv venv
   source venv/Scripts/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Stock Analysis & Visualisation

Run analysis and visualisation using stock_volatility_profiler.py:

```bash
# Analyze stock data
python stock_volatility_profiler.py analyse sample_data

# Create visualisations
python stock_volatility_profiler.py visualise sample_data

# Both analysis and visualisation
python stock_volatility_profiler.py both sample_data

# Single file analysis
python stock_volatility_profiler.py analyse sample_data/aapl_stock_data.csv
```

#### Commands
- `analyse` - Generate summary statistics, volatility metrics, and performance analysis
- `visualise` - Create price trends, volatility, returns distribution, and volume charts
- `both` - Run both analysis and visualization

### Fetching Stock Data

Default sample data for AAPL, GOOGL, and HSBA.L is available in `data/sample_data/`.

Fetch data for any ticker with command-line arguments:

```bash
# Basic usage w/ custom ticker
python scripts/fetch_stock_data.py --ticker MSFT

# Fully customised
python scripts/fetch_stock_data.py --ticker NVDA --start 2023-01-01 --end 2024-01-01 --output-dir my_stocks
```

#### Command-Line Options
```
-t, --ticker      Stock ticker symbol (e.g., AAPL, GOOGL)
-s, --start       Start date in YYYY-MM-DD format (default: 2020-01-01)
-e, --end         End date in YYYY-MM-DD format (default: 2024-01-01)
-o, --output-dir  Output directory within data/ (default: custom)
```

## 📁 Project Structure
```
stock-volatility-profiler/
├── app/
│   ├── data_loader.py            # Data loading
│   ├── analyser.py               # Stock analysis
│   └── visualiser.py             # Visualisation
├── data/
│   ├── sample_data/              # Pre-configured sample data
│   └── custom/                   # User-requested custom data
├── scripts/
│   └── fetch_stock_data.py
├── stock_volatility_profiler.py  # Main application
├── requirements.txt
└── README.md
```

## 🔍 Data Format

### Input Data
- Date
- Open, High, Low, Close prices
- Volume
- Ticker symbol

### Analysis Output
- **Summary Statistics**: Min/Max/Average prices, volatility, trading volume
- **Volatility Analysis**: Rolling volatility calculations
- **Price Range Analysis**: Daily price ranges and movements
- **Performance Metrics**: Period returns and price changes

## 📋 Dependencies
- [**yfinance**](https://github.com/ranaroussi/yfinance): Yahoo Finance data fetching
- [**Polars**](https://github.com/pola-rs/polars): Super-fast DataFrames
- [**matplotlib**](https://matplotlib.org/): Plotting and visualisation

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Disclaimer**: This project is not affiliated with Yahoo, Inc. Stock data is retrieved using the yfinance library for research and educational purposes. Please refer to Yahoo's terms of use for data usage rights.
