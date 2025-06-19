import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

def render():
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    def get_gemini_response(prompt):
        response = model.generate_content(prompt)
        return response.text

    def input_pdf_text(uploaded_file):
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    st.title("🧠 AI ATS Resume Evaluator")
    st.caption("Analyze your resume against a job description using Gemini 1.5 Flash LLM")

    jd = st.text_area("📋 Paste the Job Description")
    uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type="pdf", help="Only PDF files supported")

    if st.button("🔍 Analyze"):
        if not uploaded_file:
            st.warning("⚠️ Please upload your resume first.")
            return
        if not jd:
            st.warning("⚠️ Please paste a job description.")
            return

        with st.spinner("Reading resume and analyzing..."):
            resume_text = input_pdf_text(uploaded_file)

            prompt = f"""
Act like a skilled ATS (Applicant Tracking System) with deep expertise in software engineering, data science, data analysis, and big data roles.
Your task is to evaluate the resume based on the job description below. The job market is competitive, so provide clear insights.

Resume:
{resume_text}

Job Description:
{jd}

Please answer in the following human-readable format:
1. ✅ JD Match (%)
2. ❌ Missing Keywords (comma-separated)
3. 📝 Profile Summary (1-3 sentences about candidate fit)
"""
            result = get_gemini_response(prompt)

        st.subheader("📊 ATS Analysis Result")
        st.markdown(result)

if __name__ == "__main__":
    render()
