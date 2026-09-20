function ResumePreview({
  data,
  generatedResume,
  hasGeneratedResume = false,
  template,
  onDownloadPDF,
}) {
  const resume = generatedResume;
  const name = resume?.header.name || data.personal.name || "Your Name";
  const email = resume?.header.email || data.personal.email;
  const phone = resume?.header.phone || data.personal.phone;
  const location = resume?.header.location || data.personal.location;
  const github = resume?.header.github_url || data.personal.github;
  const linkedin = resume?.header.linkedin_url || data.personal.linkedin;
  const portfolio = resume?.header.portfolio_url || data.personal.portfolio;
  const summary =
    resume?.summary || "Your professional summary will appear here after generating your resume.";
  const skills = resume?.skills || data.skills;

  return (
    <div className="preview-container">
      <div className="preview-header">
        <div>
          <h2>Resume Preview</h2>
          {generatedResume && <span className="ai-badge">AI Generated</span>}
        </div>

        {hasGeneratedResume && (
          <button className="download-btn" onClick={onDownloadPDF} disabled={!hasGeneratedResume}>
            Download PDF
          </button>
        )}
      </div>

      <div className={`resume-page template-${template}`}>
        <header className="resume-header">
          <h1>{name}</h1>

          <div className="contact-info">
            {email && <span>{email}</span>}
            {phone && <span>{phone}</span>}
            {location && <span>{location}</span>}
          </div>

          <div className="resume-links">
            {github && (
              <a href={github} target="_blank" rel="noreferrer">
                GitHub
              </a>
            )}
            {linkedin && (
              <a href={linkedin} target="_blank" rel="noreferrer">
                LinkedIn
              </a>
            )}
            {portfolio && (
              <a href={portfolio} target="_blank" rel="noreferrer">
                Portfolio
              </a>
            )}
          </div>
        </header>

        <ResumeSection title="Professional Summary">
          <p className="resume-text">{summary}</p>
        </ResumeSection>

        {skills.length > 0 && (
          <ResumeSection title="Technical Skills">
            <p className="resume-text">{skills.join(" • ")}</p>
          </ResumeSection>
        )}

        {(resume?.projects?.length || data.projects.length) > 0 && (
          <ResumeSection title="Projects">
            {(resume?.projects || []).map((project, index) => (
              <div className="resume-item" key={index}>
                <div className="resume-item-header">
                  <strong>{project.name}</strong>
                  {project.github_url && (
                    <a href={project.github_url} target="_blank" rel="noreferrer">
                      GitHub
                    </a>
                  )}
                </div>

                <p className="resume-text">{project.description}</p>
                {project.technologies.length > 0 && (
                  <small>
                    <strong>Technologies:</strong> {project.technologies.join(", ")}
                  </small>
                )}
              </div>
            ))}

            {!resume &&
              data.projects.map((project, index) => (
                <div className="resume-item" key={index}>
                  <div className="resume-item-header">
                    <strong>{project.name || "Project Name"}</strong>
                  </div>
                  <p className="resume-text">
                    {project.description || "Project description"}
                  </p>
                  {project.technologies && (
                    <small>
                      <strong>Technologies:</strong> {project.technologies}
                    </small>
                  )}
                </div>
              ))}
          </ResumeSection>
        )}

        {(resume?.experience?.length || data.experience.length) > 0 && (
          <ResumeSection title="Experience">
            {(resume?.experience || []).map((experience, index) => (
              <div className="resume-item" key={index}>
                <div className="resume-item-header">
                  <strong>{experience.role}</strong>
                  <span>{experience.duration}</span>
                </div>
                <div>{experience.company}</div>
                <ul>
                  {experience.description.map((description, i) => (
                    <li key={i}>{description}</li>
                  ))}
                </ul>
              </div>
            ))}
          </ResumeSection>
        )}

        {(resume?.education?.length || data.education.length) > 0 && (
          <ResumeSection title="Education">
            {(resume?.education || []).map((education, index) => (
              <div className="resume-item" key={index}>
                <div className="resume-item-header">
                  <strong>{education.degree}</strong>
                  <span>{education.duration}</span>
                </div>
                <div>{education.institution}</div>
                {education.grade && <small>{education.grade}</small>}
              </div>
            ))}
          </ResumeSection>
        )}

        {(resume?.certifications?.length || data.certifications.length) > 0 && (
          <ResumeSection title="Certifications">
            <ul>
              {(resume?.certifications || data.certifications).map((certification, index) => (
                <li key={index}>{certification}</li>
              ))}
            </ul>
          </ResumeSection>
        )}
      </div>
    </div>
  );
}

function ResumeSection({ title, children }) {
  return (
    <section className="resume-section">
      <h3>{title}</h3>
      {children}
    </section>
  );
}

export default ResumePreview;