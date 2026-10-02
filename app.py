import os
import re
import streamlit as st
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader
from tenacity import retry, stop_after_attempt, wait_exponential

# Page Configuration
st.set_page_config(
    page_title="AI Cold Email & ATS Matcher",
    page_icon="🚀",
    layout="wide"
)

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY missing in .env file! Please check your settings.")
    st.stop()

client = genai.Client(api_key=api_key)

def extract_text_from_pdf(uploaded_file):
    """Uploaded PDF file se text extract karta hai"""
    reader = PdfReader(uploaded_file)
    extracted_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"
    return extracted_text

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=6),
    reraise=True
)
def call_gemini_api(prompt):
    return client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt
    )

# Header Section
st.title("🚀 AI-Powered Cold Email & ATS Optimizer")
st.markdown("Analyze your **Resume (PDF)** against job requirements, calculate real-time **ATS Match Scores**, and generate high-converting cold emails.")

st.divider()

# Input Section: 2 Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Candidate & Customization")
    candidate_name = st.text_input("Candidate Name", value="Manasvi Mishra")
    target_role = st.text_input("Target Job Role", value="AI Software Engineering Intern")
    
    email_tone = st.selectbox(
        "Select Email Tone",
        options=[
            "Professional & Formal (Best for Corporate/MNCs)",
            "Casual & Friendly (Best for Early-stage Startups)",
            "Confident & High-Impact (Best for Tech/Engineering roles)",
            "Persuasive & Sales-Oriented (High-converting pitch)"
        ]
    )
    
    uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    st.subheader("📋 Target Job Description")
    job_description = st.text_area("Paste Job Description (JD) here", height=280, placeholder="We are looking for an AI Engineering Intern skilled in Python, LLMs, and RAG pipelines...")

st.divider()

# Action Button
if st.button("✨ Analyze Resume & Generate Outreach", type="primary", use_container_width=True):
    if not uploaded_resume:
        st.warning("⚠️ Please upload a Resume PDF file before proceeding.")
    elif not job_description.strip():
        st.warning("⚠️ Please paste the Job Description.")
    else:
        with st.spinner("⏳ Processing PDF & running Gemini AI analysis..."):
            try:
                resume_text = extract_text_from_pdf(uploaded_resume)

                prompt = f"""
                You are an elite Tech Executive, Executive Resume Reviewer, and Copywriter.
                Analyze the candidate's background against the job description and create a high-converting outreach package.

                CANDIDATE DETAILS:
                - Name: {candidate_name}
                - Target Role: {target_role}
                - Resume Content:
                {resume_text}

                JOB DESCRIPTION:
                {job_description}

                TONE OF THE EMAIL:
                - Write the email strictly in a **{email_tone}** tone.

                INSTRUCTIONS:
                1. Calculate an ATS Match Score (0-100%) comparing the background to the JD.
                2. Identify top skill overlaps between candidate background and JD.
                3. Identify top 3 critical missing keywords/skills from the resume that the JD requires.
                4. Write a high-converting Cold Email using the AIDA framework matching the tone ({email_tone}):
                   - Subject Line: Catchy and tailored.
                   - Body: Highlight skill fit with strong CTA under 150 words.

                FORMAT YOUR OUTPUT EXACTLY AS FOLLOWS (Keep headers exact):
                MATCH_SCORE: [Number only, e.g. 85]
                KEY_SKILLS: [Comma-separated matching skills]
                MISSING_KEYWORDS: [Comma-separated missing keywords]
                EMAIL_SUBJECT: [Catchy Subject]
                EMAIL_BODY:
                [Full email body starting with Hi Recruiter, up to Sign-off]
                """

                response = call_gemini_api(prompt)
                raw_text = response.text

                # Parse Structured Output
                score_match = re.search(r"MATCH_SCORE:\s*(\d+)", raw_text)
                skills_match = re.search(r"KEY_SKILLS:\s*(.*)", raw_text)
                missing_match = re.search(r"MISSING_KEYWORDS:\s*(.*)", raw_text)
                subject_match = re.search(r"EMAIL_SUBJECT:\s*(.*)", raw_text)
                body_match = re.search(r"EMAIL_BODY:\s*([\s\S]*)", raw_text)

                score = score_match.group(1) if score_match else "N/A"
                skills = skills_match.group(1).strip() if skills_match else "N/A"
                missing = missing_match.group(1).strip() if missing_match else "N/A"
                subject = subject_match.group(1).strip() if subject_match else "Cold Email"
                body = body_match.group(1).strip() if body_match else raw_text

                full_email_text = f"Subject: {subject}\n\n{body}"

                st.success("✅ Analysis Complete!")

                # UI Upgrade Component: Metrics Cards
                st.markdown("### 📊 Overview & Metrics")
                m_col1, m_col2, m_col3 = st.columns(3)
                
                with m_col1:
                    st.metric(label="ATS Match Score", value=f"{score}%", delta="Target > 80%")
                with m_col2:
                    st.metric(label="Tone Applied", value=email_tone.split(" ")[0])
                with m_col3:
                    st.metric(label="Keywords Extracted", value="Complete")

                st.divider()

                # UI Upgrade Component: Organized Tabs
                tab1, tab2 = st.tabs(["✉️ Generated Cold Email", "📈 ATS Analysis & Keywords"])

                with tab1:
                    st.subheader("Personalized Cold Email Draft")
                    st.text_input("Subject Line", value=subject, disabled=True)
                    st.text_area("Email Content", value=body, height=220)
                    
                    # 1-Click Copy Area
                    st.caption("📋 Use the copy icon at the top right of the code block below for 1-click copy:")
                    st.code(full_email_text, language="markdown")

                with tab2:
                    st.subheader("ATS Compatibility Breakdown")
                    st.markdown(f"**🎯 Key Skill Overlaps:**\n{skills}")
                    st.markdown(f"**⚠️ Missing Keywords to Add:**\n{missing}")

            except Exception as e:
                st.error("⚠️ Google API server experienced high demand. Please try clicking again in a few seconds.")