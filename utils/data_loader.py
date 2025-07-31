import streamlit as st
import pandas as pd
import sqlite3

# Import the robust DB_PATH from the corrected constants.py
from constants import DB_PATH

@st.cache_data
def load_all_data():
    """
    Loads performance, orders, and payment log data from the SQLite database
    using the correct table names.
    """
    if not DB_PATH.exists():
        st.error(f"Error: Database file not found at {DB_PATH}.")
        st.info("Please ensure 'data.db' is in the project's root directory.")
        st.stop()

    print(f"Attempting to load data from SQLite database: {DB_PATH}")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # CHANGE: The SQL queries now use the original table names from your database.
            performance_df = pd.read_sql_query("SELECT * FROM influencer_performance", conn)
            
            orders_df = pd.read_sql_query("SELECT * FROM enriched_orders", conn)
            orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
            orders_df['revenue_generated'] = pd.to_numeric(orders_df['revenue_generated'], errors='coerce').fillna(0)
            
            payment_log_df = pd.read_sql_query("SELECT * FROM payments_log", conn)
            # Your original code used 'invoice_date'. This is preserved.
            payment_log_df['invoice_date'] = pd.to_datetime(payment_log_df['invoice_date'])

            return performance_df, orders_df, payment_log_df
            
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        st.info("Please ensure the database file is not corrupted and the tables 'influencer_performance', 'enriched_orders', and 'payments_log' exist.")
        st.stop()

def filter_dataframes(performance_df, orders_df, payment_log_df, start_date, end_date, brand, product, platform):
    """
    Filters the DataFrames based on the provided sidebar selections.
    Your original filtering logic is preserved.
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
    # Your original code used 'invoice_date'. This is preserved.
    filtered_payment_log_df = payment_log_df[
        (payment_log_df['invoice_date'].dt.date >= start_date) &
        (payment_log_df['invoice_date'].dt.date <= end_date) &
        (payment_log_df['influencer_id'].isin(filtered_influencers))
    ].copy()

    return filtered_performance_df, filtered_orders_df, filtered_payment_log_df
