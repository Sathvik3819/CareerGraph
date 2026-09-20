import { useEffect, useState } from "react";
import { apiFetch } from "../utils/api";

function ResumeHistory({ refreshKey, onSelectResume }) {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchHistory();
  }, [refreshKey]);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      setError("");
      const response = await apiFetch("/api/resume/history");

      if (!response.ok) throw new Error("Failed to load resume history");

      const data = await response.json();
      setResumes(data.resumes);
    } catch (error) {
      console.error(error);
      setError("Unable to load resume history.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <section className="history-section">
        <div className="history-header">
          <h2>Resume History</h2>
        </div>
        <div className="history-loading">Loading previous resumes...</div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="history-section">
        <div className="history-header">
          <h2>Resume History</h2>
        </div>
        <div className="history-error">{error}</div>
      </section>
    );
  }

  return (
    <section id="resume-history" className="history-section">
      <div className="history-header">
        <div>
          <h2>Resume History</h2>
          <p>View resumes you generated previously.</p>
        </div>
        <button className="history-refresh" onClick={fetchHistory}>
          Refresh
        </button>
      </div>

      {resumes.length === 0 ? (
        <div className="history-empty">
          <h3>No resumes yet</h3>
          <p>Generate your first tailored resume to see it here.</p>
        </div>
      ) : (
        <div className="history-list">
          {resumes.map((resume) => (
            <div className="history-card" key={resume.id}>
              <div className="history-card-main">
                <div>
                  <h3>{resume.job_role}</h3>
                  <p className="history-candidate">{resume.candidate_name}</p>
                  <p className="history-date">{new Date(resume.created_at).toLocaleString()}</p>
                </div>

                <div className="history-badges">
                  <span className={`decision-badge ${resume.decision === "APPROVED" ? "approved" : "revise"}`}>
                    {resume.decision}
                  </span>
                  <span className="template-badge">{resume.template}</span>
                </div>
              </div>

              <div className="history-stats">
                <div>
                  <span>ATS Score</span>
                  <strong>{resume.ats_score}%</strong>
                </div>
                <div>
                  <span>Review Score</span>
                  <strong>{resume.review_score}%</strong>
                </div>
                <div>
                  <span>Iterations</span>
                  <strong>{resume.iterations}</strong>
                </div>
              </div>

              <button className="history-view-btn" onClick={() => onSelectResume(resume.id)}>
                View Resume
              </button>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default ResumeHistory;