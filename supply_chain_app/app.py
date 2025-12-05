import streamlit as st
import pandas as pd
from utils.duckdb_conn import load_table
from utils.charts import supplier_defect_chart, lead_time_chart, shipping_cost_chart
from utils.ml import load_model, train_model, predict_delay
from utils.llm import supply_chain_insight
from utils.checker import check_pipeline

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="Supply Chain AI Platform", layout="wide")

st.sidebar.title("🔗 Supply Chain AI Platform")
tab = st.sidebar.radio("Navigate", 
    ["Dashboard", "ML Prediction", "LLM Insight", "Query Explorer", "Pipeline Checker"]
)

# GEMINI API
api_key = st.sidebar.text_input("Gemini API Key", type="password")


# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------
# -------------------------
# DASHBOARD (replace existing Dashboard block)
# -------------------------
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

if tab == "Dashboard":
    st.title("🚀 Supply Chain Command Center")
    st.markdown("### Monitor Performance, Logistics, and Inventory Risks")

    from utils.duckdb_conn import get_conn
    con = get_conn()

    # 1. DATA LOADING
    # Kita join Mart (Aggregates) dengan Staging (Dimensions) untuk fleksibilitas
    sql_query = """
    WITH data AS (
        SELECT 
            m.product_id,
            s.product_category,
            s.supplier_name,
            s.supplier_city,
            s.transport_mode,
            s.shipping_carrier,
            s.route,
            -- Metrics
            COALESCE(m.total_revenue, 0) as total_revenue,
            COALESCE(m.total_sold, 0) as total_sold,
            COALESCE(m.avg_defect_rate, s.defect_rate, 0) as defect_rate,
            COALESCE(s.stock_level, 0) as stock_level,
            COALESCE(s.shipping_cost, 0) as shipping_cost,
            COALESCE(s.shipping_time_days, s.supplier_lead_time_days, 0) as lead_time,
            COALESCE(m.avg_mfg_lead_time, 0) as mfg_lead_time
        FROM mart_supply_chain_performance m
        LEFT JOIN stg_supply_chain s ON m.product_id = s.product_id
    )
    SELECT * FROM data
    WHERE total_revenue > 0 -- Filter noise
    ORDER BY total_revenue DESC
    """

    try:
        df = con.execute(sql_query).fetchdf()
    except Exception as e:
        st.error(f"❌ Database Error: {e}")
        st.stop()

    if df.empty:
        st.warning("No data available.")
        st.stop()

    # 2. SIDEBAR FILTERS (Interactive)
    with st.sidebar:
        st.header("🔍 Filters")
        
        # Filter Category
        all_cats = df['product_category'].unique().tolist()
        sel_cats = st.multiselect("Product Category", all_cats, default=all_cats[:2])
        
        # Filter Transport Mode
        all_modes = df['transport_mode'].unique().tolist()
        sel_modes = st.multiselect("Transport Mode", all_modes, default=all_modes)

        # Apply Filters
        if sel_cats:
            df = df[df['product_category'].isin(sel_cats)]
        if sel_modes:
            df = df[df['transport_mode'].isin(sel_modes)]

    # 3. TOP LEVEL METRICS
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    total_rev = df['total_revenue'].sum()
    avg_defect = df['defect_rate'].mean()
    avg_ship_cost = df['shipping_cost'].mean()
    avg_lead = df['lead_time'].mean()

    col1.metric("💰 Total Revenue", f"Rp {total_rev:,.0f}", help="Total revenue from selected segments")
    col2.metric("⚠️ Avg Defect Rate", f"{avg_defect:.2f}%", delta_color="inverse", delta=f"{avg_defect-2:.2f}% (vs Target)")
    col3.metric("🚚 Avg Shipping Cost", f"${avg_ship_cost:.2f}", delta_color="inverse")
    col4.metric("⏱️ Avg Lead Time", f"{avg_lead:.1f} Days")

    st.markdown("---")

    # 4. DASHBOARD TABS
    tab_overview, tab_logistics, tab_inventory = st.tabs(["📊 Overview & Sales", "🚢 Logistics & Cost", "📦 Inventory & Risk"])

    # --- TAB 1: OVERVIEW ---
    with tab_overview:
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.subheader("Revenue by Product Category")
            # Treemap sangat bagus untuk melihat proporsi kategori -> supplier
            fig_tree = px.treemap(df, 
                                  path=[px.Constant("All"), 'product_category', 'supplier_name'], 
                                  values='total_revenue',
                                  color='defect_rate',
                                  color_continuous_scale='RdYlGn_r',
                                  title="Revenue Breakdown (Color = Defect Rate Risk)")
            st.plotly_chart(fig_tree, use_container_width=True)
            
        with c2:
            st.subheader("Top Suppliers by Revenue")
            top_sup = df.groupby('supplier_name')['total_revenue'].sum().nlargest(10).reset_index()
            fig_bar = px.bar(top_sup, x='total_revenue', y='supplier_name', orientation='h', color='total_revenue', title="Leaderboard")
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- TAB 2: LOGISTICS ---
    with tab_logistics:
        st.subheader("Shipping Efficiency Analysis")
        st.caption("Insight: Identify carriers that are expensive AND slow (Top Left Quadrant is bad).")
        
        c_log1, c_log2 = st.columns([2, 1])
        
        with c_log1:
            # Scatter Plot: Cost vs Time (The most important logic metric)
            fig_scatter = px.scatter(df, 
                                     x="lead_time", 
                                     y="shipping_cost", 
                                     size="total_sold", 
                                     color="transport_mode",
                                     hover_data=['shipping_carrier', 'product_category'],
                                     title="Correlation: Shipping Cost vs. Lead Time",
                                     labels={"lead_time": "Delivery Time (Days)", "shipping_cost": "Cost per Unit"})
            # Add average lines
            fig_scatter.add_vline(x=df['lead_time'].mean(), line_dash="dash", line_color="gray")
            fig_scatter.add_hline(y=df['shipping_cost'].mean(), line_dash="dash", line_color="gray")
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with c_log2:
            st.markdown("#### Carrier Performance")
            # Compare Carrier Costs
            carrier_perf = df.groupby('shipping_carrier')[['shipping_cost', 'lead_time']].mean().reset_index()
            fig_carrier = px.bar(carrier_perf, x='shipping_carrier', y='shipping_cost', 
                                 color='lead_time', title="Avg Cost by Carrier",
                                 labels={'lead_time': 'Avg Days'})
            st.plotly_chart(fig_carrier, use_container_width=True)

    # --- TAB 3: INVENTORY & RISK ---
    with tab_inventory:
        c_inv1, c_inv2 = st.columns(2)
        
        with c_inv1:
            st.subheader("🚨 Stockout Risk Monitor")
            st.caption("Products with High Sales Velocity but Low Stock.")
            
            # Logic: Ratio Sold vs Stock
            df['turnover_risk'] = df['total_sold'] / (df['stock_level'] + 1)
            risk_df = df.sort_values('turnover_risk', ascending=False).head(10)
            
            st.dataframe(
                risk_df[['product_id', 'product_category', 'stock_level', 'total_sold', 'turnover_risk']],
                column_config={
                    "turnover_risk": st.column_config.ProgressColumn("Risk Score", format="%.1f", min_value=0, max_value=risk_df['turnover_risk'].max())
                },
                use_container_width=True
            )
            
        with c_inv2:
            st.subheader("Quality Control: Defect Analysis")
            # Histogram defect rate
            fig_hist = px.histogram(df, x="defect_rate", nbins=20, color="product_category", 
                                    title="Distribution of Defect Rates",
                                    marginal="box") # Adds a boxplot on top
            st.plotly_chart(fig_hist, use_container_width=True)

    # Data Source Checkbox
    with st.expander("Show Raw Aggregated Data"):
        st.dataframe(df)


# ---------------------------------------------------
# ML PREDICTION
# ---------------------------------------------------
if tab == "ML Prediction":
    st.header("🤖 Supplier Delay Prediction")

    df = load_table("fact_sales")

    try:
        model = load_model()
        st.success("Model loaded.")
    except:
        st.warning("Model not found, training now...")
        model = train_model(df)
        st.success("Model trained.")

    # Input row selector
    row = df.sample(1).iloc[0]
    st.write("Selected Data Point:", row)

    prob = predict_delay(model, row)
    st.metric("Delay Probability", f"{prob*100:.2f}%")


# ---------------------------------------------------
# LLM INSIGHT
# ---------------------------------------------------
if tab == "LLM Insight":
    st.header("🧠 AI Supply Chain Analyst")

    if not api_key:
        st.info("Insert Gemini API key first")
    else:
        df = load_table("mart_supply_chain_performance")

        query = st.text_area("Ask anything about your supply chain:")
        if st.button("Ask Gemini"):
            with st.spinner("Analyzing..."):
                ans = supply_chain_insight(df, query, api_key)
                st.write(ans)


# ---------------------------------------------------
# QUERY EXPLORER
# ---------------------------------------------------
if tab == "Query Explorer":
    st.header("💻 SQL Query Explorer (DuckDB)")

    df = None
    query = st.text_area("SQL Query", "SELECT * FROM fact_sales LIMIT 10")
    if st.button("Run"):
        df = load_table("(" + query + ")")

    if df is not None:
        st.dataframe(df)


# ---------------------------------------------------
# PIPELINE CHECKER
# ---------------------------------------------------
if tab == "Pipeline Checker":
    st.header("🧪 Pipeline Health Check")

    checks = check_pipeline()
    for table, status in checks.items():
        st.write(f"{table}: {status}")
