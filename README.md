# AI-Powered Resume Analyzer & Career Recommendation System

A modern resume analysis tool built with Python and Streamlit that helps students and job seekers optimize their resumes for ATS compatibility and discover suitable career paths.

## Features

✅ **PDF Resume Upload** – Extract text automatically  
✅ **ATS Score Calculation** – Evaluate resume structure and completeness (0-100)  
✅ **Skill Extraction** – Detect technical and soft skills  
✅ **Career Recommendations** – Suggest suitable job roles based on skills  
✅ **Missing Skills Detection** – Identify gaps for target career paths  
✅ **Resume Improvement Suggestions** – Actionable feedback  
✅ **Interactive Dashboard** – Real-time analysis results  

## Technology Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **PDF Processing:** PyPDF2
- **NLP:** NLTK, Pandas
- **ML:** Scikit-learn
- **Database:** SQLite (optional)

## Installation

1. Clone the repository:
```bash
cd "AI resume analyzer"
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Start the Streamlit app:
```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

### Steps:
1. Upload a PDF resume
2. (Optional) Enter a target job description or career role
3. View the ATS score, skills analysis, and recommendations
4. See career path suggestions and missing skills

## Project Structure

```
AI resume analyzer/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── src/
│   ├── pdf_extractor.py     # PDF text extraction
│   ├── skill_detector.py    # Skill detection & extraction
│   ├── ats_calculator.py    # ATS score calculation
│   ├── career_recommender.py # Career recommendations
│   └── database.py          # SQLite database operations
└── README.md                # This file
```

## Sample Skills Detected

Programming Languages: Python, Java, JavaScript, C++, SQL, R, Go  
Frontend: React, Angular, Vue.js, HTML, CSS  
Backend: Node.js, Django, Flask, Spring  
ML/Data: Machine Learning, TensorFlow, PyTorch, Pandas, NumPy  
Cloud: AWS, Azure, Google Cloud  
Databases: MySQL, PostgreSQL, MongoDB  
Tools: Git, Docker, Kubernetes  

## Sample Career Paths

- **Software Developer** – Requires: Java, Python, JavaScript, Git
- **Data Scientist** – Requires: Python, SQL, Machine Learning, Statistics
- **Web Developer** – Requires: HTML, CSS, JavaScript, React
- **Data Analyst** – Requires: SQL, Python, Excel, Tableau
- **ML Engineer** – Requires: Python, Machine Learning, TensorFlow, PyTorch

## Resume Scoring Rubric

| Component | Weight | Details |
|-----------|--------|---------|
| Structure | 20% | Presence of sections: Education, Skills, Experience, Projects |
| Skills | 25% | Number and relevance of technical skills |
| Keywords | 20% | Industry-relevant keywords and ATS terms |
| Experience | 15% | Work experience, internships, projects |
| Achievements | 10% | Action verbs, metrics, and measurable results |
| Certifications | 10% | Relevant certifications and courses |

## Future Enhancements

- [ ] LinkedIn profile import
- [ ] Resume template generator
- [ ] OpenAI-powered rewrite suggestions
- [ ] Resume comparison with job postings
- [ ] User accounts and history tracking
- [ ] Export improvement checklist as PDF
