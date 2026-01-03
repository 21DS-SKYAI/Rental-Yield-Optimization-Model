import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px

st.set_page_config(page_title="Rental Insight Engine", layout="wide")

st.title("🏙️ Rental Market Insight Engine")
st.markdown("Upload your property data and get **instant micro-market insights**")

# -----------------------------
# Upload Section
# -----------------------------
uploaded_file = st.file_uploader(
    "📤 Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Data uploaded successfully!")

    st.subheader("🔍 Preview")
    st.dataframe(df.head())

    required_cols = [
        "latitude", "longitude",
        "carpet_area_sqft", "monthly_rent"
    ]

    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        st.error(f"Missing required columns: {missing}")
        st.stop()

    # -----------------------------
    # Feature Engineering
    # -----------------------------
    df["rent_per_sqft"] = df["monthly_rent"] / df["carpet_area_sqft"]

    df["amenities_count"] = df.get("amenities_count", 1)
    df["building_age"] = df.get("building_age", 10)

    features = [
        "latitude",
        "longitude",
        "rent_per_sqft",
        "carpet_area_sqft",
        "amenities_count",
        "building_age"
    ]

    X = StandardScaler().fit_transform(df[features])

    # -----------------------------
    # Clustering Control
    # -----------------------------
    st.sidebar.header("⚙️ Controls")
    k = st.sidebar.slider("Number of Micro-Markets", 3, 8, 5)

    if st.sidebar.button("🚀 Analyze Market"):
        kmeans = KMeans(n_clusters=k, random_state=42)
        df["micro_market"] = kmeans.fit_predict(X)

        # -----------------------------
        # Benchmarking
        # -----------------------------
        cluster_median = (
            df.groupby("micro_market")["rent_per_sqft"]
            .median()
        )

        df["cluster_median"] = df["micro_market"].map(cluster_median)

        df["pricing_gap_pct"] = (
            (df["rent_per_sqft"] - df["cluster_median"])
            / df["cluster_median"]
        ) * 100

        def label(x):
            if x < -10:
                return "Underpriced"
            elif x > 10:
                return "Overpriced"
            else:
                return "Fair"

        df["pricing_label"] = df["pricing_gap_pct"].apply(label)

        df["recommended_rent"] = (
            df["cluster_median"] * df["carpet_area_sqft"]
        ).round(0)

        # -----------------------------
        # KPIs
        # -----------------------------
        c1, c2, c3 = st.columns(3)
        c1.metric("Properties", len(df))
        c2.metric("Underpriced", (df["pricing_label"] == "Underpriced").sum())
        c3.metric("Overpriced", (df["pricing_label"] == "Overpriced").sum())

        # -----------------------------
        # Map
        # -----------------------------
        st.subheader("📍 Micro-Market Map")
        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color="micro_market",
            size="rent_per_sqft",
            hover_data=[
                "monthly_rent",
                "pricing_label",
                "recommended_rent"
            ],
            zoom=10,
            mapbox_style="carto-positron"
        )
        st.plotly_chart(fig, use_container_width=True)

        # -----------------------------
        # Table
        # -----------------------------
        st.subheader("📊 Property Insights")
        st.dataframe(
            df.sort_values("pricing_gap_pct")[
                [
                    "micro_market",
                    "monthly_rent",
                    "recommended_rent",
                    "pricing_label",
                    "pricing_gap_pct"
                ]
            ]
        )
else:
    st.info("Upload a CSV or Excel file to begin analysis.")


st.subheader("🧩 How This App Works")

st.markdown("""
1️⃣ Upload your rental property data (CSV / Excel)  
Note that Data field's must have - (latitude | longitude | carpet_area_sqft | monthly_rent | amenities_count)
2️⃣ We automatically group properties into **micro-markets**  
3️⃣ Each property is compared only with **similar peers**  
4️⃣ You get **underpriced / overpriced flags** and **optimal rent**
""")


    caption="Rental Market Insight Workflow",
    use_column_width=True
)


