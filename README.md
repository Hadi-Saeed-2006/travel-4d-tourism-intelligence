# 🌍 TRAVEL 4D — Global Tourism Intelligence

> **Explore the world. Understand the season. Optimize the journey.**

TRAVEL 4D is a Streamlit-based tourism intelligence platform designed to help travellers understand **where and when to travel** by combining tourism volume, seasonal cost pressure, weather suitability and crowd pressure into a transparent decision-support model.

## 🚀 Current capabilities

- 🌍 Interactive orthographic tourism globe
- 🏆 20-country tourism benchmark ranking
- 📅 12-month destination seasonality analysis
- ✈️ Flight-cost seasonal benchmark index
- 🏨 Hotel-cost seasonal benchmark index
- 🌦 Weather suitability score
- 👥 Tourism crowd-pressure score
- ⭐ Travel Value Score
- 🧠 Smart Trip Finder with configurable priorities
- 📚 Visible methodology and data-provenance layer

## 🧠 Intelligence model

The current prototype calculates Travel Value using:

| Factor | Weight |
|---|---:|
| Flight affordability | 25% |
| Hotel affordability | 20% |
| Weather suitability | 30% |
| Crowd avoidance | 25% |

The scoring engine is deliberately transparent so that every recommendation can be explained.

## 📊 Data methodology

The tourism benchmark uses **2019 international tourism arrivals** from the World Bank World Development Indicators / UN Tourism source layer. The project uses 2019 as a clearly labeled benchmark because cross-country arrival definitions and collection methods vary and recent annual observations are not uniformly available for every destination.

The current monthly flight, hotel, weather and crowd values are **derived baseline indices for the prototype**. They are not live fares, live hotel quotes or official monthly statistics.

This separation between source statistics and derived intelligence is intentional. It makes the system easier to audit and gives the project a clean path to a production data layer.

## 🛠️ Technology

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

## ▶️ Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project structure

```text
travel-4d-tourism-intelligence/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── destinations.csv
└── src/
    └── scoring.py
```

## 🔭 Roadmap

### Phase 1 — Foundation ✅
- Repository
- Data schema
- Tourism benchmark dataset
- Streamlit application
- Transparent scoring engine

### Phase 2 — Intelligence
- Country-specific monthly observations
- Better shoulder-season detection
- Destination cost modelling
- Origin-to-destination travel modelling

### Phase 3 — 4D Experience
- Animated global seasonality layer
- Destination comparison mode
- Time-slider exploration
- Advanced geospatial storytelling

### Phase 4 — Production polish
- Automated data validation
- Source freshness checks
- Optional live pricing integrations
- Streamlit Cloud deployment

## ⚠️ Important limitation

TRAVEL 4D is a **decision-support prototype**, not a live booking or price-guarantee system. Any cost index must be interpreted as a benchmark unless a live data source is explicitly connected.

## 👤 Author

**Hadi Shaikh** — Data Science student building practical analytics and decision-intelligence products.
