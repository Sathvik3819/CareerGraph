import { useState } from "react";
import "./App.css";
import Auth from "./components/Auth";
import ResumePreview from "./components/ResumePreview";
import ReviewPanel from "./components/ReviewPanel";
import ATSPanel from "./components/ATSPanel";
import TemplateSelector from "./components/TemplateSelector";
import AgentProgress from "./components/AgentProgress";
import ResumeHistory from "./components/ResumeHistory";
import Dashboard from "./components/Dashboard";
import ResumeEditor from "./components/ResumeEditor";
import { apiFetch, API_URL } from "./utils/api";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    Boolean(localStorage.getItem("access_token"))
  );

  const [currentUser, setCurrentUser] = useState(() => {
    const stored = localStorage.getItem("user");
    return stored ? JSON.parse(stored) : null;
  });

  const [personal, setPersonal] = useState({
    name: "",
    email: "",
    phone: "",
    location: "",
    github: "",
    linkedin: "",
    portfolio: "",
  });

  const [education, setEducation] = useState([
    {
      institution: "",
      degree: "",
      duration: "",
      grade: "",
    },
  ]);

  const [skills, setSkills] = useState([]);
  const [skillInput, setSkillInput] = useState("");

  const [projects, setProjects] = useState([
    {
      name: "",
      description: "",
      technologies: "",
      githubUrl: "",
      liveUrl: "",
    },
  ]);

  const [experience, setExperience] = useState([
    {
      company: "",
      role: "",
      duration: "",
      description: "",
    },
  ]);

  const [certifications, setCertifications] = useState([]);
  const [certificationInput, setCertificationInput] = useState("");

  const [jobRole, setJobRole] = useState("");
  const [jobDescription, setJobDescription] = useState("");

  const initialAgentSteps = [
    { id: "analyze_profile", label: "Profile Analyzer", status: "pending" },
    { id: "analyze_job", label: "JD Analyzer", status: "pending" },
    { id: "create_resume", label: "Resume Creator", status: "pending" },
    { id: "review_resume", label: "Resume Reviewer", status: "pending" },
    { id: "analyze_ats", label: "ATS Analyzer", status: "pending" },
    { id: "generate_pdf", label: "PDF Generator", status: "pending" },
  ];

  const [loading, setLoading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState(null);
  const [originalResume, setOriginalResume] = useState(null);
  const [editedResume, setEditedResume] = useState(null);
  const [selectedTemplate, setSelectedTemplate] = useState("modern");
  const [historyRefreshKey, setHistoryRefreshKey] = useState(0);
  const [error, setError] = useState("");
  const [agentSteps, setAgentSteps] = useState(initialAgentSteps);
  const [showDashboard, setShowDashboard] = useState(true);

  const handleLogin = (data) => {
    setIsAuthenticated(true);
    setCurrentUser({
      user_id: data.user_id,
      name: data.name,
      email: data.email,
    });
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    setIsAuthenticated(false);
    setCurrentUser(null);
  };

  const handleCreateResume = () => {
    setShowDashboard(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const updatePersonal = (field, value) => {
    setPersonal((previous) => ({
      ...previous,
      [field]: value,
    }));
  };

  const addEducation = () => {
    setEducation([
      ...education,
      { institution: "", degree: "", duration: "", grade: "" },
    ]);
  };

  const removeEducation = (index) => {
    setEducation((current) => current.filter((_, i) => i !== index));
  };

  const updateEducation = (index, field, value) => {
    const updated = [...education];
    updated[index][field] = value;
    setEducation(updated);
  };

  const addSkill = () => {
    const skill = skillInput.trim();
    if (!skill) return;
    if (!skills.includes(skill)) {
      setSkills([...skills, skill]);
    }
    setSkillInput("");
  };

  const removeSkill = (skillToRemove) => {
    setSkills((current) => current.filter((skill) => skill !== skillToRemove));
  };

  const addProject = () => {
    setProjects([
      ...projects,
      { name: "", description: "", technologies: "", githubUrl: "", liveUrl: "" },
    ]);
  };

  const removeProject = (index) => {
    setProjects((current) => current.filter((_, i) => i !== index));
  };

  const updateProject = (index, field, value) => {
    const updated = [...projects];
    updated[index][field] = value;
    setProjects(updated);
  };

  const addExperience = () => {
    setExperience([
      ...experience,
      { company: "", role: "", duration: "", description: "" },
    ]);
  };

  const removeExperience = (index) => {
    setExperience((current) => current.filter((_, i) => i !== index));
  };

  const updateExperience = (index, field, value) => {
    const updated = [...experience];
    updated[index][field] = value;
    setExperience(updated);
  };

  const addCertification = () => {
    const certification = certificationInput.trim();
    if (!certification) return;
    setCertifications([...certifications, certification]);
    setCertificationInput("");
  };

  const removeCertification = (certificationToRemove) => {
    setCertifications((current) =>
      current.filter((certification) => certification !== certificationToRemove)
    );
  };

  const generateResumeWithStream = async () => {
    setLoading(true);
    setIsGenerating(true);
    setError("");
    setResult(null);
    setOriginalResume(null);
    setEditedResume(null);
    setAgentSteps(
      initialAgentSteps.map((step) => ({ ...step, status: "pending" }))
    );

    try {
      const response = await apiFetch("/api/resume/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          personal: {
            name: personal.name,
            email: personal.email || null,
            phone: personal.phone || null,
            location: personal.location || null,
            github: personal.github || null,
            linkedin: personal.linkedin || null,
            portfolio: personal.portfolio || null,
          },
          education: education.map((item) => ({
            institution: item.institution,
            degree: item.degree,
            duration: item.duration,
            grade: item.grade || null,
          })),
          skills,
          projects: projects.map((project) => ({
            name: project.name,
            description: project.description,
            technologies: project.technologies
              .split(",")
              .map((technology) => technology.trim())
              .filter(Boolean),
            github_url: project.githubUrl || null,
            live_url: project.liveUrl || null,
          })),
          experience: experience.map((item) => ({
            company: item.company,
            role: item.role,
            duration: item.duration,
            description: item.description,
          })),
          certifications,
          job_role: jobRole,
          job_description: jobDescription,
          template: selectedTemplate,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to start resume generation");
      }

      if (!response.body) {
        throw new Error("Streaming is not supported");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const events = buffer.split("\n\n");
        buffer = events.pop() || "";

        for (const event of events) {
          if (!event.startsWith("data:")) continue;

          const jsonString = event.replace(/^data:\s*/, "").trim();
          const eventData = JSON.parse(jsonString);

          if (eventData.type === "node_started") {
            setAgentSteps((previous) =>
              previous.map((step) =>
                step.id === eventData.node ? { ...step, status: "running" } : step
              )
            );
          }

          if (eventData.type === "node_completed") {
            setAgentSteps((previous) =>
              previous.map((step) =>
                step.id === eventData.node ? { ...step, status: "completed" } : step
              )
            );
          }

          if (eventData.type === "completed") {
            const finalState = eventData.result;
            const generatedResult = {
              status: finalState.status || "completed",
              iterations: finalState.iteration || 0,
              resume: finalState.resume,
              review: finalState.review,
              ats_analysis: finalState.ats_analysis,
              pdf_path: finalState.pdf_path || null,
            };

            const clonedResume = structuredClone(finalState.resume);
            setResult(generatedResult);
            setOriginalResume(clonedResume);
            setEditedResume(clonedResume);
            setHistoryRefreshKey((previous) => previous + 1);
            setAgentSteps((previous) =>
              previous.map((step) => ({ ...step, status: "completed" }))
            );
            setIsGenerating(false);
          }

          if (eventData.type === "error") {
            throw new Error(eventData.message);
          }
        }
      }
    } catch (error) {
      console.error("Resume generation failed:", error);
      setAgentSteps((previous) =>
        previous.map((step) =>
          step.status === "running" ? { ...step, status: "error" } : step
        )
      );
      setIsGenerating(false);
      alert(error instanceof Error ? error.message : "Resume generation failed.");
    } finally {
      setLoading(false);
      setIsGenerating(false);
    }
  };

  const formData = {
    personal,
    education,
    skills,
    projects,
    experience,
    certifications,
    jobRole,
    jobDescription,
  };

  const loadResumeFromHistory = async (resumeId) => {
    try {
      const response = await apiFetch(`/api/resume/${resumeId}`);
      if (!response.ok) throw new Error("Failed to load resume");

      const data = await response.json();
      const saved = data.candidate_data || {};

      setPersonal({
        name: saved.personal?.name || "",
        email: saved.personal?.email || "",
        phone: saved.personal?.phone || "",
        location: saved.personal?.location || "",
        github: saved.personal?.github || "",
        linkedin: saved.personal?.linkedin || "",
        portfolio: saved.personal?.portfolio || "",
      });

      setEducation(
        (saved.education || []).map((item) => ({
          institution: item.institution || "",
          degree: item.degree || "",
          duration: item.duration || "",
          grade: item.grade || "",
        }))
      );

      setSkills(saved.skills || []);
      setProjects(
        (saved.projects || []).map((project) => ({
          name: project.name || "",
          description: project.description || "",
          technologies: Array.isArray(project.technologies)
            ? project.technologies.join(", ")
            : project.technologies || "",
          githubUrl: project.github_url || "",
          liveUrl: project.live_url || "",
        }))
      );

      setExperience(
        (saved.experience || []).map((item) => ({
          company: item.company || "",
          role: item.role || "",
          duration: item.duration || "",
          description: item.description || "",
        }))
      );

      setCertifications(saved.certifications || []);
      setJobRole(saved.job_role || "");
      setJobDescription(saved.job_description || "");
      setSelectedTemplate(data.template || selectedTemplate);

      setResult({
        status: "completed",
        iterations: data.iterations,
        resume: data.resume,
        review: data.review,
        ats_analysis: data.ats_analysis,
        pdf_path: null,
      });

      const loadedResume = structuredClone(data.resume);
      setOriginalResume(loadedResume);
      setEditedResume(loadedResume);

      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (error) {
      console.error("Failed to load saved resume:", error);
      alert("Unable to load the selected resume.");
    }
  };

  const downloadPDF = async () => {
    if (!editedResume) return;

    try {
      const response = await fetch(`${API_URL}/api/resume/pdf`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token") || ""}`,
        },
        body: JSON.stringify({
          resume: editedResume,
          template: selectedTemplate,
        }),
      });

      if (!response.ok) throw new Error("Failed to generate PDF");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      const safeJobRole = jobRole
        .trim()
        .replace(/[^a-zA-Z0-9]+/g, "_")
        .replace(/^_|_$/g, "");

      link.href = url;
      link.download = `careergraph_${safeJobRole || "resume"}_${selectedTemplate}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("PDF generation failed:", error);
      alert("Failed to generate PDF. Please try again.");
    }
  };

  if (!isAuthenticated) {
    return <Auth onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      <header className="navbar">
        <div className="logo">
          Career<span>Graph</span>
        </div>

        <div className="user-area">
          <button
            className="dashboard-nav-btn"
            onClick={() => {
              setShowDashboard(true);
              window.scrollTo({ top: 0, behavior: "smooth" });
            }}
          >
            Dashboard
          </button>

          <button className="dashboard-nav-btn" onClick={handleCreateResume}>
            Create Resume
          </button>

          <div className="user-info">
            <strong>{currentUser?.name}</strong>
            <span>{currentUser?.email}</span>
          </div>

          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <main className="container">
        {showDashboard && (
          <Dashboard
            userName={currentUser?.name || "there"}
            onCreateResume={handleCreateResume}
            onSelectResume={loadResumeFromHistory}
          />
        )}

        {!showDashboard && (
          <div className="hero">
            <h1>Build a resume that matches your target job.</h1>
            <p>
              Give CareerGraph your profile and target job. Our AI agents analyze,
              create, review and improve your resume.
            </p>
          </div>
        )}

        <div className="builder-layout">
          <div className="builder-form">
            <section className="form-card">
              <h2>Personal Information</h2>
              <div className="input-grid">
                <input
                  placeholder="Full Name"
                  value={personal.name}
                  onChange={(e) => updatePersonal("name", e.target.value)}
                />
                <input
                  placeholder="Email"
                  value={personal.email}
                  onChange={(e) => updatePersonal("email", e.target.value)}
                />
                <input
                  placeholder="Phone"
                  value={personal.phone}
                  onChange={(e) => updatePersonal("phone", e.target.value)}
                />
                <input
                  placeholder="Location"
                  value={personal.location}
                  onChange={(e) => updatePersonal("location", e.target.value)}
                />
                <input
                  placeholder="GitHub URL"
                  value={personal.github}
                  onChange={(e) => updatePersonal("github", e.target.value)}
                />
                <input
                  placeholder="LinkedIn URL"
                  value={personal.linkedin}
                  onChange={(e) => updatePersonal("linkedin", e.target.value)}
                />
                <input
                  placeholder="Portfolio URL"
                  value={personal.portfolio}
                  onChange={(e) => updatePersonal("portfolio", e.target.value)}
                />
              </div>
            </section>

            <section className="form-card">
              <div className="section-header">
                <div>
                  <h2>Education</h2>
                  <p>Add your academic background.</p>
                </div>
                <button className="secondary-button" onClick={addEducation}>
                  + Add Education
                </button>
              </div>

              {education.map((item, index) => (
                <div className="repeat-card" key={index}>
                  <div className="input-grid">
                    <input
                      placeholder="Institution"
                      value={item.institution}
                      onChange={(e) =>
                        updateEducation(index, "institution", e.target.value)
                      }
                    />
                    <input
                      placeholder="Degree"
                      value={item.degree}
                      onChange={(e) =>
                        updateEducation(index, "degree", e.target.value)
                      }
                    />
                    <input
                      placeholder="Duration"
                      value={item.duration}
                      onChange={(e) =>
                        updateEducation(index, "duration", e.target.value)
                      }
                    />
                    <input
                      placeholder="CGPA / Grade"
                      value={item.grade}
                      onChange={(e) =>
                        updateEducation(index, "grade", e.target.value)
                      }
                    />
                  </div>

                  {education.length > 1 && (
                    <button className="remove-button" onClick={() => removeEducation(index)}>
                      Remove
                    </button>
                  )}
                </div>
              ))}
            </section>

            <section className="form-card">
              <h2>Skills</h2>

              <div className="skill-input">
                <input
                  placeholder="Enter a skill"
                  value={skillInput}
                  onChange={(e) => setSkillInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      addSkill();
                    }
                  }}
                />
                <button className="secondary-button" onClick={addSkill}>
                  Add
                </button>
              </div>

              <div className="chips">
                {skills.map((skill) => (
                  <div className="chip" key={skill}>
                    {skill}
                    <button onClick={() => removeSkill(skill)}>×</button>
                  </div>
                ))}
              </div>
            </section>

            <section className="form-card">
              <div className="section-header">
                <div>
                  <h2>Projects</h2>
                  <p>Add projects that demonstrate your technical skills.</p>
                </div>
                <button className="secondary-button" onClick={addProject}>
                  + Add Project
                </button>
              </div>

              {projects.map((project, index) => (
                <div className="repeat-card" key={index}>
                  <input
                    placeholder="Project Name"
                    value={project.name}
                    onChange={(e) => updateProject(index, "name", e.target.value)}
                  />
                  <textarea
                    placeholder="Describe your project..."
                    value={project.description}
                    onChange={(e) =>
                      updateProject(index, "description", e.target.value)
                    }
                  />
                  <input
                    placeholder="Technologies (React, Node.js, MongoDB...)"
                    value={project.technologies}
                    onChange={(e) =>
                      updateProject(index, "technologies", e.target.value)
                    }
                  />
                  <div className="input-grid">
                    <input
                      placeholder="GitHub URL"
                      value={project.githubUrl}
                      onChange={(e) =>
                        updateProject(index, "githubUrl", e.target.value)
                      }
                    />
                    <input
                      placeholder="Live URL"
                      value={project.liveUrl}
                      onChange={(e) =>
                        updateProject(index, "liveUrl", e.target.value)
                      }
                    />
                  </div>

                  {projects.length > 1 && (
                    <button className="remove-button" onClick={() => removeProject(index)}>
                      Remove Project
                    </button>
                  )}
                </div>
              ))}
            </section>

            <section className="form-card">
              <div className="section-header">
                <div>
                  <h2>Experience</h2>
                  <p>Add internships, jobs or relevant professional experience.</p>
                </div>
                <button className="secondary-button" onClick={addExperience}>
                  + Add Experience
                </button>
              </div>

              {experience.map((item, index) => (
                <div className="repeat-card" key={index}>
                  <div className="input-grid">
                    <input
                      placeholder="Company"
                      value={item.company}
                      onChange={(e) => updateExperience(index, "company", e.target.value)}
                    />
                    <input
                      placeholder="Role"
                      value={item.role}
                      onChange={(e) => updateExperience(index, "role", e.target.value)}
                    />
                    <input
                      placeholder="Duration"
                      value={item.duration}
                      onChange={(e) =>
                        updateExperience(index, "duration", e.target.value)
                      }
                    />
                  </div>

                  <textarea
                    placeholder="Describe your responsibilities and achievements..."
                    value={item.description}
                    onChange={(e) =>
                      updateExperience(index, "description", e.target.value)
                    }
                  />

                  {experience.length > 1 && (
                    <button className="remove-button" onClick={() => removeExperience(index)}>
                      Remove Experience
                    </button>
                  )}
                </div>
              ))}
            </section>

            <section className="form-card">
              <h2>Certifications</h2>

              <div className="skill-input">
                <input
                  placeholder="Certification name"
                  value={certificationInput}
                  onChange={(e) => setCertificationInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      addCertification();
                    }
                  }}
                />
                <button className="secondary-button" onClick={addCertification}>
                  Add
                </button>
              </div>

              <div className="chips">
                {certifications.map((certification) => (
                  <div className="chip" key={certification}>
                    {certification}
                    <button onClick={() => removeCertification(certification)}>×</button>
                  </div>
                ))}
              </div>
            </section>

            <section className="form-card">
              <h2>Target Job</h2>
              <input
                placeholder="Target Job Role — e.g. GenAI Engineer"
                value={jobRole}
                onChange={(e) => setJobRole(e.target.value)}
              />
              <textarea
                placeholder="Paste the complete job description here..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
              />
            </section>

            <section className="generate-section">
              <button
                className="generate-button"
                disabled={loading || !personal.name || !jobRole || !jobDescription}
                onClick={generateResumeWithStream}
              >
                {loading ? "CareerGraph is working..." : "Generate Tailored Resume"}
              </button>
            </section>

            {error && <div className="error-box">{error}</div>}

            {result && (
              <section className="form-card">
                <h2>Resume Generated</h2>
                <p>
                  Status: <strong>{result.status}</strong>
                </p>
                <p>
                  Attempts: <strong>{result.iterations}</strong>
                </p>
                <hr />
                <h2>{result.resume.header.name}</h2>
                <p>{result.resume.summary}</p>
                <h3>Skills</h3>
                <p>{result.resume.skills.join(", ")}</p>
                <h3>Projects</h3>
                {result.resume.projects.map((project, index) => (
                  <div key={index}>
                    <strong>{project.name}</strong>
                    <p>{project.description}</p>
                  </div>
                ))}
              </section>
            )}
          </div>

          <div className="preview-container">
            <AgentProgress steps={agentSteps} isGenerating={isGenerating} />
            <div className="preview-title">Live Preview</div>
            <TemplateSelector
              selectedTemplate={selectedTemplate}
              onChange={setSelectedTemplate}
            />
            {editedResume && (
              <ResumeEditor
                resume={editedResume}
                originalResume={originalResume}
                onChange={setEditedResume}
              />
            )}
            <ResumePreview
              data={formData}
              generatedResume={editedResume}
              hasGeneratedResume={!!editedResume}
              template={selectedTemplate}
              onDownloadPDF={downloadPDF}
            />
            <ReviewPanel review={result?.review} iterations={result?.iterations} />
            <ATSPanel analysis={result?.ats_analysis} />
          </div>
        </div>

        <ResumeHistory refreshKey={historyRefreshKey} onSelectResume={loadResumeFromHistory} />
      </main>
    </div>
  );
}

export default App;