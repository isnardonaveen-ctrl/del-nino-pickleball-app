import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF

# --- PAGE CONFIG ---
st.set_page_config(page_title="Del Niño Pickleball Club", page_icon="🏓", layout="wide")

# --- STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #013220 !important; }
    [data-testid="stSidebar"] { background-color: #0a4d35 !important; border-right: 2px solid #D4AF37 !important; }
    h1, h2, h3 { color: #D4AF37 !important; }
    .main .block-container { z-index: 1; position: relative; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS ---
def show_home_page():
    st.markdown("<h1 style='text-align: center;'>Del Niño Pickleball Club</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Tacloban City's Premier Pickleball Community</h3>", unsafe_allow_html=True)
    st.write("Welcome to the heart of the fastest-growing sports community in Tacloban City!")
    # ... (Rest of your home content)

def show_admin_page():
    st.title("🔒 Admin Dashboard")
    password = st.text_input("Enter Admin Password:", type="password")
    if password == "Admin123":
        st.write("Access granted to financial tools.")
        # ... (Your logic here)
    elif password:
        st.error("Incorrect password.")

# --- NAVIGATION ---
with st.sidebar:
    st.image("https://github.com/isnardonaveen-ctrl/del-nino-pickleball-app/blob/main/6832fb4b-7df6-4105-9c8c-7140bfdf4668-removebg-preview.png?raw=true", use_container_width=True)
    page = st.radio("Navigation", ["Home", "Admin Dashboard"])

# --- ROUTING ---
if page == "Home":
    show_home_page()
else:
    show_admin_page()
