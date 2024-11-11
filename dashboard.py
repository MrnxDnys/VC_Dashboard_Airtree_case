import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Set page config
st.set_page_config(
    page_title="VC Portfolio Dashboard",
    page_icon="💼",
    layout="wide"
)

# Add custom CSS for better spacing
st.markdown("""
    <style>
    .main > div {
        padding-top: 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sample data - in production, this would come from a database
@st.cache_data
def load_data():
    # Portfolio companies data
    companies_data = pd.DataFrame({
        'Company': ['Company ' + str(i) for i in range(1, 29)],
        'Stage': np.random.choice(['Seed', 'Series A', 'Series B', 'Series C+'], 28),
        'Investment_Date': pd.date_range(start='1/1/2020', periods=28, freq='M'),
        'Investment_Amount': np.random.randint(1000000, 10000000, 28),
        'Current_Value': np.random.randint(2000000, 20000000, 28),
        'Sector': np.random.choice(['FinTech', 'HealthTech', 'AI/ML', 'Enterprise', 'Consumer'], 28)
    })
    
    # Historical valuations data
    valuations_data = pd.DataFrame({
        'Date': pd.date_range(start='1/1/2020', periods=48, freq='M'),
        'Portfolio_Value': np.linspace(100000000, 420000000, 48) + np.random.normal(0, 10000000, 48)
    })
    
    return companies_data, valuations_data

# Load data
companies_df, valuations_df = load_data()

# Header
st.title("Airtree Portfolio Performance Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
selected_sector = st.sidebar.multiselect(
    "Sector",
    options=companies_df['Sector'].unique(),
    default=companies_df['Sector'].unique()
)

selected_stage = st.sidebar.multiselect(
    "Stage",
    options=companies_df['Stage'].unique(),
    default=companies_df['Stage'].unique()
)

# Filter data
filtered_companies = companies_df[
    (companies_df['Sector'].isin(selected_sector)) &
    (companies_df['Stage'].isin(selected_stage))
]

# Top metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    tvpi = filtered_companies['Current_Value'].sum() / filtered_companies['Investment_Amount'].sum()
    st.metric("TVPI", f"{tvpi:.2f}x")

with col2:
    irr = 25.5  # This would normally be calculated based on cash flows
    st.metric("IRR", f"{irr:.1f}%")

with col3:
    total_value = filtered_companies['Current_Value'].sum()
    st.metric("Total Portfolio Value", f"${total_value/1e6:.1f}M")

with col4:
    st.metric("Active Companies", len(filtered_companies))

# Charts row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Portfolio Value Growth")
    fig = px.line(valuations_df, x='Date', y='Portfolio_Value',
                  title=None)
    fig.update_layout(yaxis_title="Value ($)", xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Investment by Stage")
    stage_data = filtered_companies.groupby('Stage')['Investment_Amount'].sum().reset_index()
    fig = px.bar(stage_data, x='Stage', y='Investment_Amount',
                 title=None)
    fig.update_layout(yaxis_title="Total Investment ($)", xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

# Charts row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sector Distribution")
    sector_data = filtered_companies.groupby('Sector')['Current_Value'].sum()
    fig = px.pie(values=sector_data.values, names=sector_data.index,
                 title=None)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Investment vs Current Value by Stage")
    compare_data = filtered_companies.groupby('Stage').agg({
        'Investment_Amount': 'sum',
        'Current_Value': 'sum'
    }).reset_index()
    
    fig = go.Figure(data=[
        go.Bar(name='Investment Amount', x=compare_data['Stage'], y=compare_data['Investment_Amount']),
        go.Bar(name='Current Value', x=compare_data['Stage'], y=compare_data['Current_Value'])
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig, use_container_width=True)

# Portfolio companies table
st.subheader("Portfolio Companies")
st.dataframe(
    filtered_companies.style.format({
        'Investment_Amount': '${:,.0f}',
        'Current_Value': '${:,.0f}'
    }),
    hide_index=True
)

# Footer with key metrics
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("DPI", "0.8x")
with col2:
    st.metric("RVPI", "2.0x")
with col3:
    st.metric("Avg Hold Period", "2.4 years")