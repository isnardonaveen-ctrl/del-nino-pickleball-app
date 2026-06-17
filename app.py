import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF

st.set_page_config(page_title="Del Niño Pickleball Club", page_icon="🏓", layout="wide")

# --- AESTHETIC CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Open+Sans&display=swap');

    .stApp { background-color: #013220 !important; font-family: 'Open Sans', sans-serif; }
    
    [data-testid="stSidebar"] { 
        background-color: #0a4d35 !important; 
        border-right: 1px solid #D4AF37 !important; 
    }
    
    h1, h2, h3 { 
        font-family: 'Montserrat', sans-serif !important; 
        color: #D4AF37 !important; 
        text-transform: uppercase; 
        letter-spacing: 1px;
    }
    
    p, li, div { font-family: 'Open Sans', sans-serif !important; color: #E0E0E0 !important; line-height: 1.6; }
    
    /* Card-style containers */
    .stApp div[data-testid="stVerticalBlock"] { 
        background-color: rgba(255, 255, 255, 0.03); 
        padding: 1.5rem !important; 
        border-radius: 15px !important; 
        border: 1px solid rgba(212, 175, 55, 0.2);
    }

    /* FIX: Dropdown Menu Colors */
    div[data-baseweb="select"] { 
        background-color: #0a4d35 !important; 
        color: #FFFFFF !important; 
    }
    div[role="listbox"] { 
        background-color: #0a4d35 !important; 
        color: #FFFFFF !important; 
    }
    div[role="option"] { 
        color: #FFFFFF !important; 
    }
    div[role="option"]:hover { 
        background-color: #D4AF37 !important; 
        color: #013220 !important; 
    }

    div.stButton > button { 
        background-color: #D4AF37 !important; 
        color: #013220 !important; 
        font-weight: 700 !important; 
        border: none !important; 
        border-radius: 5px !important;
        transition: 0.3s !important;
    }
    
    div.stDownloadButton > button { background-color: #76FF7B !important; color: #013220 !important; font-weight: bold !important; border: 2px solid #FFFFFF !important; }

    .stApp::before { 
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
        background-image: url('https://github.com/isnardonaveen-ctrl/del-nino-pickleball-app/blob/main/6832fb4b-7df6-4105-9c8c-7140bfdf4668-removebg-preview.png?raw=true'); 
        background-repeat: no-repeat; background-position: center; background-size: 30%; 
        opacity: 0.05; pointer-events: none; z-index: 0; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://github.com/isnardonaveen-ctrl/del-nino-pickleball-app/blob/main/6832fb4b-7df6-4105-9c8c-7140bfdf4668-removebg-preview.png?raw=true", use_container_width=True)
    st.markdown("## Navigation")
    page = st.radio("Go to:", ["🏠 Home", "🔒 Admin Dashboard"])

# --- PAGE 1: PUBLIC HOME PAGE ---
def show_home_page():
    st.markdown("<h1 style='text-align: center;'>Del Niño Pickleball Club</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>The Heart of Pickleball in Tacloban City</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Del Niño Pickleball Club** is the premier home for pickleball in Tacloban. We are a fast-growing, inclusive community dedicated to one thing: bringing people together through the power of the paddle.

        ### Who We Are
        Whether you are picking up a paddle for the first time or you are a seasoned pro, you belong here. We champion an environment where everyone—regardless of age, gender, or skill—is welcome to play, grow, and compete.

        ### Why Join Us?
        * **All-Inclusive:** From beginners learning the basics to pros fine-tuning their strategy, our community is built for every level.
        * **Dynamic Play:** Beyond open play, we offer high-energy tournaments, competitive leagues, and social events.
        * **A Growing Family:** We’re more than a club; we’re a community. Join us for the fitness, and stay for the friendships.
        """)
        
        st.subheader("Weekly Schedule")
        st.write("📅 **Tuesdays, Thursdays, Saturdays:** 6PM-10PM Smashzone Southside")
        st.write("📅 **Mondays, Wednesdays, Fridays:** 6PM-10PM Smashzone Smashville")
        
        st.subheader("Open Play Fees")
        st.write("💰 **Members:** ₱100")
        st.write("💰 **Non-Members:** ₱150")
        st.write("💰 **https://reclub.co/clubs/@del-nino-pickleball")
        
    with col2:
        st.subheader("Join the Club!")
        st.write("Ready to hit the courts with us? Click below to fill out our membership form.")
        # Displaying the QR Code
        st.image("qr-code.png", caption="Scan to Register")
        # Added link button for registration
        st.link_button("📝 Click Here to Register", "https://docs.google.com/forms/d/e/1FAIpQLSeqO26XzEBb6B8g0bugD8GeLEjIKmYjHXceMnIrcbwpHgsZYQ/viewform")
    
    st.write("### See you on the court! ✨")

# --- PAGE 2: SECURE ADMIN DASHBOARD ---
def show_admin_page():
    st.markdown("<h1 style='text-align: center;'>Club Financial Tracker</h1>", unsafe_allow_html=True)
    password = st.text_input("Enter Admin Password:", type="password")
    
    if password == "pechopak155":
        st.success("Access Granted.")
        st.markdown("---")
        
        BASE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1kDSwEA75lTPwv-wNGCnU6IPI2day9D69hgan_xuG7sA/edit?gid=0#gid=0"

        @st.cache_data(ttl=5)
        def load_live_data(sheet_url):
            try:
                csv_url = sheet_url.split("/edit")[0] + "/gviz/tq?tqx=out:csv"
                return pd.read_csv(csv_url)
            except Exception: return None

        def generate_2026_calendar():
            start_date, end_date = datetime(2026, 4, 16), datetime(2026, 12, 31)
            dates, days, venues = [], [], []
            curr = start_date
            while curr <= end_date:
                if curr.weekday() != 6:
                    dates.append(curr.strftime("%Y-%m-%d"))
                    days.append(curr.strftime("%A"))
                    venues.append("Southside" if curr.strftime("%A") in ["Tuesday", "Thursday", "Saturday"] else "Smashville")
                curr += timedelta(days=1)
            return pd.DataFrame({"Date": dates, "Day": days, "Venue": venues})

        def generate_monthly_report(df, month_name):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, txt=f"Del Nino Club Report: {month_name} 2026", ln=1, align='C')
            pdf.ln(10)
            
            # --- CALCULATIONS FOR THE PDF ---
            gross_profit = df['Total Collected'].sum() if 'Total Collected' in df.columns else 0
            total_expenses = df['Misc Expenses'].sum() if 'Misc Expenses' in df.columns else 0
            court_costs = df['Court Cost'].sum() if 'Court Cost' in df.columns else 0
            total_costs = court_costs + total_expenses
            
            net_profit = df[df['Net Cash for Today'] > 0]['Net Cash for Today'].sum() if 'Net Cash for Today' in df.columns else 0
            actual_cash = df['Net Cash for Today'].sum() if 'Net Cash for Today' in df.columns else 0
            
            # Filter for days with players to get an accurate daily average
            active_days = df[df['Total Players'] > 0]
            avg_players = active_days['Total Players'].mean() if not active_days.empty else 0
            
            # --- PDF RENDERING ---
            pdf.set_font("Arial", '', 12)
            
            pdf.cell(100, 10, txt="Total Gross Profit:", border=1)
            pdf.cell(90, 10, txt=f"PHP {gross_profit:,.2f}", border=1, ln=1)
            
            pdf.cell(100, 10, txt="Total Expenses (Misc):", border=1)
            pdf.cell(90, 10, txt=f"PHP {total_expenses:,.2f}", border=1, ln=1)
            
            pdf.cell(100, 10, txt="Total Operational Costs:", border=1)
            pdf.cell(90, 10, txt=f"PHP {total_costs:,.2f}", border=1, ln=1)
            
            pdf.cell(100, 10, txt="Total Net Profit After Expenses:", border=1)
            pdf.cell(90, 10, txt=f"PHP {net_profit:,.2f}", border=1, ln=1)
            
            pdf.cell(100, 10, txt="Actual Cash in Bank:", border=1)
            pdf.cell(90, 10, txt=f"PHP {actual_cash:,.2f}", border=1, ln=1)
            
            pdf.cell(100, 10, txt="Average Players Daily:", border=1)
            pdf.cell(90, 10, txt=f"{avg_players:,.1f} players", border=1, ln=1)
            
            return pdf.output(dest='S').encode('latin-1')

        raw_sheet_df = load_live_data(BASE_SHEET_URL)
        calendar_df = generate_2026_calendar()

        if raw_sheet_df is not None:
            raw_sheet_df.columns = raw_sheet_df.columns.str.strip()
            clean_df = pd.merge(calendar_df, raw_sheet_df.dropna(subset=["Date"]), on="Date", how="left").fillna(0)
            clean_df["Total Players"] = (clean_df["Members Count"] + clean_df["Non-Members Count"]).astype(int)
            clean_df["Total Collected"] = (clean_df["Members Count"] * 100) + (clean_df["Non-Members Count"] * 150) + clean_df["T-shirt Sales"] + clean_df["Membership Fees"]
            clean_df["Court Cost"] = 3600
            clean_df["Net Cash for Today"] = clean_df.apply(lambda r: (r["Total Collected"] - r["Court Cost"]) - r["Misc Expenses"] if r["Total Players"] > 0 else 0, axis=1)
            clean_df['Month'] = pd.to_datetime(clean_df['Date']).dt.month_name()
            
            all_months = clean_df['Month'].unique().tolist()
            with st.sidebar:
                st.markdown("---")
                st.subheader("📊 Tracker Filters")
                selected_months = st.multiselect("Select Months:", options=all_months, default=all_months)
            
            if selected_months: clean_df = clean_df[clean_df['Month'].isin(selected_months)]
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Revenue", f"₱{clean_df['Total Collected'].sum():,.2f}")
            col2.metric("Profits", f"₱{clean_df[clean_df['Net Cash for Today'] > 0]['Net Cash for Today'].sum():,.2f}")
            col3.metric("Expenses", f"₱{clean_df['Misc Expenses'].sum():,.2f}")
            col4.metric("Bank", f"₱{clean_df['Net Cash for Today'].sum():,.2f}")
            
            st.markdown("---")
            tab1, tab2, tab3 = st.tabs(["📅 Ledger", "💵 Expenses", "📋 Report"])
            with tab1: st.dataframe(clean_df, use_container_width=True)
            with tab3:
                selected_month_for_pdf = st.selectbox("Choose month:", all_months)
                if st.button("Generate PDF Report"):
                    pdf_data = generate_monthly_report(clean_df[clean_df['Month'] == selected_month_for_pdf], selected_month_for_pdf)
                    st.download_button("📥 Download PDF", data=pdf_data, file_name="Report.pdf", mime="application/pdf")
        else: st.error("Failed to load spreadsheet.")
    elif password != "": st.error("Incorrect Password.")

if page == "🏠 Home": show_home_page()
elif page == "🔒 Admin Dashboard": show_admin_page()
