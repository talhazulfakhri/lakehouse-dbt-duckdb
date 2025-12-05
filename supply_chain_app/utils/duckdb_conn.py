import duckdb

def get_conn():
    return duckdb.connect("T:/supply-chain-lakehouse/warehouse/supply_chain.duckdb")

def load_table(table_name: str):
    con = get_conn()
    return con.execute(f"SELECT * FROM {table_name}").fetchdf()
