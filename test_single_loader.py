from app.data_loader import load_stock_data
from pathlib import Path

file_path = Path("data/sample_data/aapl_stock_data.csv")
df = load_stock_data(file_path)

print(f"DataFrame shape: {df.shape}")
print(f"DataFrame columns: {df.columns}")

print("\nFirst 10 rows:")
print(df.head(10))