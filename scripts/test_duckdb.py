import duckdb

con = duckdb.connect("T:/supply-chain-lakehouse/warehouse/supply_chain.duckdb")

print("TABLES IN THIS DB FILE:")
print(con.execute("SHOW TABLES").fetchall())   # <- SIMPLE, NO FAILURE

print("\nIF raw_supply_chain EXISTS, SAMPLE ROWS:")
try:
    print(con.execute("SELECT * FROM raw_supply_chain LIMIT 5").fetchdf())
except Exception as e:
    print("ERROR:", e)

con.close()
