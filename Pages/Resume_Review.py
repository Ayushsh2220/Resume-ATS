import streamlit as st
import pandas as pd
from utils.db import connect_db

st.set_page_config(page_title="Resume Review", layout="wide")
st.title("Review & Update Resumes")

conn = connect_db()
df = pd.read_sql("SELECT * FROM resumes", conn)

name_filter = st.text_input("Search by Name")
skill_filter = st.text_input("Search by Skill")

if name_filter:
    df = df[df['name'].str.contains(name_filter, case=False, na=False)]
if skill_filter:
    df = df[df['skills'].str.contains(skill_filter, case=False, na=False)]

for _, row in df.iterrows():
    with st.expander(f"{row['name']} | {row['email']} | Score: {row['score']:.2f}"):
        st.markdown(f"**Skills:** {row['skills']}")
        st.markdown(f"**Experience:**\n{row['experience']}")
        st.markdown(f"**Education:**\n{row['education']}")

        required_skills = st.text_input(f"Required Skills (comma-separated)", key=f"req_{row['id']}")
        if required_skills:
            existing = set(row['skills'].split(", "))
            required = set([s.strip().lower() for s in required_skills.split(",")])
            missing = required - existing
            st.warning(f"Missing Skills: {', '.join(missing) if missing else 'None'}")

        new_status = st.selectbox("Update Status", ["Pending", "Shortlisted", "Interviewed", "Rejected"], index=["Pending", "Shortlisted", "Interviewed", "Rejected"].index(row['status'] if row['status'] else "Pending"), key=f"status_{row['id']}")
        new_notes = st.text_area("Recruiter Notes", value=row['notes'] or "", key=f"note_{row['id']}")

        if st.button("Save Updates", key=f"save_{row['id']}"):
            conn.execute("UPDATE resumes SET status=?, notes=? WHERE id=?", (new_status, new_notes, row['id']))
            conn.commit()
            st.success("Resume updated.")
