import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="ForecastIQ | Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for Glassmorphism & Dark Theme ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');
    
    :root {
        --primary: #4F46E5;
        --secondary: #0ea5e9;
        --bg-dark: #050505;
        --surface: #111111;
    }
    
    .stApp {
        background-color: var(--bg-dark);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, .outfit {
        font-family: 'Outfit', sans-serif;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        font-family: 'Outfit', sans-serif;
    }
    
    .kpi-label {
        font-size: 0.8rem;
        color: #94a3b8;
    }
    
    .trend-up {
        color: #4ade80;
        font-weight: 700;
        font-size: 0.8rem;
    }
    
    .trend-down {
        color: #f87171;
        font-weight: 700;
        font-size: 0.8rem;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #111 !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #4F46E5, #0ea5e9);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- Logic & Data Generation ---

def generate_dummy_forecast(days=30):
    dates = pd.date_range(start=datetime.now(), periods=days)
    base_value = 10000
    values = []
    for _ in range(days):
        base_value += np.random.normal(500, 1500)
        values.append(max(0, round(base_value, 2)))
    return pd.DataFrame({"Date": dates, "Revenue": values})

def get_kpi_data(days=30):
    modifier = days / 30.0
    return {
        "Total Revenue": {"value": f"${2.4 * modifier:.1f}M", "trend": "+12.5%", "status": "up"},
        "Forecasted (30d)": {"value": f"${2.8 * modifier:.1f}M", "trend": "+16.2%", "status": "up"},
        "Demand Index": {"value": "84/100", "trend": "+5.1%", "status": "up"},
        "Inventory Health": {"value": "92%", "trend": "-2.0%", "status": "down"},
        "Active Stores": {"value": "124", "trend": "+4", "status": "up"},
        "Profit Margin": {"value": "32.4%", "trend": "+1.2%", "status": "up"}
    }

# --- Sidebar Navigation ---
st.sidebar.markdown(f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 2rem;">
        <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #4F46E5, #0ea5e9); border-radius: 8px; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-weight: bold;">📊</span>
        </div>
        <span style="font-size: 1.25rem; font-weight: bold; color: white;">Forecast<span style="color: #4F46E5;">IQ</span></span>
    </div>
""", unsafe_allow_html=True)

menu = ["Dashboard", "Forecasting Engine", "Analytics", "Inventory Intelligence", "Settings"]
choice = st.sidebar.radio("Main Menu", menu)

# --- Dashboard View ---
if choice == "Dashboard":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h1 style='margin-bottom: 0;'>Executive Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8;'>Real-time enterprise overview & predictive intelligence.</p>", unsafe_allow_html=True)
    with col2:
        days_choice = st.selectbox("Timeframe", ["Last 30 Days", "Q3 2026", "Year to Date"], index=0)
        days_map = {"Last 30 Days": 30, "Q3 2026": 90, "Year to Date": 365}
        days = days_map[days_choice]

    # Insights Row
    st.markdown("### AI Insights")
    i_col1, i_col2, i_col3, i_col4 = st.columns(4)
    insights = [
        {"cat": "Demand", "text": "Demand expected to increase by 18% next month.", "color": "#4ade80"},
        {"cat": "Inventory", "text": "Shortage risk detected for 'Wireless Earbuds'.", "color": "#f87171"},
        {"cat": "Sales", "text": "Electronics driving 22% YoY growth.", "color": "#4F46E5"},
        {"cat": "Customers", "text": "Retention improved by 4.2% recently.", "color": "#4ade80"}
    ]
    for i, col in enumerate([i_col1, i_col2, i_col3, i_col4]):
        with col:
            st.markdown(f"""
                <div class="glass-card" style="height: 100px; border-left: 4px solid {insights[i]['color']};">
                    <div style="font-size: 0.7rem; font-weight: bold; color: #64748b; text-transform: uppercase;">{insights[i]['cat']}</div>
                    <div style="font-size: 0.85rem; font-weight: 500; margin-top: 5px;">{insights[i]['text']}</div>
                </div>
            """, unsafe_allow_html=True)

    # KPI Row
    st.markdown("---")
    kpis = get_kpi_data(days)
    k_cols = st.columns(6)
    for i, (label, data) in enumerate(kpis.items()):
        with k_cols[i]:
            trend_class = "trend-up" if data["status"] == "up" else "trend-down"
            st.markdown(f"""
                <div class="glass-card">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{data['value']}</div>
                    <div class="{trend_class}">{data['trend']}</div>
                </div>
            """, unsafe_allow_html=True)

    # Charts Row
    st.markdown("### Revenue & Demand Analysis")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        df = generate_dummy_forecast(days)
        # Split into historical and predicted
        mid = len(df) // 2
        hist_df = df.iloc[:mid+1].copy()
        pred_df = df.iloc[mid:].copy()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist_df["Date"], y=hist_df["Revenue"], name="Historical", 
                                line=dict(color='#0ea5e9', width=3), fill='tozeroy', 
                                fillcolor='rgba(14, 165, 233, 0.1)'))
        fig.add_trace(go.Scatter(x=pred_df["Date"], y=pred_df["Revenue"], name="Predicted", 
                                line=dict(color='#4F46E5', width=3, dash='dash'), fill='tozeroy',
                                fillcolor='rgba(79, 70, 229, 0.1)'))
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        labels = ['Enterprise', 'Consumer', 'E-commerce', 'Wholesale']
        values = [45, 25, 20, 10]
        fig_donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7,
                                        marker=dict(colors=['#4F46E5', '#0ea5e9', '#8b5cf6', '#1e293b']))])
        fig_donut.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # CSV Upload Section
    st.markdown("---")
    st.markdown("### Train Custom Model")
    uploaded_file = st.file_uploader("Upload your historical sales dataset (CSV)", type="csv")
    if uploaded_file:
        df_uploaded = pd.read_csv(uploaded_file)
        st.success(f"Successfully loaded {len(df_uploaded)} rows.")
        st.dataframe(df_uploaded.head(5), use_container_width=True)
        if st.button("Run Forecast on New Data"):
            with st.spinner("Processing ML models..."):
                time.sleep(2)
            st.info("New forecast generated based on uploaded dataset.")

# --- Forecasting View ---
elif choice == "Forecasting Engine":
    st.title("Forecasting Engine")
    st.markdown("<p style='color: #94a3b8;'>Configure and run advanced predictive models.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Model Parameters")
        algo = st.selectbox("Algorithm", ["Random Forest Regressor", "XGBoost (Experimental)", "Prophet Engine"])
        horizon = st.selectbox("Forecast Horizon", ["Next 30 Days", "Next 90 Days", "Next 12 Months"])
        confidence = st.slider("Confidence Level", 80, 99, 95)
        if st.button("Run Simulation"):
            with st.status("Training models..."):
                st.write(f"Initializing {algo}...")
                time.sleep(1)
                st.write("Processing historical features...")
                time.sleep(1)
                st.write("Running cross-validation...")
                time.sleep(1)
            st.session_state.sim_run = True
            
    with col2:
        st.markdown("### Simulation Results")
        if st.session_state.get('sim_run'):
            acc = 95 + np.random.random() * 4
            yield_pct = 12 + np.random.random() * 10
            
            sc1, sc2 = st.columns(2)
            sc1.metric("Projected Yield", f"+{yield_pct:.1f}%", delta="Excellent")
            sc2.metric("Model Accuracy", f"{acc:.1f}%", delta="High")
            
            # Dummy chart
            chart_data = pd.DataFrame(np.random.randn(20, 2), columns=['Actual', 'Projected'])
            st.line_chart(chart_data)
        else:
            st.info("Configure parameters and click 'Run Simulation' to see projected outcomes.")

# --- Analytics View ---
elif choice == "Analytics":
    st.title("Deep Analytics")
    st.markdown("<p style='color: #94a3b8;'>Multi-dimensional analysis of your business performance.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Regional Performance")
        regions = pd.DataFrame({
            "Region": ["North America", "Europe", "Asia Pacific", "Latin America"],
            "Revenue": [1.2, 0.84, 0.65, 0.32]
        })
        st.bar_chart(regions.set_index("Region"))
        
    with col2:
        st.markdown("### Top Customers")
        customers = pd.DataFrame({
            "Client": ["Nebula Corp", "Vertex Ltd", "Stellar Solutions", "Aura Inc"],
            "Volume": ["$420k", "$310k", "$180k", "$140k"],
            "Growth": ["+12%", "+8%", "-3%", "+15%"]
        })
        st.table(customers)

# --- Inventory View ---
elif choice == "Inventory Intelligence":
    st.title("Inventory Intelligence")
    st.markdown("<p style='color: #94a3b8;'>Predictive stock management and warehouse optimization.</p>", unsafe_allow_html=True)
    
    # Inventory Status Row
    s_col1, s_col2, s_col3 = st.columns(3)
    s_col1.metric("Low Stock Alerts", "12", delta="-4", delta_color="inverse")
    s_col2.metric("Optimal Stock", "84%", delta="+2%")
    s_col3.metric("Stock Turnover", "5.2x", delta="+0.4x")
    
    st.markdown("### Warehouse Stock Levels")
    inventory_df = pd.DataFrame({
        "Product": ["UltraPod Pro", "SmartFrame 4K", "NeoWatch X", "GlowLamp Mini", "FlexTab 10", "VisionCore"],
        "Quantity": [12, 840, 56, 1200, 45, 120],
        "Threshold": [50, 200, 100, 300, 50, 150],
        "Demand": ["High", "Steady", "Low", "Seasonal", "High", "Steady"]
    })
    
    # Color coding logic for Stock Status
    inventory_df["Status"] = inventory_df.apply(lambda x: "Critical" if x["Quantity"] < x["Threshold"]*0.5 else ("Warning" if x["Quantity"] < x["Threshold"] else "Healthy"), axis=1)
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.dataframe(inventory_df, use_container_width=True)
    with c2:
        fig_inv = go.Figure(data=[
            go.Bar(name='Current', x=inventory_df["Product"], y=inventory_df["Quantity"], marker_color='#4F46E5'),
            go.Bar(name='Threshold', x=inventory_df["Product"], y=inventory_df["Threshold"], marker_color='rgba(255,255,255,0.2)')
        ])
        fig_inv.update_layout(barmode='group', template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=20, b=0), height=300)
        st.plotly_chart(fig_inv, use_container_width=True)
    
    st.markdown("### Restock Recommendations")
    st.info("Based on your sales velocity, we recommend restocking **UltraPod Pro** (500 units) and **FlexTab 10** (200 units) by Friday to avoid stockouts.")

# --- Settings View ---
elif choice == "Settings":
    st.title("Settings")
    st.markdown("<p style='color: #94a3b8;'>Configure your profile and application preferences.</p>", unsafe_allow_html=True)
    
    with st.form("settings_form"):
        col1, col2 = st.columns(2)
        with col1:
            first = st.text_input("First Name", value="Agnimitra")
            email = st.text_input("Email Address", value="agnimitra@forecastiq.com")
        with col2:
            last = st.text_input("Last Name", value="Dey")
            plan = st.selectbox("Plan", ["Pro Enterprise", "Startup", "Free"])
            
        if st.form_submit_button("Save Changes"):
            st.success(f"Settings saved for {first} {last}!")

# --- Sidebar Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px;">
        <img src="https://ui-avatars.com/api/?name=Agnimitra+Dey&background=4F46E5&color=fff" style="width: 32px; height: 32px; border-radius: 50%;">
        <div>
            <div style="font-size: 0.8rem; font-weight: bold; color: white;">Agnimitra Dey</div>
            <div style="font-size: 0.65rem; color: #64748b;">Pro Enterprise Plan</div>
        </div>
    </div>
""", unsafe_allow_html=True)
