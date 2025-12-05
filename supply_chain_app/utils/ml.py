import pickle
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

MODELPATH = os.path.join("models", "delay_predictor.pkl")
FEATURES = ["supplier_lead_time_days", "defect_rate", "shipping_cost"]

def ensure_models_dir():
    os.makedirs("models", exist_ok=True)

def train_model_from_df(df, save=True):
    if "delay_flag" not in df.columns:
        raise ValueError("train_model_from_df requires 'delay_flag' column")

    X = df[FEATURES].fillna(0)
    y = df["delay_flag"].astype(int)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    if save:
        ensure_models_dir()
        with open(MODELPATH, "wb") as f:
            pickle.dump(model, f)

    return model

def load_model():
    if not os.path.exists(MODELPATH):
        raise FileNotFoundError(f"Model file missing: {MODELPATH}")
    with open(MODELPATH, "rb") as f:
        return pickle.load(f)

def _get_value_from_row(row_like, key, fallbacks=None):
    if fallbacks is None:
        fallbacks = []

    if hasattr(row_like, "to_dict"):
        data = row_like.to_dict()
    elif isinstance(row_like, dict):
        data = row_like
    else:
        try:
            data = dict(row_like)
        except:
            data = {}

    # 1. Exact match
    if key in data:
        return data[key]

    # 2. Fallback list
    for fb in fallbacks:
        if fb in data:
            return data[fb]

    # 3. Case insensitive
    key_lower = key.lower()
    for k in data:
        if str(k).lower() == key_lower:
            return data[k]

    # 4. Remove underscores / spaces
    norm = key_lower.replace("_", "").replace(" ", "")
    for k in data:
        if str(k).lower().replace("_", "").replace(" ", "") == norm:
            return data[k]

    # 5. Smart alias mapping
    alt = {
        "supplier_lead_time_days": ["lead_time_meta", "supplier_lead_time"],
        "defect_rate": ["defect_rates", "avg_defect_rate"],
        "shipping_cost": ["transport_cost", "transport_costs", "shipping_costs"]
    }

    for alias in alt.get(key, []):
        if alias in data:
            return data[alias]
        for k in data:
            if str(k).lower() == alias.lower():
                return data[k]

    return 0

def predict_delay(model, row):
    if isinstance(row, pd.DataFrame):
        row = row.iloc[0]

    vals = []
    for feat in FEATURES:
        v = _get_value_from_row(row, feat)
        try:
            vals.append(float(v))
        except:
            vals.append(0.0)

    X = np.array(vals, dtype=float).reshape(1, -1)

    if hasattr(model, "predict_proba"):
        return float(model.predict_proba(X)[0][1])
    return float(model.predict(X)[0])

def prepare_training_df_from_duckdb(con):
    sql = """
    SELECT
      f.product_id,
      f.quantity_sold,
      f.revenue,
      COALESCE(ss.supplier_lead_time_days, 0) AS supplier_lead_time_days,
      COALESCE(ss.defect_rate, 0) AS defect_rate,
      COALESCE(ss.shipping_cost, ss.transport_cost, 0) AS shipping_cost,
      COALESCE(ss.shipping_time_days, 0) AS shipping_time_days
    FROM fact_sales f
    LEFT JOIN stg_supply_chain ss
      ON f.product_id = ss.product_id
    WHERE ss.supplier_name IS NOT NULL
    """

    df = con.execute(sql).fetchdf()
    if df.empty:
        raise ValueError("No training data returned — check joins.")

    median_time = float(df["shipping_time_days"].median())
    threshold = max(1.0, median_time)

    df["delay_flag"] = (df["shipping_time_days"] > threshold).astype(int)

    for col in FEATURES + ["delay_flag"]:
        if col not in df:
            df[col] = 0

    return df[FEATURES + ["delay_flag"]]

def train_model(df_or_con):
    if hasattr(df_or_con, "execute"):
        df = prepare_training_df_from_duckdb(df_or_con)
        return train_model_from_df(df)
    return train_model_from_df(df_or_con)
