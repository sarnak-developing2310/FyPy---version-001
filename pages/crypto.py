import streamlit as st
import pandas as pd
import numpy as np
import os
import time
from datetime import datetime, timedelta
from sklearn.cluster import KMeans

# ============
# DATA LOADING
# ============

def load_data(file_path):
    """
    Load an Excel file with multiple sheets from the local filesystem.
    Combines all sheets into one DataFrame with a MultiIndex (Coin, Index).
    """
    try:
        excel_file = pd.ExcelFile(file_path)
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

    all_data = {}
    for sheet_name in excel_file.sheet_names:
        try:
            sheet_data = excel_file.parse(sheet_name)
            all_data[sheet_name] = sheet_data
        except Exception as e:
            st.write(f"Error reading sheet {sheet_name}: {e}")
    if not all_data:
        st.error("No sheets were loaded successfully.")
        return None

    combined_data = pd.concat(all_data.values(), keys=all_data.keys(), names=["Coin", "Index"])
    return combined_data

# ============
# FEATURE EXTRACTION
# ============

def extract_features(data):
    # Ensure required columns are present and sort by date
    prices = data[['date', 'price']].dropna().sort_values('date')
    if len(prices) < 2:
        return None

    prices['date'] = pd.to_datetime(prices['date'])
    first_date = prices['date'].iloc[0]
    last_date = prices['date'].iloc[-1]
    age_in_days = (last_date - first_date).days
    age_in_months = round(age_in_days / 30.44, 2)

    # Calculate percentage change over the last 'days' days
    def calculate_price_change(days):
        if len(prices) >= days:
            start_price = prices['price'].iloc[-days]
            end_price = prices['price'].iloc[-1]
            return ((end_price - start_price) / start_price) * 100 if start_price != 0 else 0
        return None

    price_changes = {
        'price_change_24h': calculate_price_change(2),
        'price_change_7d': calculate_price_change(7),
        'price_change_14d': calculate_price_change(14),
        'price_change_30d': calculate_price_change(30)
    }

    # Replace missing changes with default values (0)
    for key in price_changes:
        if price_changes[key] is None:
            price_changes[key] = 0

    # Filter out coins based on conditions
    if (price_changes['price_change_24h'] < 0 and price_changes['price_change_7d'] < 0) or (price_changes['price_change_30d'] < -50):
        return None

    features = {
        'mean_price': np.mean(prices['price']),
        'std_price': np.std(prices['price']),
        'min_price': np.min(prices['price']),
        'max_price': np.max(prices['price']),
        'volatility': np.std(prices['price']) / np.mean(prices['price']) if np.mean(prices['price']) != 0 else 0,
        'price_change': (prices['price'].iloc[-1] - prices['price'].iloc[0]) / prices['price'].iloc[0] if prices['price'].iloc[0] != 0 else 0,
        'token': data['token'].iloc[0] if 'token' in data.columns else None,
        'contract_address': data['contract_address'].iloc[0] if 'contract_address' in data.columns else None,
        'market_cap': data['market_cap'].dropna().iloc[-1] if 'market_cap' in data.columns else None,
        'age_in_months': age_in_months,
        'Chain': data['platform'].iloc[0] if 'platform' in data.columns else None,
        'Trading Volume': data['volume'].dropna().iloc[-1] if 'volume' in data.columns else None,
        'twitter_followers': data['twitter_followers'].iloc[0] if 'twitter_followers' in data.columns else None,
        'price': prices['price'].iloc[-1],
        'prediction_date': data['date'].iloc[-1],
    }
    features.update(price_changes)
    return features

# ============
# PREDICTION RECORDING & EVALUATION
# ============

def record_predictions(prediction_df, record_file='predictions_log.csv'):
    """
    Record prediction data to a CSV log.
    """
    prediction_df = prediction_df.copy()
    prediction_df['date'] = pd.Timestamp.now()
    if os.path.exists(record_file):
        prediction_df.to_csv(record_file, mode='a', header=False, index=False)
    else:
        prediction_df.to_csv(record_file, index=False)
    st.write(f"Predictions recorded to {record_file}")

def evaluate_predictions(n_days=3, record_file='predictions_log.csv', updated_data=None):
    """
    Evaluate predictions older than n_days by comparing predicted price with latest actual price.
    """
    if not os.path.exists(record_file):
        st.write("No prediction log file found for evaluation.")
        return

    predictions_log = pd.read_csv(record_file)
    predictions_log['date'] = pd.to_datetime(predictions_log['date'])
    cutoff_date = pd.Timestamp.now() - timedelta(days=n_days)
    old_predictions = predictions_log[predictions_log['date'] <= cutoff_date]

    if old_predictions.empty:
        st.write(f"No predictions older than {n_days} days to evaluate.")
        return

    errors = []
    error_details = []
    for idx, row in old_predictions.iterrows():
        coin = row['Coin']
        predicted_price = row['price']
        try:
            coin_data = updated_data.loc[coin]
            if isinstance(coin_data, pd.DataFrame):
                actual_price = coin_data['price'].dropna().iloc[-1]
            else:
                actual_price = coin_data['price']
        except Exception as e:
            st.write(f"Could not retrieve data for coin {coin}: {e}")
            continue

        error = actual_price - predicted_price
        errors.append(abs(error))
        error_details.append({
            'Coin': coin,
            'Predicted_Price': predicted_price,
            'Actual_Price': actual_price,
            'Error': error,
            'date': row['date']
        })

    if errors:
        mae = np.mean(errors)
        st.write(f"Mean Absolute Error over predictions older than {n_days} days: {mae:,.4f}")
        errors_df = pd.DataFrame(error_details)
        st.dataframe(errors_df)
    else:
        st.write("No valid predictions were evaluated.")

# ============
# MODEL RETRAINING & CLUSTERING
# ============

def retrain_model(combined_data, record_file='predictions_log.csv'):
    try:
        st.write("Starting model retraining...")
        feature_data = []
        # Process each coin (MultiIndex level 0)
        for coin, coin_data in combined_data.groupby(level=0):
            features = extract_features(coin_data)
            if features:
                features['Coin'] = coin
                feature_data.append(features)
        if not feature_data:
            st.write("No valid features extracted for retraining.")
            return None

        features_df = pd.DataFrame(feature_data)
        # Convert numerical fields if needed
        for col in ['market_cap', 'Trading Volume']:
            if col in features_df.columns:
                features_df[col] = pd.to_numeric(features_df[col], errors='coerce')

        # Normalize selected numerical columns for clustering
        norm_columns = ['mean_price', 'std_price', 'volatility', 'price_change']
        features_normalized = features_df[norm_columns].apply(lambda x: (x - x.mean()) / x.std())

        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        features_df['Cluster'] = kmeans.fit_predict(features_normalized)

        # Map clusters to probability groups based on average price_change
        cluster_mapping = features_df.groupby('Cluster')['price_change'].mean().sort_values(ascending=False).index
        mapping_dict = {}
        if len(cluster_mapping) >= 3:
            mapping_dict = {cluster_mapping[0]: '90% Uptrend',
                            cluster_mapping[1]: '80% Uptrend',
                            cluster_mapping[2]: '70% Uptrend'}
        features_df['Probability_Group'] = features_df['Cluster'].map(mapping_dict)

        # Filter coins based on Trading Volume and market_cap thresholds
        filtered_features = features_df[
            (features_df['Trading Volume'] >= 50000) & (features_df['market_cap'] >= 1_000_000)
        ]

        # Select up to 20 coins per probability group
        final_clusters = filtered_features.groupby('Probability_Group', group_keys=False).apply(
            lambda x: x.sample(n=20, random_state=42) if len(x) >= 20 else x.head(20)
        )

        # Append current timestamp
        final_clusters['date'] = pd.Timestamp.now()

        # Reformat fields for display
        for col in ['market_cap', 'Trading Volume']:
            final_clusters[col] = final_clusters[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else x)

        st.write("Retrained Clusters (Predictions):")
        st.dataframe(final_clusters)

        # Log the predictions
        record_predictions(final_clusters, record_file=record_file)
        st.write("Model retraining completed successfully.")
        return final_clusters
    except Exception as e:
        st.error(f"Error encountered during retraining: {e}")
        raise

# ============
# MAIN STREAMLIT APP
# ============

def show_page():
    st.title("Memecoin Clustering and Prediction")

    # Specify the local file path (this will later be replaced by data from MongoDB)
    file_path = "memecoin.xlsx"  # Ensure this file exists on your local machine

    if not os.path.exists(file_path):
        st.error(f"Data file not found at {file_path}. Please ensure the file exists.")
        return

    combined_data = load_data(file_path)
    if combined_data is None:
        st.error("Failed to load data.")
        return

    st.write("Data loaded successfully. Preview of the combined data:")
    st.dataframe(combined_data.head())

    # Optionally evaluate old predictions if available
    if os.path.exists('predictions_log.csv'):
        st.subheader("Evaluating Old Predictions")
        evaluate_predictions(n_days=3, record_file='predictions_log.csv', updated_data=combined_data)

    if st.button("Run Clustering and Retraining"):
        final_clusters = None
        retry_delay_seconds = 60
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                final_clusters = retrain_model(combined_data, record_file='predictions_log.csv')
                break
            except Exception as e:
                retries += 1
                st.write(f"Retraining failed (attempt {retries}/{max_retries}). Retrying in {retry_delay_seconds} seconds...")
                time.sleep(retry_delay_seconds)
        else:
            st.error("Max retries reached. Please check the error logs and data integrity.")
            return

        if final_clusters is not None:
            csv = final_clusters.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Final Clustered Coins CSV",
                data=csv,
                file_name="final_clustered_coins.csv",
                mime="text/csv"
            )

if __name__== '_main_':
    show_page()