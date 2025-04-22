import streamlit as st
import pandas as pd
from utils.db import connect_db

st.set_page_config(page_title="Admin Tools", layout="wide")
st.title("Admin Tools")

conn = connect_db()
df = pd.read_sql("SELECT * FROM resumes", conn)

st.subheader("Download All Data")
if st.button("Download CSV"):
    st.download_button("Click to Download", df.to_csv(index=False), file_name="all_resumes.csv", mime='text/csv')

st.subheader("Delete a Resume")
resume_to_delete = st.selectbox("Select Resume", df['name'].tolist())
if st.button("Delete Resume"):
    conn.execute("DELETE FROM resumes WHERE name = ?", (resume_to_delete,))
    conn.commit()
    st.success(f"{resume_to_delete} deleted!")

st.subheader("Reset Entire Database")
if st.button("Delete All Resumes"):
    conn.execute("DELETE FROM resumes")
    conn.commit()
    st.success("Database reset successfully!")
