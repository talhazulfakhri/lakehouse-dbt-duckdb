# 🚚 Supply Chain Lakehouse: End-to-End DE, ML & AI Project

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![DuckDB](https://img.shields.io/badge/Storage-DuckDB-yellow)
![dbt](https://img.shields.io/badge/Transformation-dbt-orange)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Status](https://img.shields.io/badge/Status-Active-success)

**A modern Data Lakehouse architecture built on a local machine using 100% open-source tools.**

This project demonstrates an end-to-end data pipeline that ingests raw supply chain data, transforms it using dbt, stores it in DuckDB, predicts delivery delays using Machine Learning, and visualizes insights via an interactive Streamlit dashboard equipped with LLM capabilities.

---

## 🧱 Architecture Overview

The pipeline follows a "Modern Data Stack" approach tailored for local development:

```mermaid
graph LR
    A[Raw CSV Data] -->|Python Script| B[(DuckDB Raw Layer)]
    B -->|dbt Core| C[Staging, Dims & Facts]
    C -->|dbt Core| D[Data Marts]
    D -->|Query| E[Streamlit Dashboard]
    D -->|Training Data| F[Scikit-Learn Model]
    F -->|Predictions| E
    G[Gemini/GPT API] -.->|Insights| E


## 📂 Project StructurePlaintextsupply-chain-lakehouse/
│
├── data/                       # Raw input data
│   └── raw_supply_chain.csv
│
├── warehouse/                  # OLAP Database file
│   └── supply_chain.duckdb
│
├── scripts/                    # ETL & Training Scripts
│   ├── ingest_csv_to_duckdb.py
│   ├── inspect_duckdb.py
│   └── train_model.py
│
├── dbt/                        # dbt Transformation Project
│   └── supply_chain/
│       ├── models/
│       │   ├── staging/        # Cleaned data
│       │   ├── dimensions/     # Dimension tables (Product, etc)
│       │   ├── facts/          # Fact tables (Sales)
│       │   └── marts/          # Aggregated tables for BI
│       └── dbt_project.yml
│
├── supply_chain_app/           # Dashboard Application
│   ├── app.py
│   ├── utils/
│   │   ├── ml.py
│   │   └── charts.py
│   ├── models/                 # Serialized ML Models
│   │   └── delay_predictor.pkl
│   └── requirements.txt
│
└── README.md
🧪 DatasetThe project uses the Supply Chain Dataset (Cosmetics & Logistics) sourced from Kaggle.Records: ~100 rows (Simulated data)Key Features: Product SKU, Price, Lead times, Shipping costs, Defect rates, Routes, and Carrier details.🚀 Getting StartedFollow these steps to run the project from scratch.1️⃣ Clone the RepositoryBashgit clone [https://github.com/talhazulfakhri/lakehouse-dbt-duckdb.git](https://github.com/talhazulfakhri/lakehouse-dbt-duckdb.git)
cd supply-chain-lakehouse
2️⃣ Environment SetupCreate a virtual environment to keep dependencies clean.Bashpython -m venv .venv
# Activate: Windows
.venv\Scripts\activate
# Activate: Mac/Linux
source .venv/bin/activate

# Install dependencies
pip install -r supply_chain_app/requirements.txt
3️⃣ Ingest Data (ETL)Load the raw CSV into the DuckDB raw layer.Bashpython scripts/ingest_csv_to_duckdb.py
Output: Creates warehouse/supply_chain.duckdb populated with raw_supply_chain.4️⃣ Run dbt TransformationsClean, model, and aggregate the data.Bashcd dbt/supply_chain
dbt deps
dbt run
Output: Generates stg_supply_chain, dim_product, fact_sales, and mart_supply_chain_performance.5️⃣ Train Machine Learning ModelTrain a Random Forest Classifier to predict shipping delays.Bash# Go back to root if inside dbt folder
cd ../../
python scripts/train_model.py
Features: supplier_lead_time, defect_rate, shipping_costTarget: delay_flag (Derived from shipping days)Output: Saves model to supply_chain_app/models/delay_predictor.pkl6️⃣ Launch the DashboardStart the Streamlit app to visualize the data.Bashcd supply_chain_app
streamlit run app.py
📊 Analytics & InsightsThe Dashboard provides three main layers of value:Business Intelligence (BI):Sales KPIs & Revenue analysis.Defect rate vs. Manufacturing cost correlation.Top performing products and routes.Predictive Analytics (ML):Real-time prediction of shipment delays based on lead time and carrier performance.Generative AI (Ready):Architecture supports plugging in OpenAI/Gemini API to query the DuckDB warehouse using Natural Language.
