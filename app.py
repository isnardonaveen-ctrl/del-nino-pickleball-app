import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF

st.set_page_config(page_title="Del Niño Pickleball Club", page_icon="🏓", layout="wide")

# --- CSS STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #013220 !important; }
    [data-testid="stSidebar"] { background-color: #0a4d35 !important; border-right: 2px solid #D4AF37 !important; }
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: #FFFFFF !important; }
    button[data-testid="stSidebarCollapseButton"] { background-color: #D4AF37 !important; border: none !important; border-radius: 5px !important; padding: 5px !important; width: 35px !important; height: 35px !important; display: flex !important; align-items: center !important; justify-content: center !important; }
    button[data-testid="stSidebarCollapseButton"] svg { fill: #013220 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #D4AF37 !important; }
    div[data-baseweb="select"] > div { background-color: #FFFFFF !important; border: 3px solid #D4AF37 !important; border-radius: 8px !important; }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div { color: #000000 !important; }
    div[role="listbox"] { background-color: #FFFFFF !important; }
    div[role="listbox"] span { color: #000000 !important; font-weight: bold !important; }
    div.stButton > button { background-color: #D4AF37 !important; color: #013220 !important; font-weight: bold !important; border: 2px solid #FFFFFF !important; }
    div.stDownloadButton > button { background-color: #76FF7B !important; color: #013220 !important; font-weight: bold !important; border: 2px solid #FFFFFF !important; }
    div[data-testid="stWidgetLabel"] p, label { color: #D4AF37 !important; font-weight: bold !important; font-size: 1.1rem !important; }
    .stApp::before { content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-image: url('https://github.com/isnardonaveen-ctrl/del-nino-pickleball-app/blob/main/6832fb4b-7df6-4105-9c8c-7140bfdf4668-removebg-preview.png?raw=true'); background-repeat: no-repeat; background-position: center; background-size: 50%; opacity: 0.15; pointer-events: none; z-index: 0; }
    body, p, h1, h2, h3, h4, h5, h6, li { color: #FFFFFF !important; }
    h1, h2, h3 { color: #D4AF37 !important; }
    h1 { text-align: center; }
    [data-testid="stDataFrame"] { background-color: #0a4d35 !important; }
    .main .block-container { z-index: 1; position: relative; }
    blockquote { border-left: 5px solid #D4AF37; padding-left: 15px; font-style: italic; color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://github.com/isnardonaveen-ctrl/del-nino-pickleball-app/blob/main/6832fb4b-7df6-4105-9c8c-7140bfdf4668-removebg-preview.png?raw=true", use_container_width=True)
    st.markdown("## Navigation")
    page = st.radio("Go to:", ["🏠 Home", "🔒 Admin Dashboard"])

# --- PAGE 1: PUBLIC HOME PAGE ---
def show_home_page():
    st.markdown("<h1 style='text-align: center; color: #D4AF37; font-size: 4rem;'>Del Niño Pickleball Club</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FFFFFF;'>Tacloban City's Premier Pickleball Community</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ABOUT US SECTION
    st.markdown("""
    Welcome to **Del Niño Pickleball Club**, the beating heart of the fastest-growing sports community in Tacloban City!

    Whether you’re holding a paddle for the very first time or perfecting your third-shot drop to dominate the professional circuits, you have a home on our courts. Founded on a passion for fitness, fun, and fellowship, Del Niño Pickleball Club was built to bring people together through the joy of the game.

    ### 🌟 Our Philosophy: All Game. All Heart. All Welcome.
    At Del Niño, we believe pickleball is more than just a sport—it’s a community. We pride ourselves on creating an inclusive, high-energy environment where **all genders, ages, and skill levels** can thrive.

    * **The First-Timers:** Nervous about stepping onto the court? Don't be! Our welcoming community and friendly regulars will have you dinking like a pro in no time.
    * **The Social Players:** Looking for a fun way to stay active, burn some calories, and meet incredible people? Our community is packed with vibrant personalities who love a good rally and a great laugh.
    * **The Competitors:** Ready to test your limits? We host high-octane tournaments, fast-paced ladder leagues, and intensive clinics designed to sharpen your edge and elevate your game to professional standards.

    ### 🔥 What Makes the Del Niño Experience Special?
    We aren't just a place to rent a court; we are a destination. When you step into Del Niño, you’re getting the full experience:

    * **Top-Tier Facilities:** Play on premium, well-maintained courts designed for optimal bounce, traction, and peak performance.
    * **Dynamic Events:** From action-packed weekend shootouts and themed social nights to elite local tournaments, there is always something happening on our calendar.
    * **A Growing Family:** Beyond the lines of the court, we are a tight-knit family. We celebrate every milestone, every incredible shot, and every new friendship formed over the net.

    ### Join the Movement!
    The paddle sport taking over the world has officially found its ultimate home in Leyte. Come for the fitness, stay for the family.
    
    Whether you're looking to smash a winner, learn the basics, or just enjoy the best community vibe in Tacloban, **Del Niño Pickleball Club** is ready for you.

    > **See you on the court!** 🏓✨
    """)
    
    st.markdown("---")
    
    # INFO & REGISTRATION SECTION
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<h3 style='text-align: left;'>Weekly Schedule</h3>", unsafe_allow_html=True)
        st.write("📅 **Tuesdays, Thursdays, Saturdays:** Southside")
        st.write("📅 **Sundays, Mondays, Wednesdays, Fridays:** Smashville")
        
    with col2:
        st.markdown("<h3 style='text-align: left;'>Open Play Fees</h3>", unsafe_allow_html=True)
        st.write("💰 **Members:** ₱100")
        st.write("💰 **Non-Members:** ₱150")

    with col3:
        st.markdown("<h3 style='text-align: left;'>Join the Club!</h3>", unsafe_allow_html=True)
        st.write("Ready to hit the courts with us? Scan the QR code or click below to register.")
        # Placeholder for QR Code
        st.info("![QR Code Placeholder](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/QR_code_for_mobile_English_Wikipedia.svg/220px-QR_code_for_mobile_English_Wikipedia.svg.png)")
        st.button("📝 Click Here to Register")


# --- PAGE 2: SECURE ADMIN DASHBOARD ---
def show_admin_page():
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>Club Financial Tracker</h1>", unsafe_allow_html=True)
    
    # PASSWORD PROTECTION
    password = st.text_input("Enter Admin Password:", type="password")
    
    if password == "Admin123":  # Change this to whatever you want!
        st.success("Access Granted.")
        st.markdown("---")
        
        # --- ORIGINAL TRACKER LOGIC STARTS HERE ---
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
            start_date = datetime(2026, 4, 16)
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
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, txt=f"Del Nino Club Report: {month_name} 2026", ln=1, align='C')
            pdf.ln(10)
            
            total_expenses = df['Misc Expenses'].sum() if 'Misc Expenses' in df.columns else 0
            avg_players = df['Total Players'].mean() if 'Total Players' in df.columns and not df.empty else 0
            total_costs = (df['Court Cost'].sum() if 'Court Cost' in df.columns else 0) + total_expenses
            total_shirt_sales = df['T-shirt Sales'].sum() if 'T-shirt Sales' in df.columns else 0
            total_membership = df['Membership Fees'].sum() if 'Membership Fees' in df.columns else 0
            
            pdf.set_font("Arial", '', 12)
            pdf.cell(100, 10, txt="Total Expenses:", border=1)
            pdf.cell(90, 10, txt=f"PHP {total_expenses:,.2f}", border=1, ln=1)
            pdf.cell(100, 10, txt="Total T-shirt Sales:", border=1)
            pdf.cell(90, 10, txt=f"PHP {total_shirt_sales:,.2f}", border=1, ln=1)
            pdf.cell(100, 10, txt="Total Membership Fees:", border=1)
            pdf.cell(
