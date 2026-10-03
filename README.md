# cold-email-ats-optimizer
Set-Content -Path README.md -Value '# 🚀 AI-Powered Cold Email & ATS Matcher

> An end-to-end, commercial-grade career assistant built with Python, Streamlit, and the Google Gemini API (`gemini-3.8-flash`). It parses candidate resumes against target job descriptions to compute ATS match scores, extract keyword gaps, and generate high-converting, AIDA-framework cold emails across multiple customizable tones.

🌐 **Live Demo Application:** [https://cold-email-ats-optimizer.streamlit.app](https://cold-email-ats-optimizer.streamlit.app)

---

## ✨ Key Features

- **📄 Automated PDF Parsing:** Extracts clean text from uploaded candidate resumes instantly using `pypdf`.
- **📊 Real-Time ATS Match Analysis:** Calculates a percentage match score (0–100%) and categorizes key skill overlaps alongside critical missing keywords.
- **✉️ Multi-Tone Email Generation:** Drafts personalized outreach messages structured around the **AIDA** framework under 150 words.
  - *Professional & Formal* (Corporate / MNCs)
  - *Casual & Friendly* (Early-stage Startups)
  - *Confident & High-Impact* (Tech & Engineering Roles)
  - *Persuasive & Sales-Oriented* (High-Converting Pitch)
- **⚡ Resilient API Handling:** Integrated `tenacity` retry logic with exponential backoff to handle high-traffic Google API 503 errors automatically.
- **🎯 Dashboard Layout:** Modern UI built with Streamlit featuring key metric cards, tabbed outputs, and 1-click code block copying.

---

## 🛠️ Tech Stack

- **Frontend / Web Framework:** [Streamlit](https://streamlit.io/)
- **LLM / AI Model:** [Google Gemini API](https://ai.google.dev/) (`gemini-3.8-flash`) via `google-genai` SDK
- **PDF Extraction:** `pypdf`
- **Fault Tolerance:** `tenacity` (Retry mechanism)
- **Environment Management:** `python-dotenv`

---

## 📂 Project Structure

```text
cold-email-ats-app/
├── app.py              # Main Streamlit web application
├── requirements.txt    # Python dependencies for deployment
├── .env.example        # Environment variable template
├── .gitignore          # Excludes secrets (.env) and venv
└── README.md           # Project documentation
