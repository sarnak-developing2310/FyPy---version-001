import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import os

def extract_features(df):
    """
    Extract features from a DataFrame that contains:
      - 'Close' column (daily close prices)
      - 'Volume' column (daily volumes)
    Uses the first day's close as the strike price for adjustment.
    """
    # Drop missing values in 'Close' and 'Volume'
    close_prices = df['Close'].dropna().values
    volume_data = df['Volume'].dropna().values

    # Ensure we have enough data
    if len(close_prices) < 2:
        return None

    # Strike Price Adjustment: Using the first day's close as the strike price.
    strike_price = close_prices[0]
    strike_diff_mean = np.mean(close_prices - strike_price)

    # Volume Feature: Average volume over the time span.
    avg_volume = np.mean(volume_data)

    # Price-Based Features
    mean_price = np.mean(close_prices)
    std_price = np.std(close_prices)
    min_price = np.min(close_prices)
    max_price = np.max(close_prices)
    price_change = ((close_prices[-1] - close_prices[0]) / close_prices[0]) if close_prices[0] != 0 else 0

    features = {
        'mean_price': mean_price,
        'std_price': std_price,
        'min_price': min_price,
        'max_price': max_price,
        'price_change': price_change,
        'strike_diff_mean': strike_diff_mean,
        'avg_volume': avg_volume
    }
    return features

def process_index(file_path):
    """
    For a given index Excel file, this function:
      1. Reads and combines all sheets (each sheet represents a stock).
      2. Extracts features for each stock.
      3. Normalizes the features and performs clustering.
      4. Maps clusters to uptrend groups.
      5. Selects up to 20 stocks per group.
    Returns the final clustered DataFrame.
    """
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        return None

    try:
        data = pd.ExcelFile(file_path)
    except Exception as e:
        st.error(f"Error reading Excel file {file_path}: {e}")
        return None

    # Combine all sheets into one DataFrame with a MultiIndex (Stock, Index)
    all_data = {}
    for sheet_name in data.sheet_names:
        try:
            sheet_data = data.parse(sheet_name)
            all_data[sheet_name] = sheet_data
        except Exception as e:
            st.error(f"Error reading sheet {sheet_name}: {e}")
    if not all_data:
        st.error("No valid sheets found in file.")
        return None

    combined_data = pd.concat(all_data.values(), keys=all_data.keys(), names=["Stock", "Index"])

    # Build a features DataFrame, one row per stock.
    feature_data = []
    for stock_symbol, stock_df in combined_data.groupby(level=0):
        feats = extract_features(stock_df)
        if feats:
            feats['Stock'] = stock_symbol
            feature_data.append(feats)
    features_df = pd.DataFrame(feature_data)
    if features_df.empty:
        st.error("No valid stock data found in file.")
        return None

    # Define final features and normalize them.
    final_feature_cols = [
        'mean_price',
        'std_price',
        'min_price',
        'max_price',
        'price_change',
        'strike_diff_mean',
        'avg_volume'
    ]
    scaler = StandardScaler()
    X = scaler.fit_transform(features_df[final_feature_cols])

    # Clustering using silhouette score to select the best k.
    if X.shape[0] < 2:
        st.warning("Only one sample available for clustering. Skipping clustering step.")
        features_df['Cluster'] = 0
    else:
        best_k = None
        best_score = -1
        best_kmeans = None
        for k in range(2, 11):
            kmeans = KMeans(n_clusters=k, random_state=42)
            labels = kmeans.fit_predict(X)
            score = silhouette_score(X, labels)
            if score > best_score:
                best_score = score
                best_k = k
                best_kmeans = kmeans

        if best_kmeans is None:
            st.error("Clustering failed.")
            return None

        if best_score >= 0.95:
            st.success(f"Selected k={best_k} with a silhouette score of {best_score:.4f} (>= 0.95).")
        features_df['Cluster'] = best_kmeans.labels_

    # Map clusters to uptrend groups (e.g., 95%, 90%, 80% Uptrend)
    avg_change = features_df.groupby('Cluster')['price_change'].mean().sort_values(ascending=False)
    cluster_order_by_performance = avg_change.index

    uptrend_labels = ['95% Uptrend', '90% Uptrend', '80% Uptrend']
    cluster_mapping = {}
    for i, cluster_id in enumerate(cluster_order_by_performance):
        if i < len(uptrend_labels):
            cluster_mapping[cluster_id] = uptrend_labels[i]
        else:
            cluster_mapping[cluster_id] = '80% Uptrend (Extra)'
    features_df['Probability_Group'] = features_df['Cluster'].map(cluster_mapping)

    # Select exactly 20 stocks per group (or as many as available)
    def pick_top_20(df_group):
        if len(df_group) >= 20:
            return df_group.sample(n=20, random_state=42)
        else:
            return df_group.head(20)

    final_clusters = (
        features_df.groupby('Probability_Group', group_keys=False)
        .apply(pick_top_20)
        .reset_index(drop=True)
    )
    return final_clusters

def show_page():
    st.title("Stock Clustering - Uptrend Probability")
    
    # Define a dictionary mapping each index to its local Excel file path.
    data_files = {
        "Nifty50": "NIfty50_data.xlsx",
        "Nifty Next 50": "Nifty_Next_50.xlsx",
        "Sensex": "Sensex_data.xlsx",
        "Nifty Midcap 100": "Nifty_Midcap_100.xlsx",
    }

    st.write("Processing clustering for the following indices:")
    for index_name in data_files.keys():
        st.write(f"- {index_name}")

    # Create tabs for each index.
    tabs = st.tabs(list(data_files.keys()))
    for idx, index_name in enumerate(data_files.keys()):
        with tabs[idx]:
            st.header(index_name)
            file_path = data_files[index_name]
            with st.spinner(f"Processing {index_name}..."):
                final_clusters = process_index(file_path)
            if final_clusters is not None:
                st.subheader("Clustered Stocks")
                st.dataframe(final_clusters)
                csv = final_clusters.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{index_name}_clustered_stocks.csv",
                    mime="text/csv"
                )

if __name__ == '_main_':
    show_page()