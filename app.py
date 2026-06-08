import streamlit as st
import pandas as pd

# Page Window Config Setup
st.set_page_config(page_title="Del Niño Pickleball Club", page_icon="🏓", layout="wide")

st.title("🏓 Del Niño Pickleball Club Dashboard")
st.markdown("### Running Management & Cash Flow Hub")
st.markdown("---")

# 🟢 LINKED DIRECTLY TO YOUR CLEAN SHEET TEMPLATE
BASE_SHEET_URL = "https://docs.google.com/spreadsheets/d/14KbwOJO1UEDbDI_uy-30rsaypG0iaUmgrQqsmuUd0xg/edit"

@st.cache_data(ttl=5)  # Fast 5-second automatic data sync refresh loop
def load_live_data(sheet_url):
    try:
        # Convert standard URL link into a raw CSV export stream
        csv_url = sheet_url.split("/edit")[0] + "/export?format=csv&gid=0"
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        st.error(f"Error accessing your Google Sheet layout: {e}")
        return None

df = load_live_data(BASE_SHEET_URL)

if df is not None and not df.empty:
    # Remove hidden spaces out of the data headers
    df.columns = df.columns.str.strip()
    
    # Isolate real operational date entries safely
    if "Date" in df.columns:
        clean_df = df.dropna(subset=["Date"]).copy()
        clean_df["Date"] = clean_df["Date"].astype(str).str.strip()
        clean_df = clean_df[clean_df["Date"].str.contains(r'\d', na=False)]
    else:
        clean_df = df.copy()
        
    # Standardize tracking blocks into true mathematical numeric values
    numeric_cols = ["Total Collected", "Session Profit/Loss", "Misc Expenses", "Members Count", "Non-Members Count", "Total Players"]
    for col in numeric_cols:
        if col in clean_df.columns:
            clean_df[col] = pd.to_numeric(clean_df[col].astype(str).str.replace('₱', '').str.replace(',', ''), errors='coerce').fillna(0)
        else:
            clean_df[col] = 0

    # Running Operational Ledger Aggregations
    total_revenue = clean_df["Total Collected"].sum()
    gross_profits = clean_df[clean_df["Session Profit/Loss"] > 0]["Session Profit/Loss"].sum()
    total_expenses = clean_df["Misc Expenses"].sum()
    cash_in_bank = gross_profits - total_expenses

    # Display Top Live Financial Status Cards Row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Open Play Revenue", f"₱{total_revenue:,.2f}")
    col2.metric("Gross Play Profits", f"₱{gross_profits:,.2f}")
    col3.metric("Total Club Expenses", f"₱{total_expenses:,.2f}")
    col4.metric("Actual Cash In Bank", f"₱{cash_in_bank:,.2f}")
    
    st.markdown("---")
    
    # Operational Application Sub-Navigation Views
    tab1, tab2, tab3 = st.tabs(["📅 Live Session Ledger", "💵 Expenses Ledger (2nd Sheet)", "📋 Clipboard Report Generator"])
    
    with tab1:
        st.subheader("Rolling Activity Records")
        
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
        st.caption("Isolates lines where custom miscellaneous costs were logged inside the workbook.")
        
        if "Misc Expenses" in clean_df.columns:
            expense_mask = clean_df["Misc Expenses"] > 0
            expenses_df = clean_df[expense_mask][["Date", "Venue", "Misc Expenses", "Expenses Remarks"]].copy()
            expenses_df.columns = ["Expense Date", "Venue Context", "Amount Paid", "Expense Remarks / Description"]
            
            if len(expenses_df) > 0:
                st.dataframe(expenses_df.style.format({"Amount Paid": "₱{:,.2f}"}), use_container_width=True)
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
else:
    st.warning("Awaiting operational logging column metrics from your clean spreadsheet...")
