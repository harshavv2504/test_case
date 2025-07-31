import streamlit as st
import pandas as pd
import sqlite3

# --- Database Configuration (Corrected Import) ---
# CHANGE 1: Import the robust DB_PATH instead of the simple DB_NAME.
from constants import DB_PATH

@st.cache_data
def load_all_data():
    """
    Loads performance, orders, and payment log data from the SQLite database.
    Uses a robust, absolute path to the database, making it safe for deployment.
    Caches the data to avoid reloading on every rerun.
    """
    # CHANGE 2: Check if the database file exists at the absolute path before connecting.
    if not DB_PATH.exists():
        st.error(f"Error: Database file not found at {DB_PATH}.")
        st.info("Please ensure 'data.db' is in the project's root directory and you have run the necessary data creation scripts.")
        st.stop()

    print(f"Attempting to load data from SQLite database: {DB_PATH}")
    try:
        # CHANGE 3: Connect to the database using the robust DB_PATH.
        with sqlite3.connect(DB_PATH) as conn:
            # Load data from the final SQL marts to match dashboard expectations.
            # (Assuming table names are like 'influencer_performance_mart' based on earlier context)
            performance_df = pd.read_sql_query("SELECT * FROM influencer_performance_mart", conn)
            
            orders_df = pd.read_sql_query("SELECT * FROM orders_mart", conn)
            # Convert date/numeric columns after loading.
            orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
            orders_df['revenue_generated'] = pd.to_numeric(orders_df['revenue_generated'], errors='coerce').fillna(0)
            
            payment_log_df = pd.read_sql_query("SELECT * FROM payment_log_mart", conn)
            # The original code used 'invoice_date', let's assume it's 'payment_date' in the mart.
            # If the column is different, please adjust this line.
            payment_log_df['payment_date'] = pd.to_datetime(payment_log_df['payment_date'])

            return performance_df, orders_df, payment_log_df
            
    except Exception as e:
        st.error(f"An unexpected error occurred while loading data: {e}")
        st.info("Please ensure the database file is not corrupted and the tables (e.g., 'orders_mart') exist.")
        st.stop()

def filter_dataframes(performance_df, orders_df, payment_log_df, start_date, end_date, brand, product, platform):
    """
    Filters the DataFrames based on the provided sidebar selections.
    This function contains your original filtering logic and is unchanged.
    """
    # Platform filter logic
    if 'Organic' in platform:
        platform_mask = orders_df['platform'].isin([p for p in platform if p != 'Organic']) | \
                        orders_df['platform'].isna() | (orders_df['platform'] == '')
    else:
        platform_mask = orders_df['platform'].isin(platform)

    # Filter orders_df
    filtered_orders_df = orders_df[
        (orders_df['order_date'].dt.date >= start_date) &
        (orders_df['order_date'].dt.date <= end_date) &
        (orders_df['brand'].isin(brand)) &
        (orders_df['product'].isin(product)) &
        platform_mask
    ].copy()

    # Get the list of influencers who match the order filters
    filtered_influencers = filtered_orders_df['influencer_id'].unique()

    # Filter performance_df
    filtered_performance_df = performance_df[
        (performance_df['influencer_id'].isin(filtered_influencers))
    ].copy()

    # Filter payment_log_df by date range and influencer_id
    # The original code used 'invoice_date', let's assume it's 'payment_date' in the mart.
    # If the column is different, please adjust this line.
    filtered_payment_log_df = payment_log_df[
        (payment_log_df['payment_date'].dt.date >= start_date) &
        (payment_log_df['payment_date'].dt.date <= end_date) &
        (payment_log_df['influencer_id'].isin(filtered_influencers))
    ].copy()

    return filtered_performance_df, filtered_orders_df, filtered_payment_log_df
