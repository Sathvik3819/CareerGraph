import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function Auth({ onLogin }) {
  const [mode, setMode] = useState("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submit = async () => {
    setError("");

    if (!email || !password) {
      setError("Email and password are required.");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    if (mode === "register" && (!name || name.length < 2)) {
      setError("Name must be at least 2 characters.");
      return;
    }

    try {
      setLoading(true);

      const endpoint = mode === "login" ? "/api/auth/login" : "/api/auth/register";
      const body =
        mode === "login"
          ? { email, password }
          : { name, email, password };

      const response = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        if (Array.isArray(data.detail)) {
          const messages = data.detail.map(err => `${err.loc[err.loc.length - 1]}: ${err.msg}`);
          throw new Error(messages.join(", "));
        }
        throw new Error(typeof data.detail === "string" ? data.detail : "Authentication failed");
      }

      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem(
        "user",
        JSON.stringify({
          user_id: data.user_id,
          name: data.name,
          email: data.email,
        })
      );

      onLogin(data);
    } catch (error) {
      setError(error instanceof Error ? error.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-brand">
          <h1>CareerGraph</h1>
          <p>Build job-tailored resumes with AI agents.</p>
        </div>

        <div className="auth-tabs">
          <button
            className={mode === "login" ? "auth-tab active" : "auth-tab"}
            onClick={() => {
              setMode("login");
              setError("");
            }}
          >
            Login
          </button>

          <button
            className={mode === "register" ? "auth-tab active" : "auth-tab"}
            onClick={() => {
              setMode("register");
              setError("");
            }}
          >
            Register
          </button>
        </div>

        {mode === "register" && (
          <div className="auth-field">
            <label>Name</label>
            <input
              type="text"
              value={name}
              placeholder="Your name"
              onChange={(e) => setName(e.target.value)}
            />
          </div>
        )}

        <div className="auth-field">
          <label>Email</label>
          <input
            type="email"
            value={email}
            placeholder="you@example.com"
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="auth-field">
          <label>Password</label>
          <input
            type="password"
            value={password}
            placeholder="Minimum 8 characters"
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        {error && <div className="auth-error">{error}</div>}

        <button className="auth-submit" onClick={submit} disabled={loading}>
          {loading ? "Please wait..." : mode === "login" ? "Login" : "Create Account"}
        </button>

        <p className="auth-switch">
          {mode === "login" ? "Don't have an account?" : "Already have an account?"}
          <button onClick={() => setMode(mode === "login" ? "register" : "login")}>
            {mode === "login" ? "Create one" : "Login"}
          </button>
        </p>
      </div>
    </div>
  );
}

export default Auth;