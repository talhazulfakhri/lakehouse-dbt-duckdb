🚚 Supply Chain Intelligence LakehouseA full-stack "Modern Data Stack in a Box" demonstrating an end-to-end pipeline from raw CSV ingestion to Machine Learning predictions and GenAI insights, running entirely locally.📖 Executive SummaryThis project establishes a local Data Lakehouse to analyze supply chain performance. It moves beyond simple analysis by implementing engineering best practices: ELT pipelines, dimensional modeling, predictive analytics, and an AI-powered interface.Key Capabilities:Data Engineering: Ingests raw logistics data into a DuckDB warehouse using Python.Analytics Engineering: Uses dbt (data build tool) to transform raw data into a Star Schema (Facts & Dimensions).Machine Learning: Predicts shipping delays using a Random Forest model trained on historical logistics data.GenAI Integration: A foundation for LLM-driven insights (Gemini/GPT) allows users to "chat" with their supply chain data.🧱 ArchitectureThis project follows the Medallion Architecture (Bronze $\to$ Silver $\to$ Gold) adapted for a lightweight local stack.Code snippetgraph LR
 graph LR
    A[Raw CSV Data] -->|Python Ingestion| B[(DuckDB: Raw Layer)]
    B -->|dbt: Staging| C(Staging Views)
    C -->|dbt: Modeling| D[Dimensions & Facts]
    D -->|dbt: Aggregation| E[Data Marts]
    E -->|Read| F[Streamlit Dashboard]
    F -->|Interacts| G[ML Model: Delay Prediction]
    F -->|Interacts| H[LLM Insight Layer]
    
🛠 Tech StackComponentToolWhy this tool?Storage & ComputeDuckDBLightning-fast, serverless OLAP database optimized for analytics.Transformationdbt CoreIndustry standard for modular SQL, testing, and lineage.OrchestrationPythonCustom scripts for ingestion and ML pipeline management.VisualizationStreamlitRapid frontend development for data apps.Machine LearningScikit-LearnRobust library for training the delay prediction classifier.AI LayerGemini / GPTLarge Language Model integration for unstructured data querying.📂 Project StructureBashsupply-chain-lakehouse/
│
├── 📁 data/                  # Source data storage
│   └── raw_supply_chain.csv
│
├── 📁 warehouse/             # The embedded analytical database
│   └── supply_chain.duckdb
│
├── 📁 dbt/                   # dbt project root
│   └── supply_chain/
│       ├── models/
│       │   ├── staging/      # Cleaned raw data (1:1 with source)
│       │   ├── dimensions/   # Context (Product, Location)
│       │   ├── facts/        # Measurements (Sales, Shipping)
│       │   └── marts/        # Aggregated KPIs for the dashboard
│       └── dbt_project.yml
│
├── 📁 scripts/               # ETL & Utility scripts
│   ├── ingest_csv_to_duckdb.py
│   └── inspect_duckdb.py
│
├── 📁 supply_chain_app/      # Streamlit Application
│   ├── app.py                # Main entry point
│   ├── models/               # Serialized ML models (.pkl)
│   ├── utils/                # Helper functions for UI/ML/AI
│   └── scripts/              # ML Training scripts
│
└── requirements.txt          # Python dependencies
🧪 The Data Model (Deep Dive)We utilize dbt to transform raw chaotic data into a clean Star Schema.Staging Layer (stg_supply_chain):Renames columns to snake_case.Casts data types (Strings to Float/Int).Handles null values.Dimension Tables:dim_product: Contains SKU, category, price, and supplier metadata.dim_location: Contains shipping routes and routes.Fact Table:fact_sales: Contains transactional data, revenue, shipping costs, and defect rates.Mart Layer (mart_supply_chain_performance):Pre-aggregated table joining Facts and Dimensions.Calculates key metrics like Total Revenue, Avg Shipping Time, and Defect Ratios.🤖 Machine Learning: Delay PredictionThe application includes a supervised learning model to identify potential supply chain risks.Problem: Binary Classification (Will the shipment be delayed?)Target: delay_flag (Derived from shipping days vs. lead time).Features Used:supplier_lead_time_daysdefect_rateshipping_costproduct_categoryAlgorithm: Random Forest Classifier (Scikit-Learn).Output: The model is pickled (delay_predictor.pkl) and loaded into Streamlit for real-time inference on new data.🚀 Installation & SetupFollow these steps to build the lakehouse from scratch on your local machine.1️⃣ PrerequisitesPython 3.9+Git2️⃣ Clone & Configure EnvironmentBashgit clone https://github.com/yourusername/supply-chain-lakehouse.git
cd supply-chain-lakehouse

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
