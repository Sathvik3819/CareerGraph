const templates = [
  { id: "modern", name: "Modern", description: "Clean and contemporary" },
  { id: "classic", name: "Classic", description: "Traditional professional" },
  { id: "minimal", name: "Minimal", description: "Simple and ATS-friendly" },
];

function TemplateSelector({ selectedTemplate, onChange }) {
  return (
    <div className="template-selector">
      <div className="template-selector-header">
        <h3>Resume Template</h3>
        <span>Choose a style</span>
      </div>

      <div className="template-options">
        {templates.map((template) => (
          <button
            key={template.id}
            type="button"
            className={`template-option ${selectedTemplate === template.id ? "selected" : ""}`}
            onClick={() => onChange(template.id)}
          >
            <div className="template-thumbnail">
              <div className="thumbnail-header" />
              <div className="thumbnail-line" />
              <div className="thumbnail-line short" />
              <div className="thumbnail-section" />
              <div className="thumbnail-line" />
              <div className="thumbnail-line short" />
            </div>

            <div className="template-info">
              <strong>{template.name}</strong>
              <span>{template.description}</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

export default TemplateSelector;