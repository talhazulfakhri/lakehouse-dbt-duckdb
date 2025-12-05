import shutil, datetime, pathlib, sys

SRC = pathlib.Path("T:\supply-chain-lakehouse\data_raw\supply_chain_data.csv")
DST_DIR = pathlib.Path("storage/bronze")
DST_DIR.mkdir(parents=True, exist_ok=True)


ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
dst = DST_DIR / f"supply_chain_raw__{ts}.csv"
shutil.copy(SRC, dst)
print(f"Copied {SRC} -> {dst}")