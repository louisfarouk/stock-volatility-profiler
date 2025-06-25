import polars as pl
from pathlib import Path
from typing import Union
### ADD LOGGING

def load_stock_data(file_path: Union[str, Path]) -> pl.DataFrame:
    """
    Load stock data from a yfinance CSV file into a Polars DataFrame.
    
    Args:
        file_path: Path to the CSV file containing stock data
        
    Returns:
        Polars DataFrame with cleaned stock data
    """
    raw_df = pl.read_csv(file_path, has_header=False)
    ticker = raw_df[1, 1]
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
    
    return df