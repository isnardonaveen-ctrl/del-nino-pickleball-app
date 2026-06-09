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
    pdf.cell(190, 10, txt=f"Del Nino Club Report: {month_name} 2026", ln=1, align='C')
    pdf.ln(10)
    
    # Financial Extractions
    total_expenses = df['Misc Expenses'].sum() if 'Misc Expenses' in df.columns else 0
    avg_players = df['Total Players'].mean() if 'Total Players' in df.columns and not df.empty else 0
    total_costs = (df['Court Cost'].sum() if 'Court Cost' in df.columns else 0) + total_expenses
    total_shirt_sales = df['T-shirt Sales'].sum() if 'T-shirt Sales' in df.columns else 0
    total_membership = df['Membership Fees'].sum() if 'Membership Fees' in df.columns else 0
    
    # Build Document View
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, txt="Total Expenses:", border=1)
    pdf.cell(90, 10, txt=f"PHP {total_expenses:,.2f}", border=1, ln=1)
    
    pdf.cell(100, 10, txt="Total T-shirt Sales:", border=1)
    pdf.cell(90, 10, txt=f"PHP {total_shirt_sales:,.2f}", border=1, ln=1)
    
    pdf.cell(100, 10, txt="Total Membership Fees:", border=1)
    pdf.cell(90, 10, txt=f"PHP {total_membership:,.2f}", border=1, ln=1)
    
    pdf.cell(100, 10, txt="Average Players/Day:", border=1)
    pdf.cell(90, 10, txt=f"{avg_players:.1f}", border=1, ln=1)
    
    pdf.cell(100, 10, txt="Total Operational Costs:", border=1)
    pdf.cell(90, 10, txt=f"PHP {total_costs:,.2f}", border=1, ln=1)
    
    return pdf.output(dest='S').encode('latin-1')

if raw_sheet_df is not None:
    raw_sheet_df.columns = raw_sheet_df.columns.str.strip()
    
    # Structural Safety Check
    target_cols = ["Members Count", "Non-Members Count", "Misc Expenses", "T-shirt Sales", "Membership Fees"]
    for col in target_cols:
        if col not in raw_sheet_df.columns:
            raw_sheet_df[col] = 0

    if "Date" in raw_sheet_df.columns:
        raw_sheet_df["Date"] = raw_sheet_df["Date"].astype(str).str.strip()
        clean_df = pd.merge(calendar_df, raw_sheet_df.dropna(subset=["Date"]), on="Date", how="left")
    else:
        clean_df = calendar_df

    # Standardize Array types safely
    for col in target_cols:
        clean_df[col] = pd.to_numeric(clean_df[col], errors='coerce').fillna(0)

    clean_df["Members Count"] = clean_df["Members Count"].astype(int)
    clean_df["Non-Members Count"] = clean_df["Non-Members Count"].astype(int)

    # Core Math Operational Rules
    clean_df["Total Players"] = (clean_df["Members Count"] + clean_df["Non-Members Count"]).astype(int)
    clean_df["Open Play Total Fees"] = (clean_df["Members Count"] * 100) + (clean_df["Non-Members Count"] * 150)
    clean_df["Total Collected"] = clean_df["Open Play Total Fees"] + clean_df["T-shirt Sales"] + clean_df["Membership Fees"]
    
    clean_df["Court Cost"] = 3600
    clean_df["Net Cash for Today"] = clean_df.apply(lambda r: (r["Total Collected"] - r["Court Cost"]) - r["Misc Expenses"] if r["Total Players"] > 0 else 0, axis=1)

    # Sidebar Filter Operations
    clean_df['Month'] = pd.to_datetime(clean_df['Date']).dt.month_name()
    all_months = clean_df['Month'].unique().tolist()
    
    with st.sidebar:
        st.subheader("📊 Filter Data")
        selected_months = st.multiselect("Select Months:", options=all_months, default=all_months)
    
    if selected_months:
        clean_df = clean_df[clean_df['Month'].isin(selected_months)]

    # Metrics Display Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₱{clean_df['Total Collected'].sum():,.2f}")
    col2.metric("Gross Profits", f"₱{clean_df[clean_df['Net Cash for Today'] > 0]['Net Cash for Today'].sum():,.2f}")
    col3.metric("Total Expenses", f"₱{clean_df['Misc Expenses'].sum():,.2f}")
    col4.metric("Actual Cash In Bank", f"₱{clean_df['Net Cash for Today'].sum():,.2f}")
    
    st.markdown("---")

    def highlight_financials(val):
        color = '#76FF7B' if val > 0 else '#FF6B6B' if val < 0 else 'white'
        bg = 'background-color: transparent;'
        return f'color: {color}; {bg} font-weight: bold;'

    tab1, tab2, tab3 = st.tabs(["📅 Live Session Ledger", "💵 Expenses Ledger", "📋 Clipboard Report Generator"])

    with tab1:
        display_df = clean_df[["Date", "Day", "Venue", "Members Count", "Non-Members Count", "Total Players", "Open Play Total Fees", "T-shirt Sales", "Membership Fees", "Total Collected", "Court Cost", "Misc Expenses", "Net Cash for Today"]]
        st.dataframe(display_df.style.format({
            "Members Count": "{:.0f}",
            "Non-Members Count": "{:.0f}",
            "Open Play Total Fees": "₱{:,.2f}", 
            "T-shirt Sales": "₱{:,.2f}", 
            "Membership Fees": "₱{:,.2f}",
            "Total Collected": "₱{:,.2f}", 
            "Court Cost": "₱{:,.2f}", 
            "Misc Expenses": "₱{:,.2f}", 
            "Net Cash for Today": "₱{:,.2f}"
        }).map(highlight_financials, subset=['Net Cash for Today']), use_container_width=True)

    with tab2:
        expense_cols = ["Date", "Venue", "Misc Expenses"]
        if "Expenses Remarks" in clean_df.columns:
            expense_cols.append("Expenses Remarks")
        expense_df = clean_df[clean_df["Misc Expenses"] > 0][expense_cols]
        st.dataframe(expense_df.style.format({"Misc Expenses": "₱{:,.2f}"}), use_container_width=True)

    with tab3:
        st.subheader("📋 Monthly Audit Report")
        selected_month_for_pdf = st.selectbox("Choose a month to export:", all_months)
        
        if st.button("Generate PDF Report"):
            report_df = clean_df[clean_df['Month'] == selected_month_for_pdf]
            pdf_data = generate_monthly_report(report_df, selected_month_for_pdf)
            
            # Safe single-line execution to avoid syntax errors
            st.download_button(label="📥 Download PDF Report", data=pdf_data, file_name=f"Report_{selected_month_for_pdf}_2026.pdf", mime="application/pdf")
            st.success(f"Report for {selected_month_for_pdf} generated!")
else:
    st.error("Failed to load spreadsheet link configuration data.")
