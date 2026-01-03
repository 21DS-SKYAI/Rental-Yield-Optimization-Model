import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px

# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(
    page_title="Rental Insight Engine",
    layout="wide"
)

# ---------------------------------
# Header
# ---------------------------------
st.title("🏙️ Rental Market Insight Engine")
st.markdown(
    """
    **Set the right rent using data, not guesswork.**

    Upload your property data and instantly discover:
    - 📍 Micro-markets
    - 💰 Underpriced & overpriced rentals
    - 🎯 Optimal rent recommendations
    """
)

st.divider()

# ---------------------------------
# Step 1: Upload Data
# ---------------------------------
st.subheader("📤 Step 1: Upload Your Property Data")

st.markdown(
    """
    Upload a **CSV or Excel file** with the following **mandatory columns**:

    `latitude | longitude | carpet_area_sqft | monthly_rent`

    Optional (recommended):
    `amenities_count | building_age`
    """
)

uploaded_file = st.file_uploader(
    "Choose your file",
    type=["csv", "xlsx"]
)

# ---------------------------------
# If file uploaded
# ---------------------------------
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File uploaded successfully!")

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # ---------------------------------
    # Validate columns
    # ---------------------------------
    required_cols = [
        "latitude", "longitude",
        "carpet_area_sqft", "monthly_rent"
    ]

    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        st.error(f"❌ Missing required columns: {missing}")
        st.stop()

    # ---------------------------------
    # Step 2: Prepare Data
    # ---------------------------------
    st.subheader("⚙️ Step 2: Preparing Your Data")

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

    st.success("✅ Data standardized and ready for analysis")

    # ---------------------------------
    # Step 3: Analysis Controls
    # ---------------------------------
    st.sidebar.header("⚙️ Analysis Settings")

    k = st.sidebar.slider(
        "Number of Micro-Markets",
        min_value=3,
        max_value=8,
        value=5,
        help="Higher value = more granular market segments"
    )

    if st.sidebar.button("🚀 Analyze Market"):
        # ---------------------------------
        # Clustering
        # ---------------------------------
        kmeans = KMeans(n_clusters=k, random_state=42)
        df["micro_market"] = kmeans.fit_predict(X)

        # ---------------------------------
        # Benchmarking
        # ---------------------------------
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
                return "🟢 Underpriced"
            elif x > 10:
                return "🔴 Overpriced"
            else:
                return "⚪ Fair"

        df["pricing_label"] = df["pricing_gap_pct"].apply(label)

        df["recommended_rent"] = (
            df["cluster_median"] * df["carpet_area_sqft"]
        ).round(0)

        # ---------------------------------
        # KPIs
        # ---------------------------------
        st.subheader("📊 Market Summary")

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Properties", len(df))
        c2.metric(
            "Underpriced",
            (df["pricing_label"] == "🟢 Underpriced").sum()
        )
        c3.metric(
            "Overpriced",
            (df["pricing_label"] == "🔴 Overpriced").sum()
        )

        # ---------------------------------
        # Map
        # ---------------------------------
        st.subheader("📍 Micro-Market Map")

        fig = px.scatter_mapbox(
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
        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------
        # Table
        # ---------------------------------
        st.subheader("📋 Property-Level Insights")

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
    st.info("👆 Upload your data file to start the analysis")

# ---------------------------------
# How It Works (Bottom Section)
# ---------------------------------
st.divider()

st.subheader("🧩 How This App Works")

st.markdown(
    """
    **1️⃣ Upload your rental data**  
    Provide property-level rent and location details.

    **2️⃣ Micro-markets are created**  
    Similar properties are grouped using Machine Learning.

    **3️⃣ Peer comparison happens**  
    Each property is compared only with similar units.

    **4️⃣ Actionable insights delivered**  
    You instantly see underpriced, fair, and overpriced rentals along with optimal rent suggestions.
    """
)
