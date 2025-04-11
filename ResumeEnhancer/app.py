import streamlit as st
import pandas as pd
import PyPDF2
import difflib
import os

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text.strip()

def detect_text_column(df):
    # Try to auto-detect the most text-heavy column
    text_column = None
    max_length = 0
    for col in df.columns:
        combined_text = ' '.join(df[col].astype(str).dropna().tolist())
        if len(combined_text) > max_length:
            max_length = len(combined_text)
            text_column = col
    return text_column

def compare_resumes(user_text, sample_text):
    # Normalize whitespaces
    user_text = ' '.join(user_text.lower().split())
    sample_text = ' '.join(sample_text.lower().split())

    similarity = difflib.SequenceMatcher(None, user_text, sample_text).ratio()
    keywords = ["projects", "internship", "skills", "certifications", "achievements", "publications"]
    suggestions = [f"Consider adding a section on '{k.title()}'." for k in keywords if k not in user_text]
    return similarity, suggestions

st.title("Resume Enhancer for CSE Students")

st.write("### Upload Your Resume (PDF):")
user_pdf = st.file_uploader("Upload Your Resume", type="pdf")

sample_folder = "ResumeSample"
available_samples = [f for f in os.listdir(sample_folder) if f.endswith(".csv")]

if available_samples:
    selected_sample = st.selectbox("Select a Sample Resume for Comparison", available_samples)
else:
    st.error("No sample resumes available. Please ask admin to upload samples.")

if user_pdf and selected_sample:
    # Extract user resume text
    user_text = extract_text_from_pdf(user_pdf)

    if not user_text:
        st.error("No text found in the uploaded PDF. Please check the file.")
    else:
        try:
            sample_df = pd.read_csv(os.path.join(sample_folder, selected_sample))
            text_column = detect_text_column(sample_df)

            if not text_column:
                st.error("Couldn't detect text content in the sample CSV. Please check the file format.")
            else:
                sample_text = ' '.join(sample_df[text_column].astype(str).dropna().tolist())
                similarity, suggestions = compare_resumes(user_text, sample_text)

                st.write(f"### Similarity with sample resume: **{similarity * 100:.2f}%**")
                st.write("### Suggestions for Improvement:")
                if suggestions:
                    for s in suggestions:
                        st.write(f"- {s}")
                else:
                    st.write("Your resume looks well-structured!")
        except Exception as e:
            st.error(f"Error processing the sample resume: {e}")
