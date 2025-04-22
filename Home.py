import streamlit as st
import pandas as pd
from utils.db import get_resume_count, get_avg_match_score
from utils.db import init_db

st.set_page_config(page_title="Resume Tracker Dashboard", layout="wide")

init_db()  # ✅ Initializes the resumes table



# Login (static for now)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

with st.sidebar:
    st.header("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login = st.button("Login")

    if login:
        if username == "admin" and password == "admin123":
            st.session_state['logged_in'] = True
        else:
            st.error("Invalid credentials")

if not st.session_state['logged_in']:
    st.warning("Please login to access the dashboard.")
    st.stop()

# Dashboard
st.title("ATS Dashboard Overview")

total_resumes = get_resume_count()
avg_score = get_avg_match_score()

col1, col2 = st.columns(2)
col1.metric("Total Resumes", total_resumes)
col2.metric("Average Match Score", f"{avg_score:.2f}" if avg_score else "N/A")

st.info("Use the sidebar to navigate through the system.")