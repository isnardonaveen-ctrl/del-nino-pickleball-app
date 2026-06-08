import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page Window Config Setup
st.set_page_config(page_title="Del Niño Pickleball Club", page_icon="🏓", layout="wide")

st.title("🏓 Del Niño Pickleball Club Dashboard")
st.markdown("### Running Management & Cash Flow Hub (Auto-Calendar 2026)")
st.markdown("---")

# 🟢 PASTE YOUR NEW GOOGLE SHEET URL HERE
BASE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1kDSwEA75lTPwv-wNGCnU6IPI2day9D69hgan_xuG7sA/edit?gid=0#gid=0"

@st.cache_data(ttl=5)  # 5-second fast auto-refresh
def load_live_data(sheet_url):
    try:
        csv_url = sheet_url.split("/edit")[0] + "/gviz/tq?tqx=out:csv"
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        st.error(f"Database sync handshake interrupted: {e}")
        return None

# 📅 AUTOMATED CALENDAR GENERATOR (Generates June 9 to Dec 31, 2026)
def generate_2026_calendar():
    start_date = datetime(2026, 6, 9)
    end_date = datetime(2026, 12, 31)
    
    dates = []
    days = []
    venues = []
    
    current = start_date
    while current <= end_date:
        # Exclude Sundays (assuming open play runs Mon-Sat)
        if current.weekday() != 6:  
            dates.append(current.strftime("%Y-%m-%d"))
            days.append(current.strftime("%A"))
            # Alternate venues based on days
            if current.strftime("%A") in ["Tuesday", "Thursday", "Saturday"]:
                venues.append("Southside")
            else:
                venues.append("Smashville")
        current += timedelta(days=1)
        
    return pd.DataFrame({"Date": dates, "Day": days, "Venue": venues})

raw_sheet_df = load_live_data(BASE_SHEET_URL)
calendar_df = generate_2026_calendar()

if raw_sheet_df is not None:
    # Clean headers
    raw_sheet_df.columns = raw_sheet_df.columns.str.strip()
    
    # Clean user inputs from Google Sheet
    if "Date" in raw_sheet_df.columns:
        raw_sheet_df["Date"] = raw_sheet_df["Date"].astype(str).str.strip()
        raw_sheet_df = raw_sheet_df.dropna(subset=["Date"])
    
    # Merge the user inputs into the master generated 2026 calendar framework
    clean_df = pd.merge(calendar_df, raw_sheet_df, on="Date", how="left")
    
    # Fill empty/unplayed days with zero values automatically
    clean_df["Members Count"] = pd.to_numeric(clean_df.get("Members Count", 0), errors='coerce').fillna(0).astype(int)
    clean_df["Non-Members Count"] = pd.to_numeric(clean_df.get("Non-Members Count", 0), errors='coerce').fillna(0).astype(int)
    clean_df["Misc Expenses"] = pd.to_numeric(clean_df.get("Misc Expenses", 0), errors='coerce').fillna(0)
    clean_df["Expenses Remarks"] = clean_df.get("Expenses Remarks", "").fillna("None")
    
    # System Fees Fixed Constants
    clean_df["Member Fee"] = 100
    clean_df["Non-Member Fee"] = 150
    clean_df["Court Cost"] = 3600
    
    # Live Financial Math Calculations
    clean_df["Total Players"] = clean_df["Members Count"] + clean_df["Non-Members Count"]
    clean_df["Total Collected"] = (clean_df["Members Count"] * clean_df["Member Fee"]) + (clean_df["Non-Members Count"] * clean_df["Non-Member Fee"])
    
    # Session profit calculation runs ONLY if players are present
    clean_df["Session Profit/Loss"] = clean_df.apply(
        lambda r: r["Total Collected"] - r["Court Cost"] if r["Total Players"] > 0 else 0, axis=1
    )

    # Global KPI Summary Logic
    total_revenue = clean_df["Total Collected"].sum()
    gross_profits = clean_df[clean_df["Session Profit/Loss"] > 0]["Session Profit/Loss"].sum()
    total_expenses = clean_df["Misc Expenses"].sum()
    cash_in_bank = gross_profits - total_expenses

    # Metric Dashboard Layout View
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Open Play Revenue", f"₱{total_revenue:,.2f}")
    col2.metric("Gross Play Profits", f"₱{gross_profits:,.2f}")
    col3.metric("Total Club Expenses", f"₱{total_expenses:,.2f}")
    col4.metric("Actual Cash In Bank", f"₱{cash_in_bank:,.2f}")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📅 Live Session Ledger", "💵 Expenses Ledger (2nd Sheet)", "📋 Clipboard Report Generator"])
    
    with tab1:
        st.subheader("2026 Master Activity Records")
        
        final_ledger_cols = ["Date", "Day", "Venue", "Members Count", "Non-Members Count", "Total Players", "Total Collected", "Court Cost", "Session Profit/Loss", "Misc Expenses", "Expenses Remarks"]
        ledger_display = clean_df[final_ledger_cols].copy()
        
        def highlight_financials(row):
            formats = [''] * len(row)
            if "Session Profit/Loss" in row.index:
                val = row["Session Profit/Loss"]
                idx = row.index.get_loc("Session Profit/Loss")
                if val > 0:
                    formats[idx] = 'background-color: #E2EFDA; color: #375623; font-weight: bold;'
                elif val < 0:
                    formats[idx] = 'background-color: #FCE4D6; color: #C00000; font-weight: bold;'
            return formats

        styled_df = ledger_display.style.apply(highlight_financials, axis=1).format({
            "Total Collected": "₱{:,.2f}", "Court Cost": "₱{:,.2f}", "Session Profit/Loss": "₱{:,.2f}", "Misc Expenses": "₱{:,.2f}"
        })
        st.dataframe(styled_df, use_container_width=True, height=450)
        
    with tab2:
        st.subheader("Automated Club Expense Tracker")
        expense_mask = clean_df["Misc Expenses"] > 0
        expenses_df = clean_df[expense_mask][["Date", "Venue", "Misc Expenses", "Expenses Remarks"]].copy()
        
        if len(expenses_df) > 0:
            st.dataframe(expenses_df.style.format({"Misc Expenses": "₱{:,.2f}"}), use_container_width=True)
            st.metric("Total Logged Expenses Balance", f"₱{total_expenses:,.2f}")
        else:
            st.info("No club expenses recorded yet! Add a value to the 'Misc Expenses' column in your sheet to automatically see it populate.")
        
    with tab3:
        st.subheader("Viber / Messenger Clipboard Template")
        if len(clean_df) > 0:
            selected_row_idx = st.slider("Select Row Sequence", min_value=0, max_value=len(clean_df)-1, value=0)
            row_data = clean_df.iloc[selected_row_idx]
            
            flash_report = f"""🏓 *DEL NIÑO PICKLEBALL CLUB - DAILY OPEN PLAY REPORT*
---------------------------------------------------------------------
*Date:* {row_data.get('Date', 'N/A')}  |  *Venue:* {row_data.get('Venue', 'N/A')}

👥 *ATTENDANCE PROFILE:*
 • Registered Club Members: {int(row_data.get('Members Count', 0))} -> (₱100 each)
 • Non-Member Attendees: {int(row_data.get('Non-Members Count', 0))} -> (₱150 each)
 • Total Players On-Court: {int(row_data.get('Total Players', 0))} / 40 Capacity Limit

💰 *TODAY'S FINANCIAL BREAKDOWN:*
 • Total Fees Collected: ₱{row_data.get('Total Collected', 0):,.2f}
 • Venue Court Rental Cost: ₱3,600.00 (Fixed)
 • Miscellaneous Expense: ₱{row_data.get('Misc Expenses', 0):,.2f}
 • Expense Remarks: {row_data.get('Expenses Remarks', 'None')}
 -----------------------------------------------------------------
 ⚡ *TODAY'S NET SESSION BALANCE:* ₱{row_data.get('Session Profit/Loss', 0):,.2f}

🏦 *CLUB RUNNING ACCUMULATION (YTD):*
 • Total Open Play Revenue: ₱{total_revenue:,.2f}
 • Gross Session Profits: ₱{gross_profits:,.2f}
 • Total Club Expenses: ₱{total_expenses:,.2f}
 🚀 *CURRENT CASH IN BANK:* ₱{cash_in_bank:,.2f}"""

            st.text_area("Highlight and Copy Text Box Below:", value=flash_report, height=400)
