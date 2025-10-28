from raw_data_study import correlation_with_target
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def cluster_columns(df: pd.DataFrame, columns: list[str], new_columns_name: str):

    df[columns] = df[columns].astype(float)

    X = df.copy()


    # YOUR CODE HERE: Define a list of the features to be used for the clustering
    features = columns


    # Standardize
    X_scaled = X.loc[:, features]
    X_scaled = (X_scaled - X_scaled.mean(axis=0)) / X_scaled.std(axis=0)


    # YOUR CODE HERE: Fit the KMeans model to X_scaled and create the cluster labels
    kmeans = KMeans(n_clusters=10, n_init=10, random_state=0)
    X["Cluster"] = kmeans.fit_predict(X_scaled)
    X["Cluster"] = X["Cluster"].astype('category')

    df["Cluster"] = X[new_columns_name]
    correlation_with_target(df, "Cluster")
