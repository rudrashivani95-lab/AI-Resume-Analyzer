import { useState } from 'react';

const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:4000';

function App() {
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleAnalyze(event) {
    event.preventDefault();
    setLoading(true);
    setError('');
    setAnalysis(null);

    try {
      const response = await fetch(`${backendUrl}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resumeText, jobDescription })
      });

      if (!response.ok) {
        const json = await response.json();
        throw new Error(json.error || 'Failed to analyze resume');
      }

      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <header>
        <h1>AI Resume Analyzer</h1>
        <p>Measure ATS fit, keyword match, and resume improvement recommendations.</p>
      </header>

      <form className="analyzer-form" onSubmit={handleAnalyze}>
        <label>
          Resume text
          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="Paste your resume here"
            rows="12"
          />
        </label>

        <label>
          Job description
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description you want to optimize for"
            rows="8"
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Resume'}
        </button>
      </form>

      {error && <div className="error-box">{error}</div>}

      {analysis && (
        <section className="results-panel">
          <div className="score-card">
            <h2>ATS Score</h2>
            <p className="score-value">{analysis.score}/100</p>
          </div>

          <div className="breakdown">
            <h3>Score breakdown</h3>
            <ul>
              <li>Length: {analysis.breakdown.length.toFixed(1)}</li>
              <li>Skills: {analysis.breakdown.skills}</li>
              <li>Job match: {analysis.breakdown.jobMatch}</li>
              <li>Achievements: {analysis.breakdown.achievements}</li>
              <li>Education: {analysis.breakdown.education}</li>
            </ul>
          </div>

          <div className="summary-grid">
            <div>
              <h3>Matched skills</h3>
              <p>{analysis.summary.matchedSkills.join(', ') || 'None detected'}</p>
            </div>
            <div>
              <h3>Action verbs</h3>
              <p>{analysis.summary.actionVerbs.join(', ') || 'None detected'}</p>
            </div>
            <div>
              <h3>Job keywords found</h3>
              <p>{analysis.summary.jobKeywordsFound.join(', ') || 'None detected'}</p>
            </div>
          </div>

          <div className="recommendations">
            <h3>Recommendations</h3>
            <ol>
              {analysis.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ol>
          </div>

          <div className="keyword-lists">
            <div>
              <h3>Target keywords</h3>
              <p>{analysis.jobKeywords.join(', ') || 'No keywords found'}</p>
            </div>
            <div>
              <h3>Missing keywords</h3>
              <p>{analysis.missingJobKeywords.join(', ') || 'None detected'}</p>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}

export default App;
