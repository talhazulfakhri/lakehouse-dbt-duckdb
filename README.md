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

# Create a virtual environment
python -m venv .venv

# Activate environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
3️⃣ Ingest Raw Data (Extract & Load)Run the python script to read the CSV and create the DuckDB database.Bashpython scripts/ingest_csv_to_duckdb.py
Result: A supply_chain.duckdb file is created in the warehouse/ folder.4️⃣ Run dbt Models (Transform)Transform the raw data into analytics-ready tables.Bashcd dbt/supply_chain

# Check connection
dbt debug

# Run transformations
dbt run

# (Optional) Generate documentation
dbt docs generate && dbt docs serve
5️⃣ Train the ML ModelTrain the Random Forest classifier on the transformed data.Bash# Return to project root first if needed
cd ../../
python supply_chain_app/scripts/train_model.py
6️⃣ Launch the Dashboard 📊Start the Streamlit app to visualize the data and test the ML model.Bashcd supply_chain_app
streamlit run app.py
