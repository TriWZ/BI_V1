
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Triphorium Real-Time Energy Dashboard")

# --- Upload Section ---
st.sidebar.header("Upload Your Excel Data")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
else:
    # Load sample data if none uploaded
    df = pd.read_excel("MultiBuilding_Utility_SampleData.xlsx")

# --- Filter Section ---
st.sidebar.header("Filter")
buildings = df["Building"].unique().tolist()
selected_buildings = st.sidebar.multiselect("Select Buildings", buildings, default=buildings)

df_filtered = df[df["Building"].isin(selected_buildings)]

# --- KPI Summary ---
st.markdown("### Key Performance Indicators (Year-to-Date)")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Electricity (kWh)", f"{df_filtered['Electricity (kWh)'].sum():,.0f}")
kpi2.metric("Total Water (tons)", f"{df_filtered['Water (tons)'].sum():,.0f}")
kpi3.metric("Total Gas (m³)", f"{df_filtered['Gas (m³)'].sum():,.0f}")
kpi4.metric("Total CO₂ (tons)", f"{df_filtered['CO₂ Emissions (tons)'].sum():.2f}")

# --- Trend Charts ---
st.markdown("### Monthly Trends by Building")

tab1, tab2, tab3, tab4 = st.tabs(["Gas", "CO₂ Emissions", "Electricity", "Water"])

with tab1:
    fig1 = px.line(df_filtered, x="Month", y="Gas (m³)", color="Building", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.area(df_filtered, x="Month", y="CO₂ Emissions (tons)", color="Building", groupnorm='fraction')
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fig3 = px.line(df_filtered, x="Month", y="Electricity (kWh)", color="Building", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    fig4 = px.scatter(df_filtered, x="Month", y="Water (tons)", color="Building", size="Water (tons)", hover_name="Building")
    st.plotly_chart(fig4, use_container_width=True)

# --- Raw Data Table ---
st.markdown("### Raw Utility Data")
st.dataframe(df_filtered)
