import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF

st.set_page_config(page_title="Del Niño Pickleball Club", page_icon="🏓", layout="wide")

st.markdown("""
    <style>
    /* 1. Main Background */
    .stApp { background-color: #013220 !important; }
    
    /* 2. SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #0a4d35 !important;
        border-right: 2px solid #D4AF37 !important;
    }
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: #FFFFFF !important; }

    /* FORCE COLLAPSE BUTTON TO BE A VISIBLE GOLD BOX */
    button[data-testid="stSidebarCollapseButton"] {
        background-color: #D4AF37 !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 5px !important;
        width: 35px !important;
        height: 35px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    button[data-testid="stSidebarCollapseButton"] svg { fill: #013220 !important; }

    /* Sidebar headers in Gold */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #D4AF37 !important; }

    /* 3. DROPDOWN (SELECTBOX) & INPUTS - HIGH CONTRAST FIX */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 3px solid #D4AF37 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #000000 !important;
    }
    div[role="listbox"] { background-color: #FFFFFF !important; }
    div[role="listbox"] span { color: #000000 !important; font-weight: bold !important; }

    /* 4. BUTTONS - HIGH CONTRAST */
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #013220 !important;
        font-weight: bold !important;
        border: 2px solid #FFFFFF !important;
    }
    div.stDownloadButton > button {
        background-color: #76FF7B !important;
        color: #013220 !important;
        font-weight: bold !important;
        border: 2px solid #FFFFFF !important;
    }

    /* 5. LABELS */
    div[data-testid="stWidgetLabel"] p, label {
        color: #D4AF37 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }

    /* 6. WATERMARK LOGO */
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('https://github.com/isnardonaveen-ctrl/del-nino-pickleball-app/blob/main/6832fb4b-7df6-4105-9c8c-7140bfdf4668-removebg-preview.png?raw=true');
        background-repeat: no-repeat; background-position: center; background-size: 50%;
        opacity: 0.15; pointer-events: none; z-index: 0;
    }
    
    /* 7. Text & Table Styling */
    body, p, h1, h2, h3, h4, h5, h6 { color: #FFFFFF !important; }
    h1, h2, h3 { color: #D4AF37 !important; text-align: center; }
    [data-testid="stDataFrame"] { background-color: #0a4d35 !important; }
    .main .block-container { z-index: 1; position: relative; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #D4AF37;'>Del Niño Pickleball Club Tracker</h1>", unsafe_allow_html=True)
st.markdown("---")

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

def generate_monthly_report(df, month_name):
    pdf = FPDF()
    pdf.add_page()
    
    # Title Configuration
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(
