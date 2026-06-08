import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Del Niño Pickleball Club", page_icon="🏓", layout="wide")

st.title("🏓 Del Niño Pickleball Club Tracker")
st.markdown("---")

# 🟢 PASTE YOUR GOOGLE SHEET URL HERE
BASE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1kDSwEA75lTPwv-wNGCnU6IPI2day9D69hgan_xuG7sA/edit?gid=0#gid=0"

@st.cache_data(ttl=5)
def load_live_data(sheet_url):
    try:
        csv_url = sheet_url.split("/edit")[0] + "/gviz/tq?tqx=out:csv"
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        st.error(f"Sync error: {e}")
        return None

# GENERATE 2026 CALENDAR
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

    # Calculations
    clean_df["Members Count"] = pd.to_numeric(clean_df.get("Members Count", 0), errors='coerce').fillna(0).astype(int)
    clean_df["Non-Members Count"] = pd.to_numeric(clean_df.get("Non-Members Count", 0), errors='coerce').fillna(0).astype(int)
    clean_df["Misc Expenses"] = pd.to_numeric(clean_df.get("Misc Expenses", 0), errors='coerce').fillna(0)
    
    clean_df["Total Players"] = (clean_df["Members Count"] + clean_df["Non-Members Count"]).astype(int)
    clean_df["Total Collected"] = (clean_df["Members Count"] * 100) + (clean_df["Non-Members Count"] * 150)
    clean_df["Court Cost"] = 3600
    
    clean_df["Net Cash for Today"] = clean_df.apply(
        lambda r: (r["Total Collected"] - r["Court Cost"]) - r["Misc Expenses"] if r["Total Players"] > 0 else 0, axis=1
    )

    # Dashboard Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₱{clean_df['Total Collected'].sum():,.2f}")
    col2.metric("Gross Profits", f"₱{clean_df[clean_df['Net Cash for Today'] > 0]['Net Cash for Today'].sum():,.2f}")
    col3.metric("Total Expenses", f"₱{clean_df['Misc Expenses'].sum():,.2f}")
    col4.metric("Actual Cash In Bank", f"₱{clean_df['Net Cash for Today'].sum():,.2f}")
    
    st.markdown("---")
    
    # 🎨 COLOR HIGHLIGHTING LOGIC
    def highlight_financials(val):
        color = '#375623' if val > 0 else '#C00000' if val < 0 else 'black'
        bg = '#E2EFDA' if val > 0 else '#FCE4D6' if val < 0 else ''
        return f'color: {color}; background-color: {bg}; font-weight: bold;'

    st.subheader("Live Session Ledger")
    
    display_df = clean_df[[
        "Date", "Day", "Venue", "Members Count", "Non-Members Count", 
        "Total Players", "Total Collected", "Court Cost", "Misc Expenses", "Net Cash for Today"
    ]]
    
    st.dataframe(display_df.style.format({
        "Total Collected": "₱{:,.2f}", 
        "Court Cost": "₱{:,.2f}", 
        "Misc Expenses": "₱{:,.2f}", 
        "Net Cash for Today": "₱{:,.2f}",
        "Members Count": "{:.0f}",
        "Non-Members Count": "{:.0f}",
        "Total Players": "{:.0f}"
    }).applymap(highlight_financials, subset=['Net Cash for Today']), use_container_width=True)
