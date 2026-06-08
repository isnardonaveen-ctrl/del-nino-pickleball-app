import streamlit as st
import pandas as pd

# 1. Page Configuration Setup
st.set_page_config(page_title="Del Niño Pickleball Club", page_icon="🏓", layout="wide")

st.title("🏓 Del Niño Pickleball Club Dashboard")
st.markdown("### Running Management & Cash Flow Hub")
st.markdown("---")

# 🟢 YOUR NEW LIVE MULTI-TAB GOOGLE SHEET DATABASE LINK
BASE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1U10CeH9VqpCnheUfXsesUR3GeYDNvhO8gIcz4b15aR4/edit"

@st.cache_data(ttl=10)  # Fast 10-second automatic background refresh loop
def load_live_data(sheet_url):
    try:
        # Connects directly to the main spreadsheet data stream (gid=0)
        csv_url = sheet_url.split("/edit")[0] + "/export?format=csv&gid=0"
        raw_df = pd.read_csv(csv_url, header=None)
        
        # Automatically scans rows to find exactly where your data column headers start
        header_row_idx = 0
        for idx, row in raw_df.iterrows():
            if "Date" in row.values and "Total Collected" in row.values:
                header_row_idx = idx
                break
                
        df = pd.read_csv(csv_url, skiprows=header_row_idx)
        return df
    except Exception as e:
        st.error(f"Error fetching data from cloud database stream: {e}")
        return None

df = load_live_data(BASE_SHEET_URL)

if df is not None:
    # Clean up hidden formatting spaces out of row titles
    df.columns = df.columns.str.strip()
    
    # Isolate real row entries and filter out empty background template rows
    if "Date" in df.columns:
        clean_df = df.dropna(subset=["Date"]).copy()
        clean_df = clean_df[clean_df["Date"].str.contains(r'\d{4}', na=False)]
    else:
        clean_df = df.copy()
        
    # Standardize textual cell properties into true calculation numbers 
    numeric_cols = ["Total Collected", "Session Profit/Loss", "Misc Expenses", "Members Count", "Non-Members Count", "Total Players"]
    for col in numeric_cols:
        if col in clean_df.columns:
            clean_df[col] = pd.to_numeric(clean_df[col].astype(str).str.replace('₱', '').str.replace(',', ''), errors='coerce').fillna(0)
        else:
            clean_df[col] = 0

    # Operational Capital Metrics Calculations
    total_revenue = clean_df["Total Collected"].sum()
    gross_profits = clean_df[clean_df["Session Profit/Loss"] > 0]["Session Profit/Loss"].sum()
    total_expenses = clean_df["Misc Expenses"].sum()
    cash_in_bank = gross_profits - total_expenses

    # Display Visual Dashboard KPI Information Grid
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Open Play Revenue", f"₱{total_revenue:,.2f}")
    col2.metric("Gross Play Profits", f"₱{gross_profits:,.2f}")
    col3.metric("Total Club Expenses", f"₱{total_expenses:,.2f}")
    col4.metric("Actual Cash In Bank", f"₱{cash_in_bank:,.2f}")
    
    st.markdown("---")
    
    # 2. Main Web Layout Navigation Tabs Definition
    tab1, tab2, tab3 = st.tabs(["📅 Live Session Ledger", "💵 Expenses Ledger (2nd Sheet)", "📋 Clipboard Report Generator"])
    
    with tab1:
        st.subheader("Rolling Activity Records")
        
        # Colorizer function for dynamic Green / Red table indicators
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

        styled_df = clean_df.style.apply(highlight_financials, axis=1)
        st.dataframe(styled_df, use_container_width=True, height=400)
        
    with tab2:
        st.subheader("Automated Club Expense Tracker")
        st.caption("This view isolates all lines where custom club or venue costs were logged.")
        
        # Extracts row entries with active expenses automatically
        if "Misc Expenses" in clean_df.columns:
            expense_mask = clean_df["Misc Expenses"] > 0
            expenses_df = clean_df[expense_mask][["Date", "Venue", "Misc Expenses", "Expenses Remarks"]].copy()
            expenses_df.columns = ["Expense Date", "Venue Context", "Amount Paid", "Expense Remarks / Description"]
            
            if len(expenses_df) > 0:
                st.dataframe(expenses_df.style.format({"Amount Paid": "₱{:,.2f}"}), use_container_width=True)
                st.metric("Total Logged Expenses Balance", f"₱{total_expenses:,.2f}")
            else:
                st.info("No club expenses recorded yet! Add miscellaneous expenses directly to your Google Sheet to populate this tab.")
        
    with tab3:
        st.subheader("Viber / Messenger Clipboard Template")
        if len(clean_df) > 0:
            # Interactive row indexing slider widget tool
            selected_row_idx = st.slider("Select Row Sequence", min_value=0, max_value=len(clean_df)-1, value=0)
            row_data = clean_df.iloc[selected_row_idx]
            
            # Generates daily copy-paste summaries automatically
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
