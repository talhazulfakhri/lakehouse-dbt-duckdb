import duckdb
import json
import os

# Menggunakan r'' untuk path Windows, dijamin aman dari masalah escape character
p = r'T:/supply-chain-lakehouse/warehouse/supply_chain.duckdb'

def safe_print(title, obj):
    print(f'--- {title} ---')
    if isinstance(obj, list):
        for r in obj:
            print(r)
    else:
        print(obj)
    print()

# 0) Cek keberadaan file database
if not os.path.exists(p):
    print('ERROR: duckdb file not found at', p)
    raise SystemExit(1)

# Hubungkan ke database
con = duckdb.connect(p)

# 1) list all tables (schema + table)
# PERBAIKAN UTAMA: Double quotes yang hilang telah ditambahkan di akhir string query
tables = con.execute("SELECT table_schema, table_name FROM information_schema.tables ORDER BY table_schema, table_name").fetchall()
safe_print('ALL_TABLES (schema.table)', ["{}.{}".format(r[0], r[1]) for r in tables])

# 2) For each table, list columns
for schema, table in tables:
    try:
        # Menggunakan f-string di sini sudah benar
        cols = con.execute(f"PRAGMA table_info('{schema}.{table}')").fetchall()
        # PRAGMA table_info returns (cid,name,type,notnull,default_value,pk) in DuckDB
        col_names = [c[1] for c in cols]
        safe_print(f'COLS: {schema}.{table}', col_names)
    except Exception as e:
        # fallback: select * limit 0
        try:
            df = con.execute(f"SELECT * FROM {schema}.{table} LIMIT 0").fetchdf()
            safe_print(f'COLS (fallback): {schema}.{table}', df.columns.tolist())
        except Exception as e2:
            safe_print(f'ERROR reading columns for {schema}.{table}', str(e2))

# 3) show a tiny sample (3 rows) for each relevant table to inspect types/content
relevant = ['raw_supply_chain','stg_supply_chain','fact_sales','dim_product','dim_supplier','mart_supply_chain_performance']
for t in relevant:
    try:
        # find schema for this table
        # Menggunakan format string dengan aman
        res = con.execute("SELECT table_schema FROM information_schema.tables WHERE table_name = '{}' LIMIT 1".format(t)).fetchone()
        if res:
            schema = res[0]
            # Menggunakan f-string untuk query SELECT *
            sample = con.execute(f"SELECT * FROM {schema}.{t} LIMIT 3").fetchdf()
            safe_print(f'SAMPLE: {schema}.{t}', sample.to_dict(orient='records'))
        else:
            safe_print(f'SAMPLE: {t}', 'TABLE NOT FOUND')
    except Exception as e:
        safe_print(f'SAMPLE ERROR: {t}', str(e))

con.close()