import re
from typing import Dict, List

# Resume sections to check for ATS compatibility
REQUIRED_SECTIONS = [
    "education", "experience", "skills", "project", "certification"
]

# Action verbs that improve ATS score
ACTION_VERBS = [
    "developed", "designed", "implemented", "created", "built", "engineered",
    "led", "managed", "coordinated", "achieved", "increased", "improved",
    "optimized", "automated", "accelerated", "launched", "directed", "spearheaded",
    "resolved", "pioneered", "deployed", "executed", "collaborated"
]

# Keywords that help ATS parsing
ATS_KEYWORDS = [
    "responsible for", "proficient in", "experienced in", "skilled in",
    "competent in", "expertise in", "knowledge of", "proficiency"
]

def calculate_ats_score(resume_text: str) -> Dict:
    """
    Calculate ATS compatibility score for a resume.
    
    Args:
        resume_text: The resume content as a string
        
    Returns:
        Dictionary containing score breakdown and total score
    """
    text_lower = resume_text.lower()
    text_words = resume_text.split()
    
    score_breakdown = {}
    total_score = 0
    
    # 1. Check for required sections (20 points)
    sections_found = 0
    for section in REQUIRED_SECTIONS:
        if section in text_lower:
            sections_found += 1
    sections_score = (sections_found / len(REQUIRED_SECTIONS)) * 20
    score_breakdown["sections"] = round(sections_score, 1)
    total_score += sections_score
    
    # 2. Check for action verbs (15 points)
    action_verbs_count = sum(1 for verb in ACTION_VERBS if verb in text_lower)
    action_verbs_score = min(15, action_verbs_count * 1.5)
    score_breakdown["action_verbs"] = round(action_verbs_score, 1)
    total_score += action_verbs_score
    
    # 3. Check for ATS keywords (10 points)
    ats_keywords_count = sum(1 for keyword in ATS_KEYWORDS if keyword in text_lower)
    ats_keywords_score = min(10, ats_keywords_count * 2)
    score_breakdown["ats_keywords"] = round(ats_keywords_score, 1)
    total_score += ats_keywords_score
    
    # 4. Resume length (15 points - should be 400-1000 words)
    word_count = len(text_words)
    if 400 <= word_count <= 1000:
        length_score = 15
    elif 300 <= word_count <= 1200:
        length_score = 12
    elif word_count > 1200:
        length_score = 8
    elif word_count >= 200:
        length_score = 5
    else:
        length_score = 0
    score_breakdown["length"] = length_score
    total_score += length_score
    
    # 5. Contact information (10 points)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    contact_score = 0
    if re.search(email_pattern, resume_text):
        contact_score += 5
    if re.search(phone_pattern, resume_text):
        contact_score += 5
    score_breakdown["contact_info"] = contact_score
    total_score += contact_score
    
    # 6. Formatting indicators (10 points)
    formatting_score = 0
    # Check for bullet points
    if resume_text.count("•") + resume_text.count("•") + resume_text.count("-") > 5:
        formatting_score += 5
    # Check for clear line breaks and structure
    if len(resume_text.split("\n")) > 10:
        formatting_score += 5
    score_breakdown["formatting"] = formatting_score
    total_score += formatting_score
    
    # 7. Quantifiable achievements (10 points)
    quantifiable_pattern = r'\b(\d+%|\d+\+|\$\d+|[\d,]+\+?)\b'
    quantifiable_count = len(re.findall(quantifiable_pattern, resume_text))
    quantifiable_score = min(10, quantifiable_count * 1.5)
    score_breakdown["quantifiable"] = round(quantifiable_score, 1)
    total_score += quantifiable_score
    
    # 8. Spacing and readability (10 points)
    lines = resume_text.split("\n")
    avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
    if 40 <= avg_line_length <= 90:
        readability_score = 10
    elif 30 <= avg_line_length <= 100:
        readability_score = 7
    else:
        readability_score = 3
    score_breakdown["readability"] = readability_score
    total_score += readability_score
    
    final_score = min(100, round(total_score, 1))
    
    return {
        "score": final_score,
        "breakdown": score_breakdown,
        "word_count": word_count,
        "sections_found": sections_found,
        "total_sections": len(REQUIRED_SECTIONS)
    }

def get_ats_recommendations(resume_text: str, ats_data: Dict) -> List[str]:
    """
    Generate ATS improvement recommendations.
    
    Args:
        resume_text: The resume content
        ats_data: ATS score data
        
    Returns:
        List of recommendations
    """
    recommendations = []
    text_lower = resume_text.lower()
    
    if ats_data["sections_found"] < ats_data["total_sections"]:
        missing = []
        for section in REQUIRED_SECTIONS:
            if section not in text_lower:
                missing.append(section.capitalize())
        if missing:
            recommendations.append(f"Add missing sections: {', '.join(missing)}")
    
    if ats_data["word_count"] < 400:
        recommendations.append("Expand your resume to at least 400 words for better ATS parsing")
    elif ats_data["word_count"] > 1200:
        recommendations.append("Consider condensing your resume to around 1000 words or less")
    
    action_verbs_count = sum(1 for verb in ACTION_VERBS if verb in text_lower)
    if action_verbs_count < 5:
        recommendations.append("Use more action verbs like 'developed', 'led', 'improved', 'implemented'")
    
    if not re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resume_text):
        recommendations.append("Ensure your email address is clearly visible")
    
    if resume_text.count("•") + resume_text.count("-") < 10:
        recommendations.append("Use bullet points to structure your achievements")
    
    return recommendations if recommendations else ["Your resume is well-optimized!"]
