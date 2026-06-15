const nlp = require('compromise');

const skillKeywords = [
  'python', 'javascript', 'react', 'node', 'sql', 'machine learning', 'data analysis',
  'nlp', 'cloud', 'aws', 'azure', 'git', 'docker', 'kubernetes', 'rest api', 'tensorflow',
  'pytorch', 'analysis', 'communication', 'presentation'
];

const achievementTriggers = [
  'increased', 'reduced', 'improved', 'optimized', 'led', 'launched', 'built', 'designed',
  'automated', 'accelerated'
];

const educationSections = ['education', 'degree', 'bachelor', 'master', 'bs', 'ms', 'phd'];

function extractTextTokens(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter(Boolean);
}

function extractKeywords(text, keywords) {
  const lower = text.toLowerCase();
  return keywords.filter((keyword) => lower.includes(keyword));
}

function buildRecommendations(matches, missing, resumeText, jobDescription) {
  const recs = [];

  if (missing.length > 0) {
    recs.push(`Include more of these target keywords from the job description: ${missing.slice(0, 8).join(', ')}.`);
  }

  if (matches.actionVerbs.length < 2) {
    recs.push('Use stronger achievement verbs such as increased, reduced, optimized, launched, or automated.');
  }

  if (!educationSections.some((section) => resumeText.toLowerCase().includes(section))) {
    recs.push('Add an Education section if it is missing or not clearly labeled.');
  }

  if (resumeText.length < 800) {
    recs.push('Expand bullet points with measurable results and actionable outcomes.');
  }

  if (jobDescription && !resumeText.toLowerCase().includes('project')) {
    recs.push('Highlight relevant projects or internship experience that maps to the job description.');
  }

  return recs;
}

function getJobKeywords(jobDescription) {
  if (!jobDescription) return [];
  const doc = nlp(jobDescription);
  const nouns = doc.nouns().out('frequency');
  const sorted = nouns
    .filter((item) => item.normal && item.normal.length > 3)
    .slice(0, 20)
    .map((item) => item.normal);
  return Array.from(new Set(sorted));
}

function analyzeResume({ resumeText, jobDescription = '' }) {
  const tokens = extractTextTokens(resumeText);
  const uniqueTokens = new Set(tokens);
  const wordCount = tokens.length;

  const matchedSkills = extractKeywords(resumeText, skillKeywords);
  const actionVerbs = extractKeywords(resumeText, achievementTriggers);
  const matchedEducation = extractKeywords(resumeText, educationSections);

  const jobKeywords = getJobKeywords(jobDescription);
  const matchedJobKeywords = jobKeywords.filter((keyword) => resumeText.toLowerCase().includes(keyword));
  const missingJobKeywords = jobKeywords.filter((keyword) => !resumeText.toLowerCase().includes(keyword));

  const scoreComponents = {
    length: Math.min(20, Math.max(0, (wordCount - 200) / 40)),
    skills: Math.min(30, matchedSkills.length * 3),
    jobMatch: Math.min(30, matchedJobKeywords.length * 2),
    achievements: Math.min(10, actionVerbs.length * 2),
    education: matchedEducation.length > 0 ? 10 : 0
  };

  const score = Math.round(
    scoreComponents.length +
      scoreComponents.skills +
      scoreComponents.jobMatch +
      scoreComponents.achievements +
      scoreComponents.education
  );

  const recommendations = buildRecommendations(
    { actionVerbs, matchedSkills, matchedEducation },
    missingJobKeywords,
    resumeText,
    jobDescription
  );

  return {
    score: Math.min(100, score),
    summary: {
      wordCount,
      matchedSkills,
      actionVerbs,
      educationSectionsFound: matchedEducation,
      jobKeywordsFound: matchedJobKeywords.slice(0, 12)
    },
    breakdown: scoreComponents,
    recommendations,
    jobKeywords: jobKeywords.slice(0, 12),
    missingJobKeywords: missingJobKeywords.slice(0, 12)
  };
}

module.exports = { analyzeResume };
