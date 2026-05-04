import streamlit as st
import PyPDF2
import requests
import json
import io

URL = "http://localhost:11434/api/chat"
MODEL = "llama3"

st.set_page_config(page_title="AI Resume Critiquer", page_icon="📄", layout="centered")

st.title("AI Resume Critiquer")
st.markdown("Upload your resume and get concise, recruiter-style feedback in seconds.")

with st.container(border=True):
    st.subheader("Upload & Target Role")
    with st.form("resume_form", clear_on_submit=False):
        col1, col2 = st.columns([1.2, 1])
        with col1:
            upload_file = st.file_uploader("Resume file", type=["pdf", "txt"], help="PDF or TXT")
        with col2:
            job_role = st.text_input(
                "Target role",
                placeholder="e.g. Software Engineer, Data Scientist",
            )
        analyze = st.form_submit_button("Analyze Resume", use_container_width=True)

def extract_text_from_pdf(uploaded_file):
    """Extracts text content from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    """Identifies file type and extracts text accordingly."""
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze and upload_file:
    try:
        with st.spinner("Reading and analyzing resume..."):
            file_content = extract_text_from_file(upload_file)
            
        if not file_content.strip():
            st.error("The file content is empty or could not be read.")
            st.stop()

        prompt = f"""Please analyze this resume and provide constructive feedback.
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation and relevance
        3. Experience descriptions and achievements
        4. Specific recommendations for: {job_role if job_role else 'general job applications'}
        
        Resume Content:
        {file_content}
        
        Please provide your analysis in a professional, structured English format using Markdown."""

        data = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are a professional HR Specialist and Career Coach."},
                {"role": "user", "content": prompt}
            ],
            "stream": True
        }

        st.subheader("AI Analysis Report")
        
        response_placeholder = st.empty()
        full_response = ""

        response = requests.post(URL, json=data, stream=True)
       
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode('utf-8'))
                if 'message' in chunk:
                    content = chunk['message']['content']
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
        st.success("Analysis completed successfully!")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

st.caption("Privacy note: your file is processed locally and not stored.")