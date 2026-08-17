import pandas as pd
import plotly.express as px
import streamlit as st
from src.scoring import MONTHS, classify_seasons, seasonal_table

st.set_page_config(page_title="TRAVEL 4D", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
.hero {padding: 1.25rem 1.5rem; border: 1px solid rgba(128,128,128,.25); border-radius: 18px; margin-bottom: 1rem;}
.small {opacity:.72; font-size:.9rem;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = pd.read_csv("data/destinations.csv")
    required = {"country", "region", "latitude", "longitude", "benchmark_rank", "arrivals_2019_m", "flight_index", "weather_index", "crowd_index"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    return data

df = load_data()

st.markdown('<div class="hero"><h1>🌍 TRAVEL 4D</h1><p>Global Tourism Intelligence — destination seasonality, cost pressure, weather and travel value.</p><p class="small">Decision-support platform • Transparent benchmark + derived intelligence model</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🧭 Trip Controls")
    regions = ["All regions"] + sorted(df["region"].unique().tolist())
    region_filter = st.selectbox("Region", regions)
    filtered = df if region_filter == "All regions" else df[df["region"] == region_filter]
    selected_country = st.selectbox("Destination", filtered["country"].tolist())
    month = st.selectbox("Travel month", MONTHS, index=8)
    priority = st.selectbox("Priority", ["Balanced", "Lowest Cost", "Weather", "Avoid Crowds"])
    st.divider()
    st.caption("Cost values are seasonal benchmark indices, not live fares or hotel quotes.")

row = df[df["country"] == selected_country].iloc[0]
season = seasonal_table(row["region"], row["flight_index"], row["crowd_index"], row["weather_index"])
selected = season[season["month"] == month].iloc[0]
labels = classify_seasons(season)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Tourism benchmark rank", f"#{int(row['benchmark_rank'])}")
c2.metric("Travel Value", f"{selected['value_score']:.0f}/100")
c3.metric("Weather", f"{selected['weather_score']:.0f}/100")
c4.metric("Crowd pressure", f"{selected['crowd_score']:.0f}/100")

st.subheader(f"🌐 {selected_country} — Intelligence Brief")
a, b, c, d = st.columns(4)
a.metric("Cheapest benchmark", labels["cheapest"])
b.metric("Best overall", labels["best"])
c.metric("Shoulder window", labels["shoulder"])
d.metric("Peak crowd month", labels["peak"])

st.subheader("📅 12-Month Seasonality Intelligence")
fig = px.line(season, x="month", y=["value_score", "weather_score", "crowd_score"], markers=True, labels={"value_score":"Score", "month":"Month", "variable":"Indicator"})
fig.update_yaxes(range=[0, 100])
fig.update_layout(height=410, legend_title_text="")
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns([1.35, 1])
with left:
    st.subheader("🌍 Global Destination Explorer")
    map_df = df.copy()
    map_df["label"] = map_df["country"] + " • #" + map_df["benchmark_rank"].astype(str)
    fig_map = px.scatter_geo(map_df, lat="latitude", lon="longitude", hover_name="country", hover_data={"benchmark_rank": True, "arrivals_2019_m": True, "region": True, "latitude": False, "longitude": False}, size="arrivals_2019_m", color="region", projection="orthographic", title="Tourism benchmark globe")
    fig_map.update_layout(height=560, margin=dict(l=0,r=0,t=50,b=0))
    st.plotly_chart(fig_map, use_container_width=True)
with right:
    st.subheader("🏆 Benchmark Ranking")
    ranking = df[["benchmark_rank", "country", "region", "arrivals_2019_m"]].sort_values("benchmark_rank").copy()
    ranking.columns = ["Rank", "Country", "Region", "Arrivals (M)"]
    st.dataframe(ranking, hide_index=True, use_container_width=True, height=480)

st.subheader("⚖️ Destination Comparison")
comp_options = df["country"].tolist()
comp1, comp2 = st.columns(2)
with comp1:
    country_a = st.selectbox("Destination A", comp_options, index=comp_options.index(selected_country), key="compare_a")
with comp2:
    default_b = 1 if comp_options.index(country_a) != 1 else 0
    country_b = st.selectbox("Destination B", comp_options, index=default_b, key="compare_b")

comparison_rows = []
for country in [country_a, country_b]:
    r = df[df["country"] == country].iloc[0]
    s = seasonal_table(r["region"], r["flight_index"], r["crowd_index"], r["weather_index"])
    m = s[s["month"] == month].iloc[0]
    comparison_rows.append({"Metric": "Tourism rank", country: int(r["benchmark_rank"]) if country == country_a else None})
    comparison_rows.append({"Metric": "Travel Value", country: round(m["value_score"], 1)})
    comparison_rows.append({"Metric": "Weather", country: round(m["weather_score"], 1)})
    comparison_rows.append({"Metric": "Crowd pressure", country: round(m["crowd_score"], 1)})
    comparison_rows.append({"Metric": "Flight index", country: round(m["flight_index"], 1)})
    comparison_rows.append({"Metric": "Hotel index", country: round(m["hotel_index"], 1)})

comparison = pd.DataFrame(comparison_rows).groupby("Metric", as_index=False).first()
for country in [country_a, country_b]:
    if country not in comparison.columns:
        comparison[country] = None
st.dataframe(comparison[["Metric", country_a, country_b]], hide_index=True, use_container_width=True)

st.subheader("🧠 Smart Trip Finder")
fc1, fc2, fc3 = st.columns(3)
with fc1:
    finder_month = st.selectbox("Preferred month", MONTHS, index=8, key="finder_month")
with fc2:
    finder_priority = st.selectbox("Optimize for", ["Balanced value", "Cost", "Weather", "Low crowds"], key="finder_priority")
with fc3:
    top_n = st.slider("Show destinations", 3, 10, 5)

scores = []
for _, r in df.iterrows():
    s = seasonal_table(r["region"], r["flight_index"], r["crowd_index"], r["weather_index"])
    m = s[s["month"] == finder_month].iloc[0]
    if finder_priority == "Cost":
        score = (100 - m["flight_index"])*0.45 + (100 - m["hotel_index"])*0.35 + m["weather_score"]*0.20
    elif finder_priority == "Weather":
        score = m["weather_score"]*0.60 + (100-m["crowd_score"])*0.20 + (100-m["hotel_index"])*0.20
    elif finder_priority == "Low crowds":
        score = (100-m["crowd_score"])*0.55 + m["weather_score"]*0.30 + (100-m["hotel_index"])*0.15
    else:
        score = m["value_score"]
    scores.append((r["country"], r["region"], score, m["weather_score"], m["crowd_score"], m["flight_index"], m["hotel_index"]))

results = pd.DataFrame(scores, columns=["Country", "Region", "Match", "Weather", "Crowd", "Flight index", "Hotel index"]).sort_values("Match", ascending=False).head(top_n)
for col in ["Match", "Weather", "Crowd", "Flight index", "Hotel index"]:
    results[col] = results[col].round(1)
st.dataframe(results, hide_index=True, use_container_width=True)

with st.expander("📚 Methodology & Data Provenance"):
    st.markdown("""
**Tourism benchmark:** International tourism arrivals benchmark, 2019, using the World Bank World Development Indicators / UN Tourism source layer. Arrival counts represent tourism trips/arrivals rather than unique travelers, and country methodologies can differ.

**Seasonal intelligence:** Monthly flight, hotel, crowd and weather values are derived baseline indices for a transparent prototype. They are not live airfare/hotel quotes or official statistics.

**Travel Value Score:** 25% flight affordability + 20% hotel affordability + 30% weather suitability + 25% crowd avoidance.

**Production path:** replace baseline indices with sourced monthly observations and optional live pricing feeds without changing the scoring interface.
    """)

st.caption("TRAVEL 4D • Global Tourism Intelligence • Python + Pandas + Plotly + Streamlit")
