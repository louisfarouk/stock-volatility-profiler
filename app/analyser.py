import polars as pl
from typing import Dict
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

class StockAnalyser:
    """Stock analyser using Polars for volatility and performance metrics."""
    
    def __init__(self, df: pl.DataFrame):
        """Initialise analyser with stock data DataFrame"""
        self.df = df.sort(["Ticker", "Date"])
        tickers = self.df["Ticker"].unique().to_list()
        logging.info(f"Initialised analyser with {len(self.df)} rows for tickers: {tickers}")
        
    def calculate_returns(self) -> pl.DataFrame:
        """Calculate daily returns for each stock"""
        return self.df.with_columns([
            (pl.col("Close").pct_change().over("Ticker") * 100).alias("Daily_Return_Pct")
        ])
    
    def calculate_volatility(self, window: int = 30) -> pl.DataFrame:
        """Calculate rolling volatility (standard deviation of returns)"""
        df_with_returns = self.calculate_returns()
        return df_with_returns.with_columns([
            pl.col("Daily_Return_Pct").rolling_std(window, min_periods=window).over("Ticker").alias(f"Volatility_{window}d")
        ])
    
    def get_summary_stats(self) -> pl.DataFrame:
        """Get summary statistics for each ticker"""
        df_with_returns = self.calculate_returns()
        return df_with_returns.group_by("Ticker").agg([
            pl.col("Close").min().alias("Min_Price"),
            pl.col("Close").max().alias("Max_Price"),
            pl.col("Close").mean().alias("Avg_Price"),
            pl.col("Daily_Return_Pct").mean().alias("Avg_Daily_Return"),
            pl.col("Daily_Return_Pct").std().alias("Volatility"),
            pl.col("Volume").mean().alias("Avg_Volume"),
            pl.col("Date").count().alias("Trading_Days")
        ])
    
    def get_price_range_analysis(self) -> pl.DataFrame:
        """Analyse price ranges and movements"""
        return self.df.with_columns([
            ((pl.col("High") - pl.col("Low")) / pl.col("Close") * 100).alias("Daily_Range_Pct"),
            ((pl.col("Close") - pl.col("Open")) / pl.col("Open") * 100).alias("Daily_Change_Pct")
        ]).group_by("Ticker").agg([
            pl.col("Daily_Range_Pct").mean().alias("Avg_Daily_Range_Pct"),
            pl.col("Daily_Change_Pct").mean().alias("Avg_Daily_Change_Pct"),
            pl.col("Daily_Range_Pct").max().alias("Max_Daily_Range_Pct")
        ])
    
    def get_recent_performance(self, days: int = 30) -> pl.DataFrame:
        """Get recent performance metrics"""
        recent_data = self.df.group_by("Ticker").tail(days)
        return recent_data.group_by("Ticker").agg([
            pl.col("Close").first().alias("Start_Price"),
            pl.col("Close").last().alias("End_Price"),
            ((pl.col("Close").last() - pl.col("Close").first()) / pl.col("Close").first() * 100).alias("Period_Return_Pct")
        ])

def analyse_stock_data(data_path: str) -> Dict[str, pl.DataFrame]:
    """Analyse stock data from file or directory"""
    from .data_loader import load_data
    
    try:
        logging.info(f"Starting analysis for: {data_path}")
        df = load_data(data_path)
        analyser = StockAnalyser(df)
        
        logging.info("Calculating summary statistics")
        summary_stats = analyser.get_summary_stats()
        
        logging.info("Calculating volatility analysis")
        volatility_analysis = analyser.calculate_volatility()
        
        logging.info("Calculating price range analysis")
        price_range_analysis = analyser.get_price_range_analysis()
        
        logging.info("Calculating recent performance")
        recent_performance = analyser.get_recent_performance()
        
        results = {
            "summary_stats": summary_stats,
            "volatility_analysis": volatility_analysis,
            "price_range_analysis": price_range_analysis,
            "recent_performance": recent_performance
        }
        logging.info("Analysis complete")
        return results
        
    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        raise

def print_analysis_summary(results: Dict[str, pl.DataFrame]) -> None:
    """Print a formatted summary of analysis results"""
    print("=== STOCK ANALYSIS SUMMARY ===\n")
    
    print("Summary Statistics:")
    print(results["summary_stats"])
    print("\n" + "="*60 + "\n")
    
    print("Price Range Analysis:")
    print(results["price_range_analysis"])
    print("\n" + "="*60 + "\n")
    
    print("Recent Performance (30 days):")
    print(results["recent_performance"])
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    data_path = "data/sample_data"
    try:
        results = analyse_stock_data(data_path)
        print_analysis_summary(results)
    except Exception as e:
        print(f"Error analysing data: {e}")