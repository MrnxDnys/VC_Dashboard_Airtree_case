import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Set page config
st.set_page_config(
    page_title="Who Gives A Crap - Portfolio Company Dashboard",
    page_icon="🧻",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
    }
    .small-font {
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Sample data generation functions
def generate_monthly_data(start_date, periods, initial_value, growth_rate, volatility):
    dates = pd.date_range(start_date, periods=periods, freq='M')
    values = [initial_value]
    for i in range(1, periods):
        next_value = values[-1] * (1 + growth_rate + np.random.normal(0, volatility))
        values.append(next_value)
    return pd.DataFrame({'Date': dates, 'Value': values})

def generate_quarterly_metrics():
    quarters = pd.date_range('2022-01-01', periods=8, freq='Q')
    return pd.DataFrame({
        'Quarter': quarters,
        'Revenue': np.linspace(15000000, 45000000, 8) + np.random.normal(0, 1000000, 8),
        'Gross_Margin': np.linspace(65, 72, 8) + np.random.normal(0, 1, 8),
        'CAC': np.linspace(40, 35, 8) + np.random.normal(0, 2, 8),
        'LTV': np.linspace(120, 150, 8) + np.random.normal(0, 5, 8),
        'Active_Subscribers': np.linspace(200000, 450000, 8) + np.random.normal(0, 10000, 8),
        'Churn_Rate': np.linspace(3.5, 2.8, 8) + np.random.normal(0, 0.2, 8)
    })

# Generate sample data
metrics_df = generate_quarterly_metrics()
arr_data = generate_monthly_data('2022-01-01', 24, 35000000, 0.04, 0.02)
customer_data = generate_monthly_data('2022-01-01', 24, 200000, 0.035, 0.01)

# Header
st.title("Who Gives A Crap - Portfolio Company Dashboard")
st.markdown("Last Updated: " + datetime.now().strftime("%Y-%m-%d"))

# Company Overview
with st.expander("Company Overview", expanded=True):
    col1, col2, col3 = st.columns([2,1,1])
    
    with col1:
        st.markdown("""
        **Investment Thesis**: Sustainable toilet paper and household products company 
        disrupting the traditional paper products market through D2C subscription model 
        and strong environmental impact mission.
        
        **Investment Details**:
        - Initial Investment: Series B - $12M (2022)
        - Ownership: 15%
        - Board Seat: Yes
        - Last Valuation: $280M (2023)
        """)
    
    with col2:
        st.markdown("""
        **Key Strengths**:
        - Strong brand loyalty
        - 100% recycled products
        - High subscription retention
        - International expansion
        """)
    
    with col3:
        st.markdown("""
        **Focus Areas**:
        - US market penetration
        - Product line expansion
        - Supply chain optimization
        - B2B channel growth
        """)

# Key Metrics
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

latest_metrics = metrics_df.iloc[-1]
prev_metrics = metrics_df.iloc[-2]

with col1:
    arr = latest_metrics['Revenue'] * 4  # Annualized
    arr_growth = (arr / (prev_metrics['Revenue'] * 4) - 1) * 100
    st.metric("ARR", f"${arr/1e6:.1f}M", f"{arr_growth:.1f}%")

with col2:
    gm_change = latest_metrics['Gross_Margin'] - prev_metrics['Gross_Margin']
    st.metric("Gross Margin", f"{latest_metrics['Gross_Margin']:.1f}%", f"{gm_change:.1f}%")

with col3:
    ltv_cac = latest_metrics['LTV'] / latest_metrics['CAC']
    prev_ltv_cac = prev_metrics['LTV'] / prev_metrics['CAC']
    ltv_cac_change = (ltv_cac / prev_ltv_cac - 1) * 100
    st.metric("LTV/CAC", f"{ltv_cac:.1f}x", f"{ltv_cac_change:.1f}%")

with col4:
    churn_change = latest_metrics['Churn_Rate'] - prev_metrics['Churn_Rate']
    st.metric("Monthly Churn", f"{latest_metrics['Churn_Rate']:.1f}%", f"{churn_change:.1f}%")

# Growth Metrics
st.subheader("Growth Metrics")
col1, col2 = st.columns(2)

with col1:
    fig = px.line(arr_data, x='Date', y='Value', title="Monthly Recurring Revenue")
    fig.update_layout(yaxis_title="Revenue ($)", xaxis_title="")
    fig.update_yaxes(tickformat='$,.0f')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.line(customer_data, x='Date', y='Value', title="Active Subscribers")
    fig.update_layout(yaxis_title="Subscribers", xaxis_title="")
    fig.update_yaxes(tickformat=',')
    st.plotly_chart(fig, use_container_width=True)

# Detailed Metrics Table
st.subheader("Quarterly Performance")
detailed_metrics = metrics_df.copy()
detailed_metrics['Quarter'] = detailed_metrics['Quarter'].dt.strftime('%Y Q%q')
detailed_metrics = detailed_metrics.round(2)
st.dataframe(
    detailed_metrics.style.format({
        'Revenue': '${:,.0f}',
        'Gross_Margin': '{:.1f}%',
        'CAC': '${:.2f}',
        'LTV': '${:.2f}',
        'Active_Subscribers': '{:,.0f}',
        'Churn_Rate': '{:.2f}%'
    }),
    hide_index=True
)

# Impact Metrics
st.subheader("Impact Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Trees Saved (YTD)", "2.8M", "12%")
    
with col2:
    st.metric("Water Saved (Gallons)", "850K", "8%")
    
with col3:
    st.metric("Plastic Packaging Avoided", "450K lbs", "15%")

# Risk Assessment
st.subheader("Risk Assessment")
risks = pd.DataFrame({
    'Risk Category': ['Supply Chain', 'Competition', 'Customer Acquisition', 'Regulatory'],
    'Risk Level': ['Medium', 'Low', 'Low', 'Low'],
    'Mitigation Strategy': [
        'Diversifying supplier base, increasing inventory holdings',
        'Strong brand moat, patent-pending sustainable packaging',
        'High LTV justifies current CAC, strong referral program',
        'Proactive compliance with environmental regulations'
    ]
})
st.table(risks)

# Key Updates
st.subheader("Recent Updates")
updates = """
- **Product**: Launched new bamboo paper line with 15% higher margins
- **Markets**: Entered Canada with strong initial traction
- **Team**: Hired new COO from P&G
- **Operations**: New warehouse in Texas reducing delivery times by 40%
"""
st.markdown(updates)

# Next Steps
st.subheader("Next Steps & Focus Areas")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Q3 2024 Objectives**
    - Launch enterprise/B2B sales channel
    - Complete ERP system implementation
    - Expand retail presence to 1,000 stores
    - Achieve 500K active subscribers
    """)

with col2:
    st.markdown("""
    **Support Required**
    - Strategic partnership introductions
    - B2B sales strategy consultation
    - Review of international expansion plan
    - Board member recruitment
    """)