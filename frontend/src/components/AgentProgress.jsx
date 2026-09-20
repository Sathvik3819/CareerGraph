const getStatusText = (status) => {
  switch (status) {
    case "running":
      return "Running...";
    case "completed":
      return "Completed";
    case "error":
      return "Failed";
    default:
      return "Waiting";
  }
};

function AgentProgress({ steps, isGenerating }) {
  if (!isGenerating && !steps.some((step) => step.status === "completed")) {
    return null;
  }

  return (
    <div className="agent-progress">
      <div className="agent-progress-header">
        <div>
          <h3>CareerGraph Agent Workflow</h3>
          <p>AI agents are analyzing and optimizing your resume.</p>
        </div>
      </div>

      <div className="agent-steps">
        {steps.map((step, index) => (
          <div className={`agent-step ${step.status}`} key={step.id}>
            <div className="agent-step-indicator">
              {step.status === "completed" && <span>✓</span>}
              {step.status === "running" && <span className="agent-spinner" />}
              {step.status === "pending" && <span>{index + 1}</span>}
              {step.status === "error" && <span>!</span>}
            </div>

            <div className="agent-step-content">
              <strong>{step.label}</strong>
              <span>{getStatusText(step.status)}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AgentProgress;