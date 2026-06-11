import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF

# --- CONFIGURATION ---
st.set_page_config(page_title="Del Niño Pickleball Club", page_icon="🏓", layout="wide")

# --- AESTHETIC CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Open+Sans&display=swap');

    .stApp { background-color: #013220 !important; font-family: 'Open Sans', sans-serif; }
    [data-testid="stSidebar"] { background-color: #0a4d35 !important; border-right: 1px solid #D4AF37 !important; }
    h1, h2, h3 { font-family: 'Montserrat', sans-serif !important; color: #D4AF37 !important; text-transform: uppercase; letter-spacing: 1px; }
    p, li, div { font-family: 'Open Sans', sans-serif !important; color: #E0E0E0 !important; line-height: 1.6; }
    
    /* Card-style containers */
    .stApp div[data-testid="stVerticalBlock"] {
        background-color: rgba(255, 255, 255, 0.03); 
        padding: 1.5rem !important; 
        border-radius: 15px !important; 
        border: 1px solid rgba(212, 175, 55, 0.2);
    }

    div.stButton > button { background-color: #D4AF37 !important; color: #013220 !important; font-weight: 700 !important; border: none !important; border-radius: 5px !important; }
    div.stDownloadButton > button { background-color: #76FF7B !important; color: #013220 !important; font-weight: bold !important; border: 2px solid #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://github.com/isnardonaveen-ctrl/del-nino-pickleball-app/blob/main/6832fb4b-7df6-4105-9c8c-7140bfdf4668-removebg-preview.png?raw=true", use_container_width=True)
    st.markdown("## Navigation")
    page = st.radio("Go to:", ["🏠 Home", "🔒 Admin Dashboard"])

# --- PAGE 1: HOME ---
def show_home_page():
    st.markdown("<h1 style='text-align: center;'>Del Niño Pickleball Club</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>The Heart of Pickleball in Tacloban City</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Del Niño Pickleball Club** is the premier home for pickleball in Tacloban. We are a fast-growing, inclusive community dedicated to one thing: bringing people together through the power of the paddle.

        ### Who We Are
        Whether you are picking up a paddle for the first time or you are a seasoned pro, you belong here. We champion an environment where everyone is welcome to play, grow, and compete.

        ### Why Join Us?
        * **All-Inclusive:** Community built for every level.
        * **Dynamic Play:** High-energy tournaments and leagues.
        * **A Growing Family:** Join us for the fitness, stay for the friendships.
        """)
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📅 Weekly Schedule")
            st.write("Tue, Thu, Sat: **Southside**")
            st.write("Sun, Mon, Wed, Fri: **Smashville**")
        with c2:
            st.subheader("💰 Open Play Fees")
            st.write("Members: **₱100**")
            st.write("Non-Members: **₱150**")

    with col2:
        st.subheader("Join the Club!")
        st.button("📝 Click Here to Register")
    
    st.write("### See you on the court! 🏓✨")

# --- PAGE 2: ADMIN DASHBOARD ---
def show_admin_page():
    st.markdown("<h1>Club Financial Tracker</h1>", unsafe_allow_html=True)
    password = st.text_input("Enter Admin Password:", type="password")
    
    if password == "Admin123":
        st.success("Access Granted.")
        # --- ORIGINAL DATA LOGIC ---
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

        raw_sheet_df = load_live_data(BASE_SHEET_URL)
        calendar_df = generate_2026_calendar()

        if raw_sheet_df is not None:
            # Data Processing Logic
            raw_sheet_df.columns = raw_sheet_df.columns.str.strip()
            clean_df = pd.merge(calendar_df, raw_sheet_df.dropna(subset=["Date"]), on="Date", how="left").fillna(0)
            
            # Calculations
            clean_df["Total Players"] = (clean_df["Members Count"] + clean_df["Non-Members Count"]).astype(int)
            clean_df["Total Collected"] = (clean_df["Members Count"] * 100) + (clean_df["Non-Members Count"] * 150) + clean_df["T-shirt Sales"] + clean_df["Membership Fees"]
            clean_df["Net Cash for Today"] = clean_df["Total Collected"] - 3600 - clean_df["Misc Expenses"]
            
            # Metrics
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Revenue", f"₱{clean_df['Total Collected'].sum():,.0f}")
            c2.metric("Profits", f"₱{clean_df[clean_df['Net Cash for Today'] > 0]['Net Cash for Today'].sum():,.0f}")
            c3.metric("Expenses", f"₱{clean_df['Misc Expenses'].sum():,.0f}")
            c4.metric("Bank", f"₱{clean_df['Net Cash for Today'].sum():,.0f}")
            
            st.line_chart(clean_df.set_index('Date')[['Total Collected', 'Misc Expenses']])
            st.dataframe(clean_df, use_container_width=True)
        else: st.error("Failed to load spreadsheet.")
            
    elif password != "": st.error("Incorrect Password.")

if page == "🏠 Home": show_home_page()
elif page == "🔒 Admin Dashboard": show_admin_page()
