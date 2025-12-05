import duckdb

con = duckdb.connect(r"T:/supply-chain-lakehouse/warehouse/supply_chain.duckdb")

print("=== TABLES IN DB ===")
print(con.execute("SELECT table_schema, table_name FROM information_schema.tables").fetchdf())

print("\n=== SHOW ALL TABLES ===")
print(con.execute("SHOW ALL TABLES").fetchdf())

con.close()
