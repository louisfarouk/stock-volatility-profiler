import yfinance as yf
import logging
import argparse
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)


def fetch_stock_data(ticker: str, start: str, end: str, save_path: Path):
    """
    Fetch stock data from Yahoo Finance and saves it to a CSV file.

    ticker: Stock ticker symbol (e.g., 'AAPL' for Apple Inc.)
    start: Start date in 'YYYY-MM-DD' format
    end: End date in 'YYYY-MM-DD' format
    save_path: Path where the CSV file will be saved
    """
    logging.info(f"Fetching data for {ticker} from {start} to {end}")
    try:
        stock_data = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
        if stock_data.empty:
            logging.error(f"No data found for {ticker} - skipping")
            return
        
        save_path.parent.mkdir(parents=True, exist_ok=True)
        stock_data.to_csv(save_path)
        logging.info(f"Saved {ticker} data to {save_path}")
        
    except Exception as e:
        logging.error(f"Failed to fetch data for {ticker} - skipping")
        
    
def main():
    parser = argparse.ArgumentParser(description='Fetch stock data from Yahoo Finance')
    parser.add_argument('--ticker', '-t', type=str, help='Stock ticker symbol (e.g., AAPL, GOOGL)')
    parser.add_argument('--start', '-s', type=str, default='2020-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', '-e', type=str, default='2024-01-01', help='End date (YYYY-MM-DD)')
    parser.add_argument('--output-dir', '-o', type=str, default='custom', help='Output directory within data/')
    
    args = parser.parse_args()
    
    if args.ticker:
        # User-sought data
        output_path = Path("data") / args.output_dir / f"{args.ticker.lower()}_stock_data.csv"
        fetch_stock_data(
            ticker=args.ticker,
            start=args.start,
            end=args.end,
            save_path=output_path
        )
    else:
        # Default sample data
        logging.info("No ticker specified. Fetching sample data...")
        fetch_stock_data(
            ticker='AAPL',
            start='2020-01-01',
            end='2024-01-01',
            save_path=Path('data/sample_data/aapl_stock_data.csv')
        )
        fetch_stock_data(
            ticker='GOOGL',
            start='2020-01-01',
            end='2024-01-01',
            save_path=Path('data/sample_data/googl_stock_data.csv')
        )
        fetch_stock_data(
            ticker='HSBA.L',
            start='2020-01-01',
            end='2024-01-01',
            save_path=Path('data/sample_data/hsba.l_stock_data.csv')
        )

if __name__ == "__main__":
    main()