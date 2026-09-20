function ResumeEditor({ resume, onChange, originalResume }) {
  const updateHeader = (field, value) => {
    onChange({
      ...resume,
      header: {
        ...resume.header,
        [field]: value,
      },
    });
  };

  const updateProject = (index, field, value) => {
    const projects = [...resume.projects];
    projects[index] = { ...projects[index], [field]: value };

    onChange({
      ...resume,
      projects,
    });
  };

  const updateExperience = (index, field, value) => {
    const experience = [...resume.experience];
    experience[index] = { ...experience[index], [field]: value };

    onChange({
      ...resume,
      experience,
    });
  };

  const updateEducation = (index, field, value) => {
    const education = [...resume.education];
    education[index] = { ...education[index], [field]: value };

    onChange({
      ...resume,
      education,
    });
  };

  return (
    <section className="resume-editor">
      <div className="editor-header">
        <div>
          <h2>Resume Editor</h2>
          <p>Fine-tune your AI-generated resume before downloading it.</p>
        </div>

        {originalResume && (
          <button className="editor-reset-btn" onClick={() => onChange(structuredClone(originalResume))}>
            Reset to AI Version
          </button>
        )}
      </div>

      <div className="editor-section">
        <h3>Contact Information</h3>

        <div className="editor-grid">
          <EditorInput
            label="Name"
            value={resume.header.name}
            onChange={(value) => updateHeader("name", value)}
          />

          <EditorInput
            label="Email"
            value={resume.header.email || ""}
            onChange={(value) => updateHeader("email", value)}
          />

          <EditorInput
            label="Phone"
            value={resume.header.phone || ""}
            onChange={(value) => updateHeader("phone", value)}
          />

          <EditorInput
            label="Location"
            value={resume.header.location || ""}
            onChange={(value) => updateHeader("location", value)}
          />

          <EditorInput
            label="GitHub"
            value={resume.header.github_url || ""}
            onChange={(value) => updateHeader("github_url", value)}
          />

          <EditorInput
            label="LinkedIn"
            value={resume.header.linkedin_url || ""}
            onChange={(value) => updateHeader("linkedin_url", value)}
          />

          <EditorInput
            label="Portfolio"
            value={resume.header.portfolio_url || ""}
            onChange={(value) => updateHeader("portfolio_url", value)}
          />
        </div>
      </div>

      <div className="editor-section">
        <h3>Professional Summary</h3>
        <textarea
          value={resume.summary}
          onChange={(e) => onChange({ ...resume, summary: e.target.value })}
          rows={5}
        />
      </div>

      <div className="editor-section">
        <h3>Skills</h3>
        <input
          value={resume.skills.join(", ")}
          onChange={(e) =>
            onChange({
              ...resume,
              skills: e.target.value
                .split(",")
                .map((skill) => skill.trim())
                .filter(Boolean),
            })
          }
          placeholder="Python, LangChain, React..."
        />
        <p className="editor-help">Separate skills with commas.</p>
      </div>

      <div className="editor-section">
        <h3>Projects</h3>

        {resume.projects.map((project, index) => (
          <div className="editor-item" key={index}>
            <h4>Project {index + 1}</h4>

            <EditorInput
              label="Project Name"
              value={project.name}
              onChange={(value) => updateProject(index, "name", value)}
            />

            <label>Description</label>
            <textarea
              value={project.description}
              onChange={(e) => updateProject(index, "description", e.target.value)}
              rows={4}
            />

            <EditorInput
              label="Technologies"
              value={project.technologies.join(", ")}
              onChange={(value) =>
                updateProject(
                  index,
                  "technologies",
                  value
                    .split(",")
                    .map((technology) => technology.trim())
                    .filter(Boolean)
                )
              }
            />

            <EditorInput
              label="GitHub URL"
              value={project.github_url || ""}
              onChange={(value) => updateProject(index, "github_url", value)}
            />

            <EditorInput
              label="Live URL"
              value={project.live_url || ""}
              onChange={(value) => updateProject(index, "live_url", value)}
            />
          </div>
        ))}
      </div>

      <div className="editor-section">
        <h3>Experience</h3>

        {resume.experience.map((item, index) => (
          <div className="editor-item" key={index}>
            <h4>Experience {index + 1}</h4>

            <EditorInput
              label="Company"
              value={item.company}
              onChange={(value) => updateExperience(index, "company", value)}
            />

            <EditorInput
              label="Role"
              value={item.role}
              onChange={(value) => updateExperience(index, "role", value)}
            />

            <EditorInput
              label="Duration"
              value={item.duration}
              onChange={(value) => updateExperience(index, "duration", value)}
            />

            <label>Description</label>
            <textarea
              value={item.description.join("\n")}
              onChange={(e) =>
                updateExperience(
                  index,
                  "description",
                  e.target.value.split("\n").filter(Boolean)
                )
              }
              rows={5}
            />
          </div>
        ))}
      </div>

      <div className="editor-section">
        <h3>Education</h3>

        {resume.education.map((item, index) => (
          <div className="editor-item" key={index}>
            <h4>Education {index + 1}</h4>

            <EditorInput
              label="Institution"
              value={item.institution}
              onChange={(value) => updateEducation(index, "institution", value)}
            />

            <EditorInput
              label="Degree"
              value={item.degree}
              onChange={(value) => updateEducation(index, "degree", value)}
            />

            <EditorInput
              label="Duration"
              value={item.duration}
              onChange={(value) => updateEducation(index, "duration", value)}
            />

            <EditorInput
              label="Grade"
              value={item.grade || ""}
              onChange={(value) => updateEducation(index, "grade", value)}
            />
          </div>
        ))}
      </div>

      <div className="editor-section">
        <h3>Certifications</h3>
        <textarea
          value={resume.certifications.join("\n")}
          onChange={(e) =>
            onChange({
              ...resume,
              certifications: e.target.value.split("\n").filter(Boolean),
            })
          }
          rows={4}
          placeholder="One certification per line"
        />
      </div>
    </section>
  );
}

function EditorInput({ label, value, onChange }) {
  return (
    <div className="editor-field">
      <label>{label}</label>
      <input value={value} onChange={(e) => onChange(e.target.value)} />
    </div>
  );
}

export default ResumeEditor;