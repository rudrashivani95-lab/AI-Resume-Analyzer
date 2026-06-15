import streamlit as st
import os
from io import BytesIO

# Configure Tesseract OCR for Windows
try:
    import pytesseract
    # point pytesseract to the Tesseract binary on Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
except:
    pass  # Tesseract not installed yet - will use fallback

# Add src to path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.pdf_extractor import extract_text_from_pdf, extract_text_from_docx
from src.skill_detector import extract_skills, get_all_skills_flat, count_skills_by_category
from src.ats_calculator import calculate_ats_score, get_ats_recommendations
from src.career_recommender import recommend_careers, get_missing_skills, get_career_recommendations
from src.database import ResumeDatabase

# Page configuration
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        background-color: rgba(45, 124, 240, 0.1);
        border-left: 4px solid #2d7cf0;
    }
    .score-display {
        font-size: 3em;
        font-weight: bold;
        color: #2d7cf0;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.title("📄 AI Resume Analyzer & Career Recommendation System")
    st.markdown("Optimize your resume for ATS compatibility and discover your ideal career paths")
    
    # Sidebar
    st.sidebar.header("About")
    st.sidebar.info(
        """
        This tool helps you:
        - Upload your resume (PDF or DOCX)
        - Calculate ATS compatibility score
        - Extract detected skills
        - Get career recommendations
        - Identify missing skills for target roles
        """
    )
    
    # Tab selection
    tab1, tab2, tab3 = st.tabs(["📊 Analyze Resume", "💼 Career Path", "📚 History"])
    
    with tab1:
        st.header("Resume Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Upload your resume (PDF or DOCX)",
                type=["pdf", "docx"]
            )
        
        with col2:
            analyze_button = st.button("🔍 Analyze Resume", use_container_width=True)
        
        if uploaded_file and analyze_button:
            with st.spinner("Analyzing your resume..."):
                # Extract text
                file_bytes = uploaded_file.read()
                
                if uploaded_file.type == "application/pdf":
                    resume_text = extract_text_from_pdf(file_bytes)
                else:
                    resume_text = extract_text_from_docx(file_bytes)
                
                if not resume_text:
                    st.error("❌ Could not extract text from the file. Please check the file format.")
                    st.info(
                        """
                        **Why this happened:**
                        - The PDF might be image-based (scanned document)
                        - The PDF may have special encoding or protection
                        
                        **Solutions:**
                        1. **For scanned PDFs:** Install Tesseract OCR:
                           - Download: https://github.com/UB-Mannheim/tesseract/wiki
                           - Install and add to PATH
                           - Then try uploading again
                        
                        2. **Try a different format:**
                           - Convert PDF to DOCX or text format
                           - Upload the converted file
                        
                        3. **Check file integrity:**
                           - Make sure the PDF is not corrupted
                           - Try opening it in your PDF reader
                        """
                    )
                    return
                
                # Analyze resume
                ats_data = calculate_ats_score(resume_text)
                detected_skills = extract_skills(resume_text)
                career_recs = recommend_careers(detected_skills)
                ats_recs = get_ats_recommendations(resume_text, ats_data)
                skill_recs = get_career_recommendations(detected_skills)
                
                # Save to database
                db = ResumeDatabase()
                db.save_resume_analysis(
                    uploaded_file.name,
                    ats_data["score"],
                    ats_data["word_count"],
                    resume_text,
                    detected_skills,
                    career_recs[:5]
                )
                
                # Display results
                st.success("✅ Analysis complete!")
                
                # ATS Score
                st.subheader("ATS Compatibility Score")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="score-display">{ats_data['score']}/100</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.metric("Word Count", ats_data["word_count"])
                
                with col3:
                    st.metric("Sections Found", f"{ats_data['sections_found']}/{ats_data['total_sections']}")
                
                # Score Breakdown
                st.subheader("Score Breakdown")
                breakdown_cols = st.columns(4)
                breakdown_items = list(ats_data["breakdown"].items())
                
                for i, (component, score) in enumerate(breakdown_items):
                    with breakdown_cols[i % 4]:
                        st.metric(
                            component.replace("_", " ").title(),
                            f"{score}"
                        )
                
                # Skills Detection
                st.subheader("Detected Skills")
                skill_counts = count_skills_by_category(detected_skills)
                
                skill_cols = st.columns(len(skill_counts))
                for i, (category, count) in enumerate(skill_counts.items()):
                    with skill_cols[i]:
                        st.metric(
                            category.replace("_", " ").title(),
                            count
                        )
                
                # Display skills by category
                st.markdown("**Skills by Category:**")
                for category, skills in detected_skills.items():
                    if skills:
                        skills_text = ", ".join(skills)
                        st.write(f"**{category.replace('_', ' ').title()}:** {skills_text}")
                
                # Career Recommendations
                st.subheader("Top Career Recommendations")
                for i, (career, score, info) in enumerate(career_recs[:5], 1):
                    with st.expander(f"{i}. {career} - {score}% match"):
                        st.write(f"**Description:** {info['description']}")
                        st.write(f"**Match Score:** {score}%")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Required Skills:**")
                            for skill in info["required_skills"]:
                                st.write(f"- {skill}")
                        
                        with col2:
                            st.write("**Preferred Skills:**")
                            for skill in info["preferred_skills"]:
                                st.write(f"- {skill}")
                
                # ATS Recommendations
                st.subheader("ATS Improvement Recommendations")
                for i, rec in enumerate(ats_recs, 1):
                    st.write(f"{i}. {rec}")
                
                # Career Development Recommendations
                st.subheader("Career Development Tips")
                for i, rec in enumerate(skill_recs, 1):
                    st.write(f"{i}. {rec}")
    
    with tab2:
        st.header("Career Path Deep Dive")
        
        # Career selection
        career_options = [
            "Software Developer", "Data Scientist", "Web Developer",
            "Data Analyst", "Machine Learning Engineer", "DevOps Engineer",
            "Frontend Developer", "Backend Developer"
        ]
        
        selected_career = st.selectbox("Select a career path", career_options)
        
        uploaded_file = st.file_uploader(
            "Upload resume to analyze gaps (Optional)",
            type=["pdf", "docx"],
            key="career_upload"
        )
        
        if uploaded_file:
            file_bytes = uploaded_file.read()
            
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(file_bytes)
            else:
                resume_text = extract_text_from_docx(file_bytes)
            
            if resume_text:
                detected_skills = extract_skills(resume_text)
                missing_info = get_missing_skills(detected_skills, selected_career)
                
                st.subheader(f"📍 {selected_career}")
                st.write(missing_info["description"])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Missing Required Skills:**")
                    if missing_info["missing_required"]:
                        for skill in missing_info["missing_required"]:
                            st.write(f"🔴 {skill}")
                    else:
                        st.success("✅ You have all required skills!")
                
                with col2:
                    st.write("**Missing Preferred Skills:**")
                    if missing_info["missing_preferred"]:
                        for skill in missing_info["missing_preferred"]:
                            st.write(f"🟡 {skill}")
                    else:
                        st.success("✅ You have all preferred skills!")
    
    with tab3:
        st.header("Analysis History")
        
        db = ResumeDatabase()
        history = db.get_resume_history()
        
        if history:
            for resume in history:
                with st.expander(f"{resume['filename']} - {resume['upload_date']}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("ATS Score", resume['ats_score'])
                    with col2:
                        st.metric("Word Count", resume['word_count'])
                    with col3:
                        st.metric("Resume ID", resume['id'])
        else:
            st.info("No analysis history yet. Upload a resume to get started!")

if __name__ == "__main__":
    main()
