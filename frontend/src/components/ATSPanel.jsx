function ATSPanel({ analysis }) {
  if (!analysis) return null;

  return (
    <div className="ats-panel">
      <div className="ats-header">
        <div>
          <h2>ATS Analysis</h2>
          <p>Deterministic match against the job requirements.</p>
        </div>

        <div className="ats-main-score">
          <strong>{analysis.overall_score}</strong>
          <span>/ 100</span>
        </div>
      </div>

      <div className="ats-score-grid">
        <div className="ats-score-card">
          <span>Required Skills</span>
          <strong>{analysis.required_skill_match_score}%</strong>
        </div>
        <div className="ats-score-card">
          <span>Preferred Skills</span>
          <strong>{analysis.preferred_skill_match_score}%</strong>
        </div>
        <div className="ats-score-card">
          <span>Keyword Match</span>
          <strong>{analysis.keyword_match_score}%</strong>
        </div>
        <div className="ats-score-card">
          <span>Section Coverage</span>
          <strong>{analysis.section_score}%</strong>
        </div>
      </div>

      <div className="ats-section">
        <div className="ats-subsection">
          <h3>Matched required skills</h3>
          <div className="ats-tags">
            {analysis.matched_required_skills.length > 0 ? (
              analysis.matched_required_skills.map((skill, index) => (
                <span className="ats-tag matched" key={`matched-skill-${index}`}>
                  {skill}
                </span>
              ))
            ) : (
              <span className="ats-tag missing">No required skills matched</span>
            )}
          </div>
        </div>

        <div className="ats-subsection">
          <h3>Missing required skills</h3>
          <div className="ats-tags">
            {analysis.missing_required_skills.length > 0 ? (
              analysis.missing_required_skills.map((skill, index) => (
                <span className="ats-tag missing" key={`missing-skill-${index}`}>
                  {skill}
                </span>
              ))
            ) : (
              <span className="ats-tag matched">All required skills are covered</span>
            )}
          </div>
        </div>

        <div className="ats-subsection">
          <h3>Matched preferred skills</h3>
          <div className="ats-tags">
            {analysis.matched_preferred_skills.length > 0 ? (
              analysis.matched_preferred_skills.map((skill, index) => (
                <span className="ats-tag matched" key={`matched-preferred-${index}`}>
                  {skill}
                </span>
              ))
            ) : (
              <span className="ats-tag missing">No preferred skills matched</span>
            )}
          </div>
        </div>

        <div className="ats-subsection">
          <h3>Missing preferred skills</h3>
          <div className="ats-tags">
            {analysis.missing_preferred_skills.length > 0 ? (
              analysis.missing_preferred_skills.map((skill, index) => (
                <span className="ats-tag missing" key={`missing-preferred-${index}`}>
                  {skill}
                </span>
              ))
            ) : (
              <span className="ats-tag matched">All preferred skills are covered</span>
            )}
          </div>
        </div>

        <div className="ats-subsection">
          <h3>Matched keywords</h3>
          <div className="ats-tags">
            {analysis.matched_keywords.length > 0 ? (
              analysis.matched_keywords.map((keyword, index) => (
                <span className="ats-tag matched" key={`matched-keyword-${index}`}>
                  {keyword}
                </span>
              ))
            ) : (
              <span className="ats-tag missing">No keywords matched</span>
            )}
          </div>
        </div>

        <div className="ats-subsection">
          <h3>Missing keywords</h3>
          <div className="ats-tags">
            {analysis.missing_keywords.length > 0 ? (
              analysis.missing_keywords.map((keyword, index) => (
                <span className="ats-tag missing" key={`missing-keyword-${index}`}>
                  {keyword}
                </span>
              ))
            ) : (
              <span className="ats-tag matched">No missing keywords</span>
            )}
          </div>
        </div>

        {analysis.missing_sections.length > 0 && (
          <div className="ats-section">
            <h3>Missing sections</h3>
            <ul className="ats-missing-sections">
              {analysis.missing_sections.map((section, index) => (
                <li key={`missing-section-${index}`}>{section}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default ATSPanel;