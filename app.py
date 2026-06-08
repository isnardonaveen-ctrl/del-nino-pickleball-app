import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Del Niño Pickleball Club", page_icon="🏓", layout="wide")
st.markdown("""
    <style>
    /* 1. Main Background */
    .stApp {
        background-color: #013220 !important; 
    }
    
    /* 2. SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #0a4d35 !important;
        border-right: 2px solid #D4AF37 !important;
    }
    
    /* Sidebar Text/Labels */
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }

    /* FORCE COLLAPSE BUTTON TO BE A VISIBLE GOLD BOX */
    button[data-testid="stSidebarCollapseButton"] {
        background-color: #D4AF37 !important; /* Gold background */
        border: none !important;
        border-radius: 5px !important;
        padding: 5px !important;
        width: 35px !important;
        height: 35px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Force the arrow icon to be dark green */
    button[data-testid="stSidebarCollapseButton"] svg {
        fill: #013220 !important;
    }
    
    /* Fix Filter dropdown visibility */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
    }
    div[data-baseweb="select"] span {
        color: #000000 !important; 
    }

    /* Sidebar headers in Gold */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #D4AF37 !important;
    }
    
    /* 3. HUGE WATERMARK LOGO */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url('https://github.com/isnardonaveen-ctrl/del-nino-pickleball-app/blob/main/6832fb4b-7df6-4105-9c8c-7140bfdf4668-removebg-preview.png?raw=true');
        background-repeat: no-repeat;
        background-position: center;
        background-size: 50%;
        opacity: 0.15;
        pointer-events: none;
        z-index: 0;
    }

    /* 4. Text & Table Styling */
    body, p, div, span, h1, h2, h3, h4, h5, h6 { color: #FFFFFF !important; }
    h1, h2, h3 { color: #D4AF37 !important; text-align: center; }
    [data-testid="stDataFrame"] { background-color: #0a4d35 !important; }
    .main .block-container { z-index: 1; position: relative; }
    </style>
    """, unsafe_allow_html=True)
# Create a centered container using empty outer columns
# --- REPLACED HEADER BLOCK ---
# Create one main centered container
# Centered Title (no columns needed now)
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>Del Niño Pickleball Club Tracker</h1>", unsafe_allow_html=True)
st.markdown("---")
# --- END REPLACED BLOCK ---

BASE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1kDSwEA75lTPwv-wNGCnU6IPI2day9D69hgan_xuG7sA/edit?gid=0#gid=0"

@st.cache_data(ttl=5)
def load_live_data(sheet_url):
    try:
        csv_url = sheet_url.split("/edit")[0] + "/gviz/tq?tqx=out:csv"
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        return None

def generate_2026_calendar():
    start_date = datetime(2026, 6, 9)
    end_date = datetime(2026, 12, 31)
    dates, days, venues = [], [], []
    current = start_date
    while current <= end_date:
        if current.weekday() != 6:
            dates.append(current.strftime("%Y-%m-%d"))
            days.append(current.strftime("%A"))
            venues.append("Southside" if current.strftime("%A") in ["Tuesday", "Thursday", "Saturday"] else "Smashville")
        current += timedelta(days=1)
    return pd.DataFrame({"Date": dates, "Day": days, "Venue": venues})

raw_sheet_df = load_live_data(BASE_SHEET_URL)
calendar_df = generate_2026_calendar()

if raw_sheet_df is not None:
    raw_sheet_df.columns = raw_sheet_df.columns.str.strip()
    if "Date" in raw_sheet_df.columns:
        raw_sheet_df["Date"] = raw_sheet_df["Date"].astype(str).str.strip()
        clean_df = pd.merge(calendar_df, raw_sheet_df.dropna(subset=["Date"]), on="Date", how="left")
    else:
        clean_df = calendar_df

    clean_df["Members Count"] = pd.to_numeric(clean_df.get("Members Count", 0), errors='coerce').fillna(0).astype(int)
    clean_df["Non-Members Count"] = pd.to_numeric(clean_df.get("Non-Members Count", 0), errors='coerce').fillna(0).astype(int)
    clean_df["Misc Expenses"] = pd.to_numeric(clean_df.get("Misc Expenses", 0), errors='coerce').fillna(0)
    clean_df["Total Players"] = (clean_df["Members Count"] + clean_df["Non-Members Count"]).astype(int)
    clean_df["Total Collected"] = (clean_df["Members Count"] * 100) + (clean_df["Non-Members Count"] * 150)
    clean_df["Court Cost"] = 3600
    clean_df["Net Cash for Today"] = clean_df.apply(lambda r: (r["Total Collected"] - r["Court Cost"]) - r["Misc Expenses"] if r["Total Players"] > 0 else 0, axis=1)

    # --- ADDED MONTH FILTER ---
    clean_df['Month'] = pd.to_datetime(clean_df['Date']).dt.month_name()
    all_months = clean_df['Month'].unique().tolist()
    
    with st.sidebar:
        st.subheader("📊 Filter Data")
        selected_months = st.multiselect("Select Months:", options=all_months, default=all_months)
    
    if selected_months:
        clean_df = clean_df[clean_df['Month'].isin(selected_months)]
    # --------------------------

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₱{clean_df['Total Collected'].sum():,.2f}")
    col2.metric("Gross Profits", f"₱{clean_df[clean_df['Net Cash for Today'] > 0]['Net Cash for Today'].sum():,.2f}")
    col3.metric("Total Expenses", f"₱{clean_df['Misc Expenses'].sum():,.2f}")
    col4.metric("Actual Cash In Bank", f"₱{clean_df['Net Cash for Today'].sum():,.2f}")
    
    st.markdown("---")

    def highlight_financials(val):
        # We use lighter shades of green and red to ensure they pop against the dark green background
        color = '#76FF7B' if val > 0 else '#FF6B6B' if val < 0 else 'white'
        bg = 'background-color: transparent;'
        return f'color: {color}; {bg} font-weight: bold;'

    tab1, tab2, tab3 = st.tabs(["📅 Live Session Ledger", "💵 Expenses Ledger", "📋 Clipboard Report Generator"])

    with tab1:
        display_df = clean_df[["Date", "Day", "Venue", "Members Count", "Non-Members Count", "Total Players", "Total Collected", "Court Cost", "Misc Expenses", "Net Cash for Today"]]
        st.dataframe(display_df.style.format({
            "Total Collected": "₱{:,.2f}", "Court Cost": "₱{:,.2f}", "Misc Expenses": "₱{:,.2f}", "Net Cash for Today": "₱{:,.2f}",
            "Members Count": "{:.0f}", "Non-Members Count": "{:.0f}", "Total Players": "{:.0f}"
        }).map(highlight_financials, subset=['Net Cash for Today']), use_container_width=True)

    with tab2:
        expense_df = clean_df[clean_df["Misc Expenses"] > 0][["Date", "Venue", "Misc Expenses", "Expenses Remarks"]]
        st.dataframe(expense_df.style.format({"Misc Expenses": "₱{:,.2f}"}), use_container_width=True)

    with tab3:
        st.info("Select a row to generate your Viber report.")
