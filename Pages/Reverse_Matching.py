import streamlit as st
import json
import os
import pandas as pd
from utils.db import connect_db
from utils.parser import match_score

st.set_page_config(page_title="Reverse JD Matching", layout="wide")
st.title("Reverse Match: Resume to JD")

conn = connect_db()
resumes = pd.read_sql("SELECT id, name, file_name FROM resumes", conn)

JD_DIR = "jd_templates"
jd_files = [f for f in os.listdir(JD_DIR) if f.endswith(".json")]

selected_resume = st.selectbox("Select Resume", resumes['name'].tolist())
selected_jd = st.selectbox("Select JD Template", [f.replace(".json", "") for f in jd_files])

if st.button("Match Now"):
    resume_row = resumes[resumes['name'] == selected_resume].iloc[0]
    with open(os.path.join(JD_DIR, f"{selected_jd}.json")) as f:
        jd_text = json.load(f)['jd']
    
    resume_text = conn.execute("SELECT experience || ' ' || education || ' ' || skills FROM resumes WHERE id=?", (resume_row['id'],)).fetchone()[0]
    score = match_score(resume_text, jd_text)
    st.success(f"Match Score with '{selected_jd}' JD: {score:.2f}")
