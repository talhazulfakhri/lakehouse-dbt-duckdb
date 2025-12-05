import plotly.express as px
import pandas as pd

def supplier_defect_chart(df):
    if 'supplier_name' not in df.columns or 'defect_rate' not in df.columns:
        available = ", ".join(df.columns.tolist())
        fig = px.bar(pd.DataFrame({'note': [f'Columns missing. Available: {available}']}), x='note', y=[0])
        fig.update_layout(title="Supplier Defect Rate (cannot render — missing columns)")
        return fig

    return px.bar(
        df,
        x="supplier_name",
        y="defect_rate",
        title="Supplier Defect Rate",
        color="defect_rate",
    )

def lead_time_chart(df):
    y_col = None
    for candidate in ['supplier_lead_time_days', 'lead_time_meta', 'lead_time']:
        if candidate in df.columns:
            y_col = candidate
            break
    if y_col is None or 'supplier_name' not in df.columns:
        available = ", ".join(df.columns.tolist())
        fig = px.box(pd.DataFrame({'note': [f'Columns missing. Available: {available}']}), x='note', y=[0])
        fig.update_layout(title="Lead Time Distribution (cannot render — missing columns)")
        return fig

    return px.box(
        df,
        x="supplier_name",
        y=y_col,
        title="Supplier Lead Time Distribution"
    )

def shipping_cost_chart(df):
    cost_col = None
    for candidate in ['shipping_cost', 'transport_costs', 'shipping_costs']:
        if candidate in df.columns:
            cost_col = candidate
            break
    if cost_col is None:
        available = ", ".join(df.columns.tolist())
        fig = px.histogram(pd.DataFrame({'note': [f'Columns missing. Available: {available}']}), x='note')
        fig.update_layout(title="Shipping Cost Distribution (cannot render — missing columns)")
        return fig

    return px.histogram(
        df,
        x=cost_col,
        nbins=40,
        title="Shipping Cost Distribution"
    )
