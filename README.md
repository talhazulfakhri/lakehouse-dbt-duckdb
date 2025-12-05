# 🚚 Supply Chain Lakehouse + ML + AI Dashboard

End-to-end **Data Engineering + Analytics + Machine Learning + AI-ready application** built with:

- **DuckDB** as analytical warehouse
- **dbt** for data transformation & modeling
- **Streamlit** for interactive dashboard
- **Scikit-Learn** for ML prediction
- **Generative AI (Gemini / GPT ready)** for LLM insight layer

This project demonstrates a **modern lakehouse architecture** on a local machine using only **free & open-source tools**.

---

## 🧱 Architecture Overview

Raw CSV (Kaggle)
|
v
Python Ingestion Script
|
v
DuckDB (Raw Layer)
|
v
dbt (Staging → Dimensions → Facts → Mart)
|
v
DuckDB (Analytics Layer)
|
v
Streamlit Dashboard
|
+--> ML Model (Delay Prediction)
|
+--> LLM Insight Layer (Gemini / GPT)

yaml
Copy code

---

## 📁 Project Structure

supply-chain-lakehouse/
│
├─ data/
│ └─ raw_supply_chain.csv
│
├─ warehouse/
│ └─ supply_chain.duckdb
│
├─ scripts/
│ ├─ ingest_csv_to_duckdb.py
│ ├─ inspect_duckdb.py
│ └─ train_model.py
│
├─ dbt/
│ └─ supply_chain/
│ ├─ models/
│ │ ├─ staging/
│ │ ├─ dimensions/
│ │ ├─ facts/
│ │ └─ marts/
│ └─ dbt_project.yml
│
├─ supply_chain_app/
│ ├─ app.py
│ ├─ utils/
│ │ ├─ ml.py
│ │ └─ charts.py
│ ├─ models/
│ │ └─ delay_predictor.pkl
│ └─ requirements.txt
│
└─ README.md

yaml
Copy code

---

## 🧪 Dataset

Source: **Kaggle – Supply Chain Dataset (Cosmetics & Logistics)**  
Total records: **100 rows**

Main raw columns:
- Product category, SKU, price
- Sales volume & revenue
- Supplier & city
- Shipping cost & time
- Manufacturing cost & defect rate

---

## ⚙️ Tech Stack

| Layer | Tool |
|------|------|
| Storage | DuckDB |
| Transformation | dbt |
| Orchestration | Python Scripts |
| Visualization | Streamlit + Plotly |
| Machine Learning | Scikit-Learn |
| AI | Gemini / GPT ready |
| Language | Python |

---

## 🚀 How to Run From Scratch

### 1️⃣ Clone This Repo

```bash
git clone https://github.com/yourusername/supply-chain-lakehouse.git
cd supply-chain-lakehouse
2️⃣ Create Virtual Environment
bash
Copy code
python -m venv .venv
. .venv\Scripts\activate
pip install -r supply_chain_app/requirements.txt
3️⃣ Ingest Raw CSV → DuckDB
bash
Copy code
python scripts/ingest_csv_to_duckdb.py
This creates:

bash
Copy code
warehouse/supply_chain.duckdb
With table:

raw_supply_chain

4️⃣ Run dbt Transformation
bash
Copy code
cd dbt/supply_chain
dbt debug
dbt run
This will generate:

stg_supply_chain

dim_product

fact_sales

mart_supply_chain_performance

📊 Analytics Layer (DuckDB)
Generated tables:

Table	Description
raw_supply_chain	Raw ingested data
stg_supply_chain	Cleaned standardized data
dim_product	Product dimension
fact_sales	Sales fact table
mart_supply_chain_performance	Aggregated KPIs

🤖 Machine Learning – Delay Prediction
Training
bash
Copy code
python supply_chain_app/scripts/train_model.py
Features:

supplier_lead_time_days

defect_rate

shipping_cost

Target:

delay_flag (auto-generated from shipping_time_days)

Model:

RandomForestClassifier

Saved output:

bash
Copy code
supply_chain_app/models/delay_predictor.pkl
📈 Streamlit Dashboard
Run App
bash
Copy code
cd supply_chain_app
streamlit run app.py
Dashboard includes:

✅ Sales KPIs
✅ Product performance
✅ Defect & manufacturing analysis
✅ ML Delay Prediction (real-time)
✅ Interactive filtering
✅ AI-ready chat analytics (Gemini / GPT)

🧠 AI Layer (LLM Ready)
The app architecture supports:

Invoice / logistics document extraction

Natural language query on structured data

AI-generated insights over KPIs

Gemini / GPT API can be plugged easily via:

swift
Copy code
utils/ai.py (optional extension)
📌 What This Project Demonstrates
✅ End-to-end Data Engineering Pipeline

✅ Modern Lakehouse architecture

✅ dbt modeling (staging → dim → fact → mart)

✅ DuckDB as embedded analytical warehouse

✅ Production-ready ML pipeline

✅ Business-oriented dashboard

✅ AI-first analytics foundation
