# Stock Volatility Profiler
Swift stock analysis using Polars (soon)

## Setup

### Prerequisites
- Python 3.8 or higher

### Installation
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

## Usage

### Fetching Stock Data

Default sample data for AAPL, GOOGL, and HSBA.L is available in `data/sample_data/`.

Fetch data for any ticker with command-line arguments:

```bash
# Basic usage w/ custom ticker
python scripts/fetch_stock_data.py --ticker MSFT

# Fully customised
python scripts/fetch_stock_data.py --ticker NVDA --start 2023-01-01 --end 2024-01-01 --output-dir data/my_stocks

# Short form
python scripts/fetch_stock_data.py -t AMZN -s 2022-01-01 -e 2023-12-31 -o data/tech_stocks
```

#### Command-Line Options
```
-t, --ticker      Stock ticker symbol (e.g., AAPL, GOOGL)
-s, --start       Start date in YYYY-MM-DD format (default: 2020-01-01)
-e, --end         End date in YYYY-MM-DD format (default: 2024-01-01)
-o, --output-dir  Output directory (default: data/custom)
```

## Project Structure
```
stock-volatility-profiler/
├── data/
│   ├── sample_data/    # Pre-configured sample data
│   └── custom/         # User-requested custom data
├── scripts/
│   └── fetch_stock_data.py
├── requirements.txt
└── README.md
```

## Data Format
Downloaded stock data includes:
- Date
- Open, High, Low, Close prices
- Adjusted Close price
- Volume

## Dependencies
- **yfinance**: Yahoo Finance data fetching
