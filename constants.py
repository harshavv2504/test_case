from pathlib import Path

# --- Define Project Root ---
# This is the crucial change. It finds the absolute path of the project's
# root directory by locating this file (constants.py). This makes all other
# file paths reliable, no matter where the app is run from.
ROOT_DIR = Path(__file__).resolve().parent

# --- UI Colors for KPI Cards and Charts ---
# Your original color constants remain unchanged.
LIGHT_COLORS = [
    "#E3F2FD",  # Light Blue (similar to powder blue)
    "#E8F5E9",  # Mint Green (existing, good)
    "#FFFDE7",  # Pale Yellow (very light cream)
    "#F3E5F5",  # Soft Lavender (existing, good)
    "#FFEBEE",  # Blush Pink (existing, good)
    "#F5F5F5",  # Very Light Grey (neutral base)
    "#DDF9F8"   # Light Aqua
]

CHART_COLORS = [
    '#66C2A5', '#FC8D62', '#8DA0CB', '#E78AC3', '#A6D854', '#FFD92F', '#E5C494', '#B3B3B3', '#8C96C6', '#8C628C',
    '#D0D1E6', '#A1D99B', '#43A2CA', '#FED98E', '#C7E9B4', '#7FCDSA', '#FDBB84', '#FDD49E', '#E0F3DB', '#CCEBC5',
    '#A8DDB5', '#7BCCC4', '#4EB3D3', '#2B8CBE', '#08589E', '#F7FCFD', '#E0ECF4', '#BFD3E6', '#9EBCDA', '#8C96C6'
]

# --- Business Logic Constants ---
# Your original profit margin factor remains unchanged.
PROFIT_MARGIN_FACTOR = 0.45 # Assumes 45% of total revenue is gross profit (1 - 0.55 COGS)

# --- File Paths & Database Configuration (Corrected for Deployment) ---
# The file paths are now built from the ROOT_DIR to be absolute and reliable.

# Path to the SQLite database file.
DB_PATH = ROOT_DIR / 'data.db'

# Path to the static assets folder
STATIC_DIR = ROOT_DIR / 'static'

# Path to the page icon inside the 'static' folder
PAGE_ICON_PATH = STATIC_DIR / "New Project.png"

# Path to the main CSS file
CSS_PATH = ROOT_DIR / "style.css"


# --- Table Styling (for Streamlit's st.dataframe if custom HTML styling is needed) ---
# Your original table styles remain unchanged.
TABLE_BASE_STYLES = [
    {'selector': 'th, td', 'props': [('padding', '0.2rem 0.4rem'), ('font-size', '0.85rem'), ('text-align', 'left')]},
    {'selector': 'th', 'props': [('font-weight', 'bold')]}
]
TABLE_HEADER_CENTER_STYLE = [{'selector': 'th', 'props': [('text-align', 'center')]}]
