import { useEffect, useState } from "react";
import { apiFetch } from "../utils/api";

function Dashboard({ userName, onCreateResume, onSelectResume }) {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await apiFetch("/api/resume/history");
      if (!response.ok) throw new Error("Failed to load history");

      const data = await response.json();
      setResumes(data.resumes);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const totalResumes = resumes.length;
  const averageATS =
    totalResumes === 0
      ? 0
      : Math.round(
          resumes.reduce((sum, resume) => sum + resume.ats_score, 0) / totalResumes
        );
  const averageReview =
    totalResumes === 0
      ? 0
      : Math.round(
          resumes.reduce((sum, resume) => sum + resume.review_score, 0) / totalResumes
        );
  const approved = resumes.filter((resume) => resume.decision === "APPROVED").length;
  const recentResumes = resumes.slice(0, 5);

  return (
    <section className="dashboard">
      <div className="dashboard-welcome">
        <div>
          <h1>Welcome back, {userName}</h1>
          <p>Tailor your resume for your next opportunity.</p>
        </div>

        <button className="dashboard-primary-btn" onClick={onCreateResume}>
          + Create Resume
        </button>
      </div>

      <div className="dashboard-stats">
        <div className="dashboard-stat-card">
          <span>Total Resumes</span>
          <strong>{totalResumes}</strong>
        </div>
        <div className="dashboard-stat-card">
          <span>Average ATS</span>
          <strong>{averageATS}%</strong>
        </div>
        <div className="dashboard-stat-card">
          <span>Average Review</span>
          <strong>{averageReview}%</strong>
        </div>
        <div className="dashboard-stat-card">
          <span>Approved</span>
          <strong>{approved}</strong>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-panel">
          <div className="dashboard-panel-header">
            <div>
              <h2>Recent Resumes</h2>
              <p>Your latest tailored resumes.</p>
            </div>
          </div>

          {loading ? (
            <div className="dashboard-empty">Loading resumes...</div>
          ) : recentResumes.length === 0 ? (
            <div className="dashboard-empty">
              <h3>No resumes yet</h3>
              <p>Create your first job-tailored resume.</p>
              <button onClick={onCreateResume}>Create Resume</button>
            </div>
          ) : (
            <div className="recent-resume-list">
              {recentResumes.map((resume) => (
                <button
                  key={resume.id}
                  className="recent-resume"
                  onClick={() => onSelectResume(resume.id)}
                >
                  <div>
                    <strong>{resume.job_role}</strong>
                    <span>{new Date(resume.created_at).toLocaleDateString()}</span>
                  </div>

                  <div className="recent-resume-score">
                    <span>ATS</span>
                    <strong>{resume.ats_score}%</strong>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="dashboard-panel">
          <div className="dashboard-panel-header">
            <div>
              <h2>Quick Actions</h2>
              <p>Continue working on your resumes.</p>
            </div>
          </div>

          <div className="quick-actions">
            <button onClick={onCreateResume} className="quick-action">
              <strong>Create Resume</strong>
              <span>Generate a new job-tailored resume</span>
            </button>

            <button
              className="quick-action"
              onClick={() =>
                document.getElementById("resume-history")?.scrollIntoView({
                  behavior: "smooth",
                })
              }
            >
              <strong>Resume History</strong>
              <span>View all your previous resumes</span>
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Dashboard;