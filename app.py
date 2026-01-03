import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Rental Yield Optimization",
    layout="wide"
)

st.title("🏙️ Rental Yield Optimization & Market Segmentation")
st.markdown("Micro-market based rent optimization using K-Means clustering")

# -----------------------------
# Generate Synthetic Data
# -----------------------------
@st.cache_data
def generate_data(n=100):
    np.random.seed(42)

    df = pd.DataFrame({
        "latitude": np.random.uniform(18.90, 19.30, n),
        "longitude": np.random.uniform(72.80, 72.98, n),
        "carpet_area_sqft": np.random.randint(350, 1500, n),
        "building_age": np.random.randint(0, 40, n),
        "floor_level": np.random.randint(1, 35, n),
        "property_type": np.random.choice(
            ["Budget", "Mid", "Luxury"], n, p=[0.3, 0.45, 0.25]
        ),
        "furnishing": np.random.choice(
            ["Unfurnished", "Semi-Furnished", "Fully-Furnished"], n,
            p=[0.4, 0.35, 0.25]
        ),
        "parking": np.random.choice([0, 1], n, p=[0.35, 0.65]),
        "amenities_count": np.random.randint(1, 8, n),
    })

    base_rate = np.random.randint(90, 180, n)

    type_mult = df["property_type"].map({
        "Budget": 0.85,
        "Mid": 1.0,
        "Luxury": 1.35
    })

    furnish_mult = df["furnishing"].map({
        "Unfurnished": 0.9,
        "Semi-Furnished": 1.0,
        "Fully-Furnished": 1.15
    })

    amenity_mult = 1 + df["amenities_count"] * 0.02
    floor_mult = 1 + df["floor_level"] / 100

    df["monthly_rent"] = (
        df["carpet_area_sqft"]
        * base_rate
        * type_mult
        * furnish_mult
        * amenity_mult
        * floor_mult
    ).round(0)

    return df

df = generate_data()

# -----------------------------
# Feature Engineering
# -----------------------------
df["rent_per_sqft"] = df["monthly_rent"] / df["carpet_area_sqft"]

features = [
    "latitude",
    "longitude",
    "rent_per_sqft",
    "carpet_area_sqft",
    "amenities_count",
    "building_age"
]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

# -----------------------------
# Clustering
# -----------------------------
k = st.sidebar.slider("Number of Micro-Markets (Clusters)", 3, 8, 5)

kmeans = KMeans(n_clusters=k, random_state=42)
df["micro_market"] = kmeans.fit_predict(X_scaled)

# -----------------------------
# Benchmarking
# -----------------------------
cluster_stats = (
    df.groupby("micro_market")["rent_per_sqft"]
    .median()
    .reset_index()
    .rename(columns={"rent_per_sqft": "cluster_median"})
)

df = df.merge(cluster_stats, on="micro_market")

df["pricing_gap_pct"] = (
    (df["rent_per_sqft"] - df["cluster_median"])
    / df["cluster_median"]
) * 100

def price_label(x):
    if x < -10:
        return "Underpriced"
    elif x > 10:
        return "Overpriced"
    else:
        return "Fair"

df["pricing_label"] = df["pricing_gap_pct"].apply(price_label)

df["recommended_rent"] = (
    df["cluster_median"] * df["carpet_area_sqft"]
).round(0)

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Properties", len(df))
col2.metric("Underpriced Units", (df["pricing_label"] == "Underpriced").sum())
col3.metric("Overpriced Units", (df["pricing_label"] == "Overpriced").sum())

# -----------------------------
# Map Visualization
# -----------------------------
st.subheader("📍 Micro-Market Clusters")

fig_map = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    color="micro_market",
    size="rent_per_sqft",
    zoom=10,
    mapbox_style="carto-positron",
    hover_data=[
        "monthly_rent",
        "pricing_label",
        "recommended_rent"
    ]
)

st.plotly_chart(fig_map, use_container_width=True)

# -----------------------------
# Pricing Distribution
# -----------------------------
st.subheader("📊 Rent per Sqft Distribution by Cluster")

fig_box = px.box(
    df,
    x="micro_market",
    y="rent_per_sqft",
    color="pricing_label"
)

st.plotly_chart(fig_box, use_container_width=True)

# -----------------------------
# Data Table
# -----------------------------
st.subheader("📋 Property-Level Insights")

st.dataframe(
    df[
        [
            "micro_market",
            "carpet_area_sqft",
            "monthly_rent",
            "recommended_rent",
            "pricing_label",
            "pricing_gap_pct"
        ]
    ].sort_values("pricing_gap_pct")
)
