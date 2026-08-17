# 🌍 TRAVEL 4D — Global Tourism Intelligence

> **Explore the world. Understand the season. Optimize the journey.**

**Live application:** https://travel-4d-tourism-intelligence-fclq2usq8dwy2unfm2p9nb.streamlit.app/

TRAVEL 4D is an interactive **tourism decision-intelligence platform** built with Python, Pandas, Plotly and Streamlit. It evaluates destinations across time rather than treating a country as a static travel recommendation.

The core question is:

> **Where should I travel, when should I go, and what trade-offs should I expect?**

The platform combines tourism-volume benchmarks with monthly cost, weather and crowd-pressure indices to produce an explainable **Travel Value Score** and personalized destination recommendations.

---

## 🎯 Why this project exists

Travel decisions are multi-factor decisions. The cheapest destination may have poor weather; the best weather may coincide with peak crowds; a popular destination may become significantly more attractive outside its peak season.

TRAVEL 4D models these trade-offs through a simple temporal intelligence layer:

```text
Destination + Month
        ↓
Cost + Weather + Crowd Signals
        ↓
Travel Value Score
        ↓
Comparison + Recommendation
```

The result is a lightweight decision-support system rather than a static tourism dashboard.

---

## 🚀 Key capabilities

- 🌍 **Interactive orthographic world globe**
- 📅 **12-month temporal seasonality analysis**
- 🏆 **30-destination tourism benchmark**
- ✈️ Seasonal flight-cost benchmark
- 🏨 Seasonal hotel-cost benchmark
- 🌦 Weather suitability scoring
- 👥 Tourism crowd-pressure scoring
- ⭐ Explainable Travel Value Score
- ⚖️ Destination-vs-destination comparison
- 🧠 Smart Trip Finder with selectable optimization priorities
- 🧭 Region and destination filtering
- 📚 Visible methodology and data-provenance layer
- 🛡️ Automated GitHub validation workflow
- ☁️ Public Streamlit deployment

---

## 🧠 Travel Value model

The current transparent scoring model uses:

| Factor | Weight |
|---|---:|
| Flight affordability | 25% |
| Hotel affordability | 20% |
| Weather suitability | 30% |
| Crowd avoidance | 25% |

The score is deliberately interpretable. A recommendation can therefore be explained rather than presented as an opaque machine-learning prediction.

### Priority modes

The Smart Trip Finder supports:

- **Balanced value** — overall Travel Value Score
- **Cost** — emphasizes flight and accommodation affordability
- **Weather** — emphasizes climate suitability
- **Low crowds** — emphasizes crowd avoidance

---

## 📊 Data methodology & responsible interpretation

The tourism-volume benchmark uses **2019 international tourism arrivals** from the World Bank World Development Indicators / UN Tourism source layer. The project uses 2019 as a clearly labeled benchmark because international-arrival definitions and collection methods can vary between destinations and because a uniform historical benchmark is useful for cross-country comparison.

The monthly flight, hotel, weather and crowd values are currently **derived baseline indices for the prototype**. They are **not live airfare quotes, live hotel prices, or official monthly tourism statistics**.

This distinction is intentional:

**Source data → documented benchmark → derived intelligence → recommendation**

This keeps the dashboard auditable and provides a clean path for replacing prototype indices with sourced monthly observations or optional live APIs later.

---

## 🏗️ Technical architecture

```text
                ┌─────────────────────┐
                │  Tourism Benchmark  │
                │   + CSV Data Layer  │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │  Seasonal Scoring   │
                │      Engine         │
                └──────────┬──────────┘
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
   Cost signals       Weather signal     Crowd signal
        └──────────────────┼──────────────────┘
                           ↓
                ┌─────────────────────┐
                │ Travel Value Score  │
                └──────────┬──────────┘
                           ↓
          Globe + Comparison + Trip Finder
                           ↓
                    Streamlit UI
```

### Engineering priorities

The project deliberately favors:

- Small local data files over unnecessary infrastructure
- Deterministic scoring over opaque models
- Cached data loading for responsive interaction
- Explicit schema validation
- Minimal external dependencies
- Automated Python compilation and dataset checks through GitHub Actions

This keeps the application easy to deploy, test and maintain.

---

## 🛠️ Technology stack

- **Python** — application and analytical logic
- **Pandas** — data processing
- **NumPy** — numerical operations
- **Plotly** — interactive geospatial and time-series visualization
- **Streamlit** — web application layer
- **GitHub Actions** — automated validation

---

## 📁 Project structure

```text
travel-4d-tourism-intelligence/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── .streamlit/
│   └── config.toml
├── .github/
│   └── workflows/
│       └── validate.yml
├── data/
│   └── destinations.csv
└── src/
    ├── __init__.py
    └── scoring.py
```

---

## ▶️ Run locally

```bash
git clone https://github.com/Hadi-Saeed-2006/travel-4d-tourism-intelligence.git
cd travel-4d-tourism-intelligence
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔬 What makes the project technically interesting

### 1. Temporal decision intelligence

A destination is evaluated across twelve monthly states instead of receiving one static score.

### 2. Explainable composite scoring

The recommendation engine exposes its component signals and weights, making the output interpretable.

### 3. Geospatial exploration

The orthographic globe provides a spatial interface for comparing destinations across regions.

### 4. Multi-objective recommendation

The Smart Trip Finder changes its objective function depending on whether the user prioritizes cost, weather, crowds or balanced value.

### 5. Data-quality awareness

The application validates required columns and destination uniqueness before analysis, while GitHub Actions performs automated checks on pushes and pull requests.

---

## 🔭 Roadmap

### Completed ✅

- 30-destination benchmark
- Seasonal intelligence engine
- Travel Value Score
- Interactive globe
- Destination comparison
- Smart Trip Finder
- Methodology/provenance layer
- GitHub Actions validation
- Streamlit deployment

### Next-generation upgrades

- Replace prototype monthly indices with sourced monthly observations
- Add explicit shoulder-season detection using tourism concentration metrics
- Add origin-aware flight modelling
- Add destination expense profiles
- Add source freshness metadata
- Add optional live pricing integrations
- Add automated data refresh pipelines

---

## ⚠️ Limitations

TRAVEL 4D is a **decision-support prototype**, not a booking engine or price-guarantee system. Benchmark indices should not be interpreted as current market prices.

Tourism-arrival statistics represent reported arrivals/trips and may differ in definition and collection methodology across destinations. Derived scores are analytical estimates produced by this project.

---

## 👤 Author

**Hadi Shaikh**  
Data Science student focused on analytics, AI/ML and decision-intelligence applications.

---

## 📌 Portfolio positioning

**Project type:** Data Analytics + Decision Intelligence + Geospatial Visualization  
**Application:** Tourism planning and destination intelligence  
**Deployment:** Streamlit  
**Repository:** GitHub  

> Built as a practical demonstration of data modelling, explainable scoring, geospatial visualization, interactive analytics, validation and production-oriented deployment.
