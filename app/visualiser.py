import polars as pl
import matplotlib.pyplot as plt
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

class StockVisualiser:
    """Stock data visualiser using matplotlib"""
    def __init__(self, df: pl.DataFrame):
        """Initialise visualiser with stock data DataFrame."""
        self.df = df.sort(["Ticker", "Date"])
        self.tickers = sorted(self.df["Ticker"].unique())
        colors = ['#1f77b4', '#ff7f0e', '#9467bd', "#f324d7", '#8c564b', "#7ddaff", "#e2ff40", "#13d6b6"]
        self.colors = colors[:len(self.tickers)]
        self.color_map = dict(zip(self.tickers, self.colors))
        logging.info(f"Initialised visualiser with {len(self.df)} rows for tickers: {self.tickers}")
        
    def plot_price_trends(self, figsize: tuple = (10, 5)) -> None:
        """Plot closing price trends for all tickers."""
        logging.info("Creating price trends plot")
        plt.figure(figsize=figsize)
        for ticker in self.tickers:
            ticker_data = self.df.filter(pl.col("Ticker") == ticker)
            plt.plot(ticker_data["Date"], ticker_data["Close"], 
                    label=ticker, linewidth=2, color=self.color_map[ticker])
        
        plt.title("Stock Price Trends")
        plt.xlabel("Date")
        plt.ylabel("Close Price ($)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_volatility(self, window: int = 30, figsize: tuple = (10, 5)) -> None:
        """Plot rolling volatility for all tickers."""
        logging.info(f"Creating {window}-day volatility plot")
        from .analyser import StockAnalyser
        
        analyser = StockAnalyser(self.df)
        vol_data = analyser.calculate_volatility(window).filter(
            pl.col(f"Volatility_{window}d").is_not_null()
        )
        plt.figure(figsize=figsize)
        for ticker in self.tickers:
            ticker_data = vol_data.filter(pl.col("Ticker") == ticker)
            if len(ticker_data) > 0:
                plt.plot(ticker_data["Date"], ticker_data[f"Volatility_{window}d"], 
                        label=ticker, linewidth=2, color=self.color_map[ticker])
        
        plt.title(f"{window}-Day Rolling Volatility")
        plt.xlabel("Date")
        plt.ylabel("Volatility (%)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_returns_distribution(self, figsize: tuple = (10, 5)) -> None:
        """Plot daily returns distribution."""
        logging.info("Creating returns distribution plot")
        from .analyser import StockAnalyser
        
        analyser = StockAnalyser(self.df)
        returns_data = analyser.calculate_returns().filter(
            pl.col("Daily_Return_Pct").is_not_null()
        )
        plt.figure(figsize=figsize)
        for ticker in self.tickers:
            ticker_returns = returns_data.filter(pl.col("Ticker") == ticker)["Daily_Return_Pct"]
            if len(ticker_returns) > 0:
                plt.hist(ticker_returns, bins=50, alpha=0.7, label=ticker, 
                        density=True, color=self.color_map[ticker])
        
        plt.title("Daily Returns Distribution")
        plt.xlabel("Daily Return (%)")
        plt.ylabel("Density")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_volume_trends(self, figsize: tuple = (10, 5)) -> None:
        """Plot volume trends for all tickers."""
        logging.info("Creating volume trends plot")
        plt.figure(figsize=figsize)
        for ticker in self.tickers:
            ticker_data = self.df.filter(pl.col("Ticker") == ticker)
            plt.plot(ticker_data["Date"], ticker_data["Volume"], 
                    label=ticker, alpha=0.7, color=self.color_map[ticker])
        
        plt.title("Trading Volume Trends")
        plt.xlabel("Date")
        plt.ylabel("Volume")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.yscale('log')  # Log scale for better visibility
        plt.tight_layout()
        plt.show()

def create_dashboard(data_path: str) -> None:
    """Create a complete visualisation dashboard."""
    from .data_loader import load_data
    
    try:
        logging.info(f"Starting dashboard creation for: {data_path}")
        df = load_data(data_path)
        visualiser = StockVisualiser(df)
        
        visualiser.plot_price_trends()
        visualiser.plot_volatility()
        visualiser.plot_returns_distribution()
        visualiser.plot_volume_trends()
        
        logging.info("Dashboard creation complete")
        
    except Exception as e:
        logging.error(f"Dashboard creation failed: {e}")
        raise

if __name__ == "__main__":
    create_dashboard("data/sample_data")