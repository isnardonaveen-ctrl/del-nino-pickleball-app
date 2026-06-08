import streamlit as st
import pandas as pd

# Page Configuration Setup
st.set_page_config(page_title="Del Niño Pickleball Club", page_icon="🏓", layout="wide")

st.title("🏓 Del Niño Pickleball Club Dashboard")
st.markdown("### Running Management & Cash Flow Hub")
st.markdown("---")

# 🟢 YOUR INTEGRATED CLOUD LINK 
# (Note: If you move your rows to Google Sheets, just swap this with your new Sheet URL!)
BASE_SHEET_URL = "https://docs.google.com/document/d/148EmmkbeQO_uQjK9ggBTu77sxT60jZ9LMob_HJkbqKE/edit"

@st.cache_data(ttl=10)  # Auto-refreshes data changes every 10 seconds
def load_tab_data(sheet_url):
    try:
        # Handles transformation of the edit URL into a clean data stream
        if "spreadsheets" in sheet_url:
            csv_url = sheet_url.split("/edit")[0] + "/export?format=csv&sheet=Open+Play+Cash+Flow"
        else:
            # Fallback wrapper if using the document viewer stream
            csv_url = sheet_url.split("/edit")[0] + "/export?format=csv"
        
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        st.error(f"Waiting for live spreadsheet data stream link configuration... Error detail: {e}")
        return None

df = load_tab_data(BASE_SHEET_URL)

if df is not None:
    # Clean hidden layout spaces out of the data headers
    df.columns = df.columns.str.strip()
    
    # Filter out completely empty or blank placeholder rows
    if "Date" in df.columns:
        clean_df = df.dropna(subset=["Date"]).copy()
    else:
        clean_df = df.copy()
        
    # Ensure numerical properties process arithmetic correctly without breaks
    for col in ["Total Collected", "Session Profit/Loss", "Misc Expenses", "Members Count", "Non-Members Count", "Total Players"]:
        if col in clean_df.columns:
            clean_df[col] = pd.to_numeric(clean_df[col], errors='coerce').fillna(0)
        else:
            clean_df[col] = 0

    # YTD KPI Summary Card Computations
    total_revenue = clean_df["Total Collected"].sum()
    gross_profits = clean_df[clean_df["Session Profit/Loss"] > 0]["Session Profit/Loss"].sum()
    total_expenses = clean_df["Misc Expenses"].sum()
    cash_in_bank = gross_profits - total_expenses

    # Render Visual Board KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Open Play Revenue", f"₱{total_revenue:,.2f}")
    col2.metric("Gross Play Profits (Positive Only)", f"₱{gross_profits:,.2f}")
    col3.metric("Total Club Expenses", f"₱{total_expenses:,.2f}")
    col4.metric("Actual Cash In Bank", f"₱{cash_in_bank:,.2f}")
    
    st.markdown("---")
    
    # Core Application View Navigation Tabs
    tab1, tab2 = st.tabs(["📅 Live Session Ledger", "📋 Clipboard Report Generator"])
    
    with tab1:
        st.subheader("Rolling Activity Records")
        
        # Colorizer function for dynamic Green/Red formatting rules
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
        st.dataframe(styled_df, use_container_width=True, height=450)
        
    with tab2:
        st.subheader("Viber / Messenger Clipboard Template")
        st.info("Slide to select your session row to dynamically prepare your message text block block:")
        
        if len(clean_df) > 0:
            # Row selection slider controller tool
            selected_row_idx = st.slider("Select Row Sequence", min_value=0, max_value=len(clean_df)-1, value=0)
            row_data = clean_df.iloc[selected_row_idx]
            
            # Formulates the copied group chat report automatically
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
            st.warning("No operational data records detected to assemble a clipboard summary.")
