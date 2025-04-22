import streamlit as st
from utils.parser import process_resume_file
from utils.db import insert_resume, init_db
from sentence_transformers import SentenceTransformer

# ✅ Page setup
st.set_page_config(page_title="Upload Resumes", layout="wide")
st.title("📄 Upload & Parse Resumes")

# ✅ Initialize database
init_db()

# ✅ Load BERT model once
@st.cache_resource
def load_model():
    return SentenceTransformer("models/all-MiniLM-L6-v2")

model = load_model()

# ✅ Inputs
job_description = st.text_area("📝 Paste Job Description", height=150)
uploaded_files = st.file_uploader("📤 Upload Resumes (.pdf, .docx)", type=["pdf", "docx"], accept_multiple_files=True)

# ✅ Process logic
if uploaded_files and job_description:
    for file in uploaded_files:
        try:
            result = process_resume_file(file, job_description, model)
            insert_resume(file.name, result)
            st.success(f"✅ {file.name} parsed and stored (Score: {result['score']:.2f})")
        except Exception as e:
            st.error(f"❌ Failed to process {file.name}: {e}")

elif uploaded_files and not job_description:
    st.warning("⚠️ Please paste a Job Description.")
elif job_description and not uploaded_files:
    st.warning("⚠️ Please upload at least one resume.")
