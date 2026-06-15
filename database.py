import sqlite3
from typing import List, Dict, Optional
from datetime import datetime

class ResumeDatabase:
    """SQLite database manager for storing resume analysis history."""
    
    def __init__(self, db_path: str = "resume_analyzer.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Resumes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ats_score REAL NOT NULL,
                word_count INTEGER NOT NULL,
                extracted_text TEXT
            )
        """)
        
        # Skills table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER NOT NULL,
                skill TEXT NOT NULL,
                category TEXT,
                FOREIGN KEY (resume_id) REFERENCES resumes(id)
            )
        """)
        
        # Career recommendations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS career_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER NOT NULL,
                career TEXT NOT NULL,
                match_score REAL NOT NULL,
                FOREIGN KEY (resume_id) REFERENCES resumes(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_resume_analysis(self, filename: str, ats_score: float, 
                           word_count: int, extracted_text: str,
                           detected_skills: Dict[str, List[str]],
                           career_recommendations: List[tuple]) -> int:
        """
        Save resume analysis to database.
        
        Args:
            filename: Resume filename
            ats_score: Calculated ATS score
            word_count: Word count of resume
            extracted_text: Full extracted text
            detected_skills: Dictionary of detected skills
            career_recommendations: List of career recommendations
            
        Returns:
            Resume ID in database
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert resume
        cursor.execute("""
            INSERT INTO resumes (filename, ats_score, word_count, extracted_text)
            VALUES (?, ?, ?, ?)
        """, (filename, ats_score, word_count, extracted_text))
        
        resume_id = cursor.lastrowid
        
        # Insert skills
        for category, skills in detected_skills.items():
            for skill in skills:
                cursor.execute("""
                    INSERT INTO skills (resume_id, skill, category)
                    VALUES (?, ?, ?)
                """, (resume_id, skill, category))
        
        # Insert career recommendations
        for career, score, _ in career_recommendations:
            cursor.execute("""
                INSERT INTO career_recommendations (resume_id, career, match_score)
                VALUES (?, ?, ?)
            """, (resume_id, career, score))
        
        conn.commit()
        conn.close()
        
        return resume_id
    
    def get_resume_history(self, limit: int = 10) -> List[Dict]:
        """Get recent resume analyses."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, filename, upload_date, ats_score, word_count
            FROM resumes
            ORDER BY upload_date DESC
            LIMIT ?
        """, (limit,))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def get_resume_skills(self, resume_id: int) -> Dict[str, List[str]]:
        """Get skills for a specific resume."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT category, skill FROM skills
            WHERE resume_id = ?
            ORDER BY category
        """, (resume_id,))
        
        skills_dict = {}
        for row in cursor.fetchall():
            category = row["category"]
            if category not in skills_dict:
                skills_dict[category] = []
            skills_dict[category].append(row["skill"])
        
        conn.close()
        return skills_dict
