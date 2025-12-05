# scripts/bronze_to_duckdb.py
import duckdb, pandas as pd, pathlib, datetime, re

BRONZE = pathlib.Path("storage/bronze")
files = sorted(BRONZE.glob("supply_chain_raw__*.csv"))
if not files:
    raise SystemExit("No bronze files found. Run ingest first.")
LATEST = files[-1]
print("Loading:", LATEST)

# try common separators: comma, tab, whitespace
def try_read(path):
    for sep in [",","\t", r'\s+']:
        try:
            if sep == r'\s+':
                df = pd.read_csv(path, sep=r'\s+', engine='python', header=None)
            else:
                df = pd.read_csv(path, sep=sep)
            return df
        except Exception:
            continue
    raise SystemExit("Failed to read CSV with common separators.")

df = try_read(LATEST)

# if header missing (we expect 24 cols), set column names
cols = ["product_category","sku","price","availability","number_of_products_sold","revenue_generated",
        "customer_demographics","stock_levels","supplier_lead_time_days","order_quantities","shipping_times",
        "shipping_carrier","shipping_costs","supplier_name","supplier_city","lead_time_meta",
        "production_volumes","manufacturing_lead_time","manufacturing_costs","inspection_results",
        "defect_rates","transportation_modes","routes","transport_costs"]
if df.shape[1] == len(cols):
    df.columns = cols
else:
    # try if first row is header
    print("Detected column count:", df.shape[1], "expected", len(cols))
    if df.shape[1] > len(cols):
        # keep first len(cols)
        df = df.iloc[:, :len(cols)]
        df.columns = cols
    else:
        raise SystemExit("Unexpected column count; adjust code to match CSV layout.")

# basic cleaning
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['revenue_generated'] = pd.to_numeric(df['revenue_generated'], errors='coerce')
df['number_of_products_sold'] = pd.to_numeric(df['number_of_products_sold'], errors='coerce', downcast='integer')
df['stock_levels'] = pd.to_numeric(df['stock_levels'], errors='coerce', downcast='integer')
df['supplier_lead_time_days'] = pd.to_numeric(df['supplier_lead_time_days'], errors='coerce', downcast='integer')
df['shipping_times'] = pd.to_numeric(df['shipping_times'], errors='coerce', downcast='integer')
df['shipping_costs'] = pd.to_numeric(df['shipping_costs'], errors='coerce')
df['production_volumes'] = pd.to_numeric(df['production_volumes'], errors='coerce', downcast='integer')
df['manufacturing_lead_time'] = pd.to_numeric(df['manufacturing_lead_time'], errors='coerce', downcast='integer')
df['manufacturing_costs'] = pd.to_numeric(df['manufacturing_costs'], errors='coerce')
df['defect_rates'] = pd.to_numeric(df['defect_rates'], errors='coerce')

df['inspection_results'] = df['inspection_results'].str.lower().replace({'pending':'pending','pass':'pass','fail':'fail'})
df['customer_demographics'] = df['customer_demographics'].fillna('unknown').str.lower()

df['ingest_ts'] = datetime.datetime.utcnow()
df['source_file'] = str(LATEST.name)

# write to DuckDB
con = duckdb.connect(database='warehouse/supply_chain.duckdb', read_only=False)
# create table if not exists and append
con.execute("CREATE TABLE IF NOT EXISTS raw_supply_chain AS SELECT * FROM df WHERE 1=0")
con.append('raw_supply_chain', df)
con.commit()
print("Wrote", len(df), "rows to raw_supply_chain in warehouse/supply_chain.duckdb")
con.close()
