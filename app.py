import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF

# --- PAGE CONFIG ---
st.set_page_config(page_title="Del Niño Pickleball Club", page_icon="🏓", layout="wide")

# --- CSS STYLING (Fixed Text Visibility) ---
st.markdown("""
    <style>
    /* Force background and text colors */
    .stApp { background-color: #013220 !important; }
    
    h1, h2, h3, h4, h5, h6, p, div, span, li { 
        color: #FFFFFF !important; 
    }
    
    /* Highlight the Titles in Gold */
    .title-gold { color: #D4AF37 !important; text-align: center; }
    
    /* Ensure sidebar is visible */
    [data-testid="stSidebar"] { background-color: #0a4d35 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS ---
def show_home_page():
    st.markdown("<h1 class='title-gold'>Del Niño Pickleball Club</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='title-gold' style='text-align: center;'>Tacloban City's Premier Pickleball Community</h3>", unsafe_allow_html=True)
    st.write("---")
    st.write("Welcome to the heart of the fastest-growing sports community in Tacloban City!")
    st.write("This is your home for fitness, fun, and fellowship on the courts.")

def show_admin_page():
    st.title("🔒 Admin Dashboard")
    password = st.text_input("Enter Admin Password:", type="password")
    if password == "Admin123":
        st.success("Access granted.")
    elif password:
        st.error("Incorrect password.")

# --- NAVIGATION ---
with st.sidebar:
    st.markdown("## Navigation")
    page = st.radio("Go to:", ["🏠 Home", "🔒 Admin Dashboard"])

# --- ROUTING ---
if page == "🏠 Home":
    show_home_page()
else:
    show_admin_page()
