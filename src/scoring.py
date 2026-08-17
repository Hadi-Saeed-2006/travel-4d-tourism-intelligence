import numpy as np
import pandas as pd

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Transparent baseline seasonal patterns. These are model inputs, not live prices.
REGION_PATTERNS = {
    "Europe": {
        "cost": [0.72, 0.70, 0.78, 0.86, 0.92, 1.02, 1.14, 1.10, 0.92, 0.84, 0.74, 0.88],
        "crowd": [0.38, 0.34, 0.48, 0.65, 0.78, 0.90, 1.00, 0.96, 0.78, 0.62, 0.42, 0.70],
        "weather": [0.45, 0.48, 0.58, 0.72, 0.84, 0.90, 0.92, 0.90, 0.84, 0.72, 0.58, 0.46],
    },
    "Asia": {
        "cost": [0.82, 0.84, 0.90, 0.88, 0.76, 0.68, 0.70, 0.70, 0.68, 0.72, 0.82, 0.96],
        "crowd": [0.78, 0.76, 0.66, 0.62, 0.52, 0.46, 0.48, 0.48, 0.46, 0.54, 0.66, 0.90],
        "weather": [0.86, 0.88, 0.82, 0.72, 0.62, 0.56, 0.58, 0.58, 0.60, 0.68, 0.78, 0.86],
    },
    "North America": {
        "cost": [0.76, 0.72, 0.76, 0.82, 0.88, 0.98, 1.12, 1.08, 0.88, 0.80, 0.72, 0.90],
        "crowd": [0.42, 0.38, 0.46, 0.58, 0.70, 0.86, 1.00, 0.96, 0.72, 0.58, 0.44, 0.76],
        "weather": [0.58, 0.62, 0.68, 0.76, 0.84, 0.90, 0.92, 0.90, 0.84, 0.76, 0.64, 0.58],
    },
    "South America": {
        "cost": [0.92, 0.96, 0.88, 0.78, 0.70, 0.66, 0.68, 0.70, 0.72, 0.76, 0.82, 1.00],
        "crowd": [0.86, 0.88, 0.72, 0.58, 0.46, 0.42, 0.44, 0.46, 0.52, 0.58, 0.66, 0.92],
        "weather": [0.84, 0.82, 0.78, 0.74, 0.70, 0.68, 0.70, 0.72, 0.76, 0.80, 0.82, 0.86],
    },
    "Africa": {
        "cost": [0.78, 0.76, 0.72, 0.68, 0.66, 0.70, 0.76, 0.78, 0.74, 0.70, 0.72, 0.82],
        "crowd": [0.68, 0.62, 0.56, 0.50, 0.48, 0.52, 0.60, 0.64, 0.58, 0.54, 0.58, 0.72],
        "weather": [0.80, 0.82, 0.84, 0.82, 0.78, 0.72, 0.70, 0.72, 0.78, 0.82, 0.84, 0.82],
    },
    "Middle East": {
        "cost": [0.82, 0.80, 0.84, 0.88, 0.96, 1.04, 1.08, 1.06, 0.96, 0.88, 0.78, 0.76],
        "crowd": [0.76, 0.70, 0.58, 0.44, 0.34, 0.28, 0.24, 0.24, 0.32, 0.46, 0.64, 0.82],
        "weather": [0.88, 0.90, 0.88, 0.80, 0.66, 0.52, 0.38, 0.38, 0.52, 0.70, 0.84, 0.90],
    },
    "Oceania": {
        "cost": [1.02, 0.98, 0.88, 0.76, 0.68, 0.66, 0.68, 0.70, 0.74, 0.80, 0.88, 1.04],
        "crowd": [0.90, 0.82, 0.64, 0.50, 0.42, 0.38, 0.40, 0.44, 0.52, 0.62, 0.74, 0.94],
        "weather": [0.88, 0.84, 0.78, 0.72, 0.68, 0.66, 0.68, 0.70, 0.74, 0.78, 0.82, 0.88],
    },
}


def seasonal_table(region: str, base_cost: float, base_crowd: float, base_weather: float) -> pd.DataFrame:
    pattern = REGION_PATTERNS.get(region, REGION_PATTERNS["Europe"])
    df = pd.DataFrame({"month": MONTHS, "cost_factor": pattern["cost"], "crowd_factor": pattern["crowd"], "weather_factor": pattern["weather"]})
    df["flight_index"] = np.clip(base_cost * df["cost_factor"] * 1.02, 20, 120)
    df["hotel_index"] = np.clip(base_cost * df["cost_factor"] * 0.98, 20, 120)
    df["crowd_score"] = np.clip((base_crowd * 0.65 + df["crowd_factor"] * 100 * 0.35), 0, 100)
    df["weather_score"] = np.clip((base_weather * 0.55 + df["weather_factor"] * 100 * 0.45), 0, 100)
    df["value_score"] = (
        (100 - df["flight_index"]) * 0.25
        + (100 - df["hotel_index"]) * 0.20
        + df["weather_score"] * 0.30
        + (100 - df["crowd_score"]) * 0.25
    ).round(1)
    return df


def classify_seasons(df: pd.DataFrame) -> dict:
    cheapest = df.loc[df["flight_index"].add(df["hotel_index"]).idxmin(), "month"]
    best = df.loc[df["value_score"].idxmax(), "month"]
    peak = df.loc[df["crowd_score"].idxmax(), "month"]
    sorted_months = df.sort_values("crowd_score")["month"].tolist()
    shoulder = ", ".join(sorted_months[2:4])
    return {"cheapest": cheapest, "best": best, "peak": peak, "shoulder": shoulder}
