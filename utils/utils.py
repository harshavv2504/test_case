import streamlit as st
import pandas as pd

def load_css(file_path):
    """
    Loads a CSS file from an absolute path and applies it to the Streamlit app.
    This function is now compatible with the Path object from constants.py.
    """
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Error: CSS file not found at the specified path: {file_path}")
    except Exception as e:
        st.error(f"An error occurred while loading CSS: {e}")

def format_indian_currency(value):
    """
    Formats a number into Indian Rupees (INR) format (e.g., 1,23,456).
    Your original formatting logic is preserved.
    """
    if not pd.api.types.is_number(value) or pd.isna(value):
        return 'N/A'
        
    s = str(int(value))
    if len(s) <= 3:
        return s
    last_three = s[-3:]
    other_numbers = s[:-3]

    other_numbers_rev = other_numbers[::-1]
    formatted_other_numbers_rev = ''
    for i, char in enumerate(other_numbers_rev):
        formatted_other_numbers_rev += char
        if (i + 1) % 2 == 0 and (i + 1) != len(other_numbers_rev):
            formatted_other_numbers_rev += ','

    return formatted_other_numbers_rev[::-1] + ',' + last_three

# Your original commented-out function is preserved.
# @st.cache_data
# def to_csv(df):
#     """Converts a DataFrame to a CSV string for downloading."""
#     return df.to_csv(index=False).encode('utf-8')
