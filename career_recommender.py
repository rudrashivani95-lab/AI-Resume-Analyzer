from typing import Dict, List, Tuple

# Career paths and their required skills
CAREER_PATHS = {
    "Software Developer": {
        "required_skills": ["python", "java", "javascript", "sql", "git", "rest api"],
        "preferred_skills": ["react", "node.js", "docker", "spring"],
        "description": "Build and maintain software applications across various platforms"
    },
    "Data Scientist": {
        "required_skills": ["python", "machine learning", "sql", "statistics", "pandas", "numpy"],
        "preferred_skills": ["tensorflow", "pytorch", "deep learning", "nlp", "r"],
        "description": "Analyze complex datasets and build predictive models"
    },
    "Web Developer": {
        "required_skills": ["html", "css", "javascript", "react", "git"],
        "preferred_skills": ["node.js", "angular", "vue.js", "typescript", "rest api"],
        "description": "Create responsive and interactive web applications"
    },
    "Data Analyst": {
        "required_skills": ["sql", "python", "excel", "statistics", "data analysis"],
        "preferred_skills": ["tableau", "power bi", "pandas", "r"],
        "description": "Extract insights from data to support business decisions"
    },
    "Machine Learning Engineer": {
        "required_skills": ["python", "machine learning", "tensorflow", "pytorch", "sql"],
        "preferred_skills": ["deep learning", "nlp", "computer vision", "kubernetes", "aws"],
        "description": "Develop and deploy machine learning models at scale"
    },
    "DevOps Engineer": {
        "required_skills": ["docker", "kubernetes", "git", "ci/cd", "aws"],
        "preferred_skills": ["terraform", "ansible", "jenkins", "linux", "python"],
        "description": "Manage infrastructure, deployment pipelines, and cloud platforms"
    },
    "Frontend Developer": {
        "required_skills": ["javascript", "react", "html", "css", "git"],
        "preferred_skills": ["typescript", "angular", "vue.js", "webpack", "tailwind"],
        "description": "Build user-facing web applications with focus on UI/UX"
    },
    "Backend Developer": {
        "required_skills": ["python", "java", "sql", "rest api", "node.js"],
        "preferred_skills": ["django", "spring", "fastapi", "graphql", "docker"],
        "description": "Develop server-side logic and database systems"
    }
}

def recommend_careers(detected_skills: Dict[str, List[str]]) -> List[Tuple[str, float, Dict]]:
    """
    Recommend suitable careers based on detected skills.
    
    Args:
        detected_skills: Dictionary with skills by category
        
    Returns:
        List of tuples (career_name, match_score, career_info) sorted by score
    """
    all_skills = []
    for skills_list in detected_skills.values():
        all_skills.extend(skills_list)
    
    all_skills_lower = [s.lower() for s in all_skills]
    
    career_scores = []
    
    for career, info in CAREER_PATHS.items():
        required = [s.lower() for s in info["required_skills"]]
        preferred = [s.lower() for s in info["preferred_skills"]]
        
        # Calculate match
        required_matches = sum(1 for skill in required if skill in all_skills_lower)
        preferred_matches = sum(1 for skill in preferred if skill in all_skills_lower)
        
        # Weighted scoring
        required_score = (required_matches / len(required)) * 100 if required else 0
        preferred_score = (preferred_matches / len(preferred)) * 100 if preferred else 0
        
        # Combined score (60% required, 40% preferred)
        match_score = (required_score * 0.6) + (preferred_score * 0.4)
        
        career_scores.append((career, round(match_score, 1), info))
    
    # Sort by score descending
    career_scores.sort(key=lambda x: x[1], reverse=True)
    return career_scores

def get_missing_skills(detected_skills: Dict[str, List[str]], target_career: str) -> Dict:
    """
    Get missing skills for a target career.
    
    Args:
        detected_skills: Dictionary with skills by category
        target_career: Target career path name
        
    Returns:
        Dictionary with missing required and preferred skills
    """
    if target_career not in CAREER_PATHS:
        return {"error": "Career not found"}
    
    all_skills = []
    for skills_list in detected_skills.values():
        all_skills.extend(skills_list)
    
    all_skills_lower = [s.lower() for s in all_skills]
    
    career_info = CAREER_PATHS[target_career]
    
    missing_required = [
        skill for skill in career_info["required_skills"]
        if skill.lower() not in all_skills_lower
    ]
    
    missing_preferred = [
        skill for skill in career_info["preferred_skills"]
        if skill.lower() not in all_skills_lower
    ]
    
    return {
        "career": target_career,
        "missing_required": missing_required,
        "missing_preferred": missing_preferred,
        "description": career_info["description"]
    }

def get_career_recommendations(detected_skills: Dict[str, List[str]]) -> List[str]:
    """
    Generate recommendations for skill development.
    
    Args:
        detected_skills: Dictionary with skills by category
        
    Returns:
        List of skill development recommendations
    """
    recommendations = []
    
    all_skills = []
    for skills_list in detected_skills.values():
        all_skills.extend(skills_list)
    
    # Check for programming languages
    prog_langs = detected_skills.get("programming_languages", [])
    if len(prog_langs) < 2:
        recommendations.append("Learn at least 2 programming languages for better job opportunities")
    
    # Check for frontend skills
    frontend = detected_skills.get("frontend", [])
    backend = detected_skills.get("backend", [])
    if not frontend and not backend:
        recommendations.append("Develop either frontend or backend skills for web development roles")
    
    # Check for cloud/devops
    cloud = detected_skills.get("cloud", [])
    if not cloud and len(all_skills) > 5:
        recommendations.append("Consider learning cloud platforms (AWS, Azure, GCP) for modern jobs")
    
    # Check for ML/Data
    ml_data = detected_skills.get("ml_data", [])
    if "python" in [s.lower() for s in all_skills] and not ml_data:
        recommendations.append("With Python skills, consider learning ML libraries: pandas, scikit-learn")
    
    # Check for databases
    databases = detected_skills.get("databases", [])
    if not databases and len(all_skills) > 3:
        recommendations.append("Add database skills (SQL, MongoDB, PostgreSQL)")
    
    # Check for DevOps
    devops = detected_skills.get("tools_devops", [])
    if "git" not in [s.lower() for s in devops]:
        recommendations.append("Master version control with Git/GitHub")
    
    return recommendations if recommendations else ["Your skill set is well-rounded!"]
