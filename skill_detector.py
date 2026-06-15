import json
import re
from typing import List, Dict

# Comprehensive skills database
SKILLS_DATABASE = {
    "programming_languages": [
        "python", "java", "javascript", "c++", "c#", "sql", "r", "go", "rust", 
        "kotlin", "swift", "objective-c", "typescript", "perl", "ruby", "php"
    ],
    "frontend": [
        "react", "angular", "vue.js", "svelte", "next.js", "html", "css", 
        "tailwind", "bootstrap", "material-ui", "webpack", "babel"
    ],
    "backend": [
        "node.js", "django", "flask", "spring", "fastapi", "express", "asp.net",
        "laravel", "ruby on rails", "golang", "graphql", "rest api"
    ],
    "ml_data": [
        "machine learning", "deep learning", "tensorflow", "pytorch", "keras", 
        "scikit-learn", "pandas", "numpy", "nlp", "computer vision", "statistics",
        "data analysis", "data science", "cv", "bert", "gpt"
    ],
    "cloud": [
        "aws", "azure", "google cloud", "gcp", "heroku", "vercel", "netlify",
        "firebase", "docker", "kubernetes", "lambda", "ec2"
    ],
    "databases": [
        "mysql", "postgresql", "mongodb", "redis", "cassandra", "elasticsearch",
        "dynamodb", "firestore", "sqlite", "oracle", "sql server"
    ],
    "tools_devops": [
        "git", "github", "gitlab", "bitbucket", "jira", "jenkins", "ci/cd",
        "docker", "kubernetes", "terraform", "ansible", "docker-compose"
    ],
    "soft_skills": [
        "communication", "leadership", "teamwork", "project management", 
        "problem solving", "critical thinking", "collaboration", "presentation"
    ]
}

def extract_skills(resume_text: str) -> Dict[str, List[str]]:
    """
    Extract skills from resume text.
    
    Args:
        resume_text: The resume content as a string
        
    Returns:
        Dictionary with detected skills by category
    """
    text_lower = resume_text.lower()
    detected_skills = {category: [] for category in SKILLS_DATABASE}
    
    for category, skills in SKILLS_DATABASE.items():
        for skill in skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                detected_skills[category].append(skill)
    
    return detected_skills

def get_all_skills_flat(detected_skills: Dict[str, List[str]]) -> List[str]:
    """
    Flatten detected skills into a single list.
    
    Args:
        detected_skills: Dictionary with skills by category
        
    Returns:
        Flat list of all detected skills
    """
    all_skills = []
    for skills_list in detected_skills.values():
        all_skills.extend(skills_list)
    return list(set(all_skills))  # Remove duplicates

def count_skills_by_category(detected_skills: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Count skills per category.
    
    Args:
        detected_skills: Dictionary with skills by category
        
    Returns:
        Count of skills per category
    """
    return {category: len(skills) for category, skills in detected_skills.items()}
