import sys
import argparse
from pathlib import Path
import logging
from app.data_loader import load_data
from app.analyser import analyse_stock_data, print_analysis_summary
from app.visualiser import StockVisualiser

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

def main():
    parser = argparse.ArgumentParser(description="Stock Volatility Profiler")
    parser.add_argument("command", choices=["analyse", "visualise", "both"], 
                       help="Command to run")
    parser.add_argument("path", help="Path to stock data file or directory in data/")
    
    args = parser.parse_args()
    logging.info(f"Starting Stock Volatility Profiler - Command: {args.command}, Path: {args.path}")
    data_path = Path("data") / args.path
    
    if not data_path.exists():
        logging.error(f"Path '{args.path}' does not exist!")
        return 1
    
    try:
        logging.info(f"Loading data from: {args.path}")
        if args.command in ["analyse", "both"]:
            logging.info("Starting analysis")
            results = analyse_stock_data(str(data_path))
            print_analysis_summary(results)
        
        if args.command in ["visualise", "both"]:
            logging.info("Starting visualisation")
            df = load_data(str(data_path))
            visualiser = StockVisualiser(df)
            visualiser.plot_price_trends()
            visualiser.plot_volatility()
            visualiser.plot_returns_distribution()
            visualiser.plot_volume_trends()
            logging.info("Visualisation complete")
        
        logging.info("Application completed successfully")
        return 0
        
    except Exception as e:
        logging.error(f"Application failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())