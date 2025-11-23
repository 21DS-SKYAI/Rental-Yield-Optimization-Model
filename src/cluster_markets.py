from sklearn.cluster import KMeans

def cluster_markets(df, n_clusters=8):
    features = df[["rental_yield", "locality_score", "amenities_score"]]
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(features)
    return df, kmeans
