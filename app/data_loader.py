import polars as pl
from pathlib import Path
from typing import Union
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

def load_stock_data(file_path: Union[str, Path]) -> pl.DataFrame:
    """
    Load stock data from a yfinance CSV file into a Polars DataFrame.
    
    Args:
        file_path: Path to the CSV file containing stock data
        
    Returns:
        Polars DataFrame with cleaned stock data
    """
    logging.info(f"Loading stock data from {file_path}")
    raw_df = pl.read_csv(file_path, has_header=False)
    ticker = raw_df[1, 1]
    logging.info(f"Processing ticker: {ticker}")
    price_headers = list(raw_df.row(0)[1:])
    headers = ["Date"] + price_headers
    
    df = pl.read_csv(
        file_path,
        has_header=False,
        skip_rows=3,
        new_columns=headers,
        try_parse_dates=True
    )

    numeric_cols = ["Close", "High", "Low", "Open", "Volume"]
    for col in numeric_cols:
        if col in df.columns:
            df = df.with_columns(pl.col(col).cast(pl.Float64))
    
    df = df.with_columns(pl.lit(ticker).alias("Ticker"))
    logging.info(f"Loaded {len(df)} rows for {ticker}")
    
    return df

def load_data(path: Union[str, Path]) -> pl.DataFrame:
    """
    Load stock data from a single file or all files in a folder.
    
    Args:
        path: File path or folder path containing stock data
        
    Returns:
        Polars DataFrame with stock data (combined if folder)
    """
    path = Path(path)
    logging.info(f"Loading data from path: {path}")
    
    if path.is_file():
        logging.info("Processing single file")
        return load_stock_data(path)
    
    if path.is_dir():
        logging.info("Processing directory")
        stock_files = list(path.glob("*_stock_data.csv"))
        if not stock_files:
            raise FileNotFoundError(f"No stock data files found in {path}")
        
        logging.info(f"Found {len(stock_files)} stock data files")
        dfs = [load_stock_data(f) for f in stock_files]
        combined_df = pl.concat(dfs, how="vertical").sort(["Ticker", "Date"])
        logging.info(f"Combined data: {len(combined_df)} total rows")
        return combined_df
    
    raise FileNotFoundError(f"Path not found: {path}")