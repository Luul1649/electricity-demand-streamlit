import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Kenya Electricity Demand Dashboard",
    layout="wide"
)

st.title("🔌 AI-Driven Electricity Demand Forecasting – Kenya")
st.markdown("This dashboard presents trends, drivers, and forecasts of electricity demand to support energy policy planning.")

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("kenya_electricity_cleaned.csv")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.header("Controls")
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (2000, int(df["Year"].max()))
)

df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

# -------------------------------
# SECTION 1: OVERVIEW
# -------------------------------
st.subheader("📈 Electricity Demand Trend")

fig1, ax1 = plt.subplots()
ax1.plot(df_filtered["Year"], df_filtered["Electricity_Consumption"])
ax1.set_xlabel("Year")
ax1.set_ylabel("Electricity Consumption (kWh per capita)")
ax1.set_title("Electricity Consumption Trend in Kenya")
st.pyplot(fig1)

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Average Consumption", f"{df_filtered['Electricity_Consumption'].mean():.1f}")
col2.metric("Maximum Consumption", f"{df_filtered['Electricity_Consumption'].max():.1f}")
col3.metric("Minimum Consumption", f"{df_filtered['Electricity_Consumption'].min():.1f}")

# -------------------------------
# SECTION 2: DRIVERS
# -------------------------------
st.subheader("📊 Drivers of Electricity Demand")

feature = st.selectbox(
    "Select Driver",
    ["GDP_Growth", "Population", "Urbanization"]
)

fig2, ax2 = plt.subplots()
ax2.scatter(df_filtered[feature], df_filtered["Electricity_Consumption"])
ax2.set_xlabel(feature)
ax2.set_ylabel("Electricity Consumption")
ax2.set_title(f"Electricity Consumption vs {feature}")
st.pyplot(fig2)

# -------------------------------
# SECTION 3: CORRELATION
# -------------------------------
st.subheader("🔗 Correlation Analysis")

corr = df_filtered[[
    "Electricity_Consumption",
    "GDP_Growth",
    "Population",
    "Urbanization"
]].corr()

st.dataframe(corr.style.background_gradient(cmap="Blues"))

# -------------------------------
# SECTION 4: SIMPLE FORECAST (ILLUSTRATIVE)
# -------------------------------
st.subheader("🔮 Electricity Demand Forecast (Illustrative)")

forecast_years = st.slider("Forecast Years", 1, 10, 5)

last_year = df["Year"].max()
last_value = df["Electricity_Consumption"].iloc[-1]

growth_rate = df["Electricity_Consumption"].pct_change().mean()

future_years = [last_year + i for i in range(1, forecast_years + 1)]
future_values = [
    last_value * (1 + growth_rate) ** i for i in range(1, forecast_years + 1)
]

forecast_df = pd.DataFrame({
    "Year": future_years,
    "Forecasted Electricity Consumption": future_values
})

fig3, ax3 = plt.subplots()
ax3.plot(df["Year"], df["Electricity_Consumption"], label="Historical")
ax3.plot(forecast_df["Year"], forecast_df["Forecasted Electricity Consumption"], linestyle="--", label="Forecast")
ax3.set_xlabel("Year")
ax3.set_ylabel("Electricity Consumption")
ax3.legend()
st.pyplot(fig3)

# -------------------------------
# SECTION 5: POLICY INSIGHTS
# -------------------------------
st.subheader("🏛️ Policy Insights")

st.markdown("""
- Electricity demand has increased steadily, driven by population growth and urbanization.
- Economic growth contributes to short-term fluctuations.
- Forecasts suggest continued demand growth, highlighting the need for investment in generation capacity.
- Policy interventions should prioritize renewable energy expansion and grid reliability.
""")

st.success("Dashboard ready for policy decision support.")

