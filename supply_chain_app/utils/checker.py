from utils.duckdb_conn import get_conn

def check_pipeline():
    con = get_conn()

    checks = {}

    required_tables = [
        "raw_supply_chain",
        "stg_supply_chain",
        "dim_product",
        "fact_sales",
        "mart_supply_chain_performance",
    ]

    for table in required_tables:
        try:
            con.execute(f"SELECT 1 FROM {table} LIMIT 1")
            checks[table] = "OK"
        except:
            checks[table] = "❌ MISSING"

    return checks
