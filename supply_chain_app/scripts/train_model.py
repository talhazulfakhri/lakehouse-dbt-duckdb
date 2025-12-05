import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# train_model.py
import duckdb
from utils.ml import prepare_training_df_from_duckdb, train_model_from_df
import os

DB_PATH = r"T:/supply-chain-lakehouse/warehouse/supply_chain.duckdb"

def main():
    if not os.path.exists(DB_PATH):
        raise SystemExit(f"DuckDB file not found at {DB_PATH}")

    con = duckdb.connect(DB_PATH)
    print("Connected to DuckDB:", DB_PATH)

    print("Preparing training dataframe (joining fact_sales -> stg_supply_chain)...")
    df = prepare_training_df_from_duckdb(con)
    print("Training dataframe shape:", df.shape)
    print("Label distribution:\n", df["delay_flag"].value_counts().to_dict())

    print("Training model...")
    model = train_model_from_df(df, save=True)
    print("Model trained and saved to models/delay_predictor.pkl")

    con.close()

if __name__ == "__main__":
    main()
