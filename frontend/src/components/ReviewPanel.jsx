function ReviewPanel({ review, iterations = 0 }) {
  if (!review) return null;

  return (
    <div className="review-panel">
      <div className="review-header">
        <div>
          <h2>AI Resume Review</h2>
          <p>Evaluated against your target job description.</p>
        </div>

        <span
          className={`decision-badge ${review.decision === "APPROVED" ? "approved" : "revise"}`}
        >
          {review.decision}
        </span>
      </div>

      <div className="score-grid">
        <div className="score-card">
          <span>Overall Score</span>
          <strong>{review.score}</strong>
          <small>/ 100</small>
        </div>
        <div className="score-card">
          <span>Job Match</span>
          <strong>{review.job_match_score}</strong>
          <small>/ 100</small>
        </div>
        <div className="score-card">
          <span>ATS Compatibility</span>
          <strong>{review.ats_score}</strong>
          <small>/ 100</small>
        </div>
        <div className="score-card">
          <span>Factual Consistency</span>
          <strong>{review.factual_consistency_score}</strong>
          <small>/ 100</small>
        </div>
      </div>

      <div className="iteration-info">
        Resume iterations: <strong>{iterations}</strong>
      </div>

      {review.strengths.length > 0 && (
        <div className="review-section">
          <h3>Strengths</h3>
          <ul className="strength-list">
            {review.strengths.map((strength, index) => (
              <li key={index}>
                <span>✓</span>
                {strength}
              </li>
            ))}
          </ul>
        </div>
      )}

      {review.missing_keywords.length > 0 && (
        <div className="review-section">
          <h3>Missing Keywords</h3>
          <div className="keyword-list">
            {review.missing_keywords.map((keyword, index) => (
              <span className="keyword-tag" key={index}>
                {keyword}
              </span>
            ))}
          </div>
        </div>
      )}

      {review.issues.length > 0 && (
        <div className="review-section">
          <h3>Issues</h3>
          <ul className="issue-list">
            {review.issues.map((issue, index) => (
              <li key={index}>{issue}</li>
            ))}
          </ul>
        </div>
      )}

      {review.suggestions.length > 0 && (
        <div className="review-section">
          <h3>Suggestions</h3>
          <ul className="suggestion-list">
            {review.suggestions.map((suggestion, index) => (
              <li key={index}>{suggestion}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default ReviewPanel;