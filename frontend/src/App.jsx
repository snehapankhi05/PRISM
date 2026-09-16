import { useState } from "react";
import "./index.css";

const API_URL = "http://127.0.0.1:8000";

const outputs = [
  {
    id: "linkedin",
    name: "LinkedIn Post",
    icon: "in",
    type: "text",
  },
  {
    id: "twitter",
    name: "Twitter / X",
    icon: "𝕏",
    type: "text",
  },
  {
    id: "advisory",
    name: "Advisory",
    icon: "!",
    type: "text",
  },
  {
    id: "executive_summary",
    name: "Executive Summary",
    icon: "≡",
    type: "text",
  },
  {
    id: "infographic",
    name: "Infographic",
    icon: "▦",
    type: "visual",
  },
  {
    id: "presentation",
    name: "Presentation",
    icon: "▤",
    type: "visual",
  },
  {
    id: "video",
    name: "Video",
    icon: "▶",
    type: "visual",
  },
];

const defaultControls = {
  targetAudience: "General public",
  tone: "Professional",
  language: "English",
  detailLevel: "Concise",
  objective: "Inform the audience",
  contentStyle: "Clear and factual",
};

function App() {
  const [page, setPage] = useState("landing");

  const [source, setSource] = useState("");
  const [sourceTitle, setSourceTitle] = useState("");

  const [controls, setControls] = useState(defaultControls);

  const [selectedOutputs, setSelectedOutputs] = useState([
    "linkedin",
  ]);

  const [results, setResults] = useState(null);
  const [activeOutput, setActiveOutput] = useState("linkedin");
  const [isGenerating, setIsGenerating] = useState(false);
  const [activeSlide, setActiveSlide] = useState(0);

  const generatedOutputs = results?.outputs || {};

  const availableOutputIds = Object.keys(generatedOutputs);

  const active =
    outputs.find((item) => item.id === activeOutput) ||
    outputs.find((item) => availableOutputIds.includes(item.id)) ||
    outputs[0];

  const handleGenerate = async () => {
    if (!source.trim()) {
      alert("Please enter source content first.");
      return;
    }

    if (selectedOutputs.length === 0) {
      alert("Please select at least one output.");
      return;
    }

    setIsGenerating(true);

    try {
      const response = await fetch(`${API_URL}/transform`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: source,
          title: sourceTitle.trim() || "Untitled Transformation",

          controls: {
            target_audience: controls.targetAudience,
            tone: controls.tone,
            language: controls.language,
            level_of_detail: controls.detailLevel,
            communication_objective: controls.objective,
            content_style: controls.contentStyle,
          },

          output_types: selectedOutputs,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.detail || "Transformation failed."
        );
      }

      setResults(data);

      const firstGeneratedOutput =
        Object.keys(data.outputs || {})[0];

      if (firstGeneratedOutput) {
        setActiveOutput(firstGeneratedOutput);
        setActiveSlide(0);
      }

      setPage("results");
    } catch (error) {
      console.error("PRISM transformation error:", error);

      alert(
        error?.message ||
          "Unable to connect to the PRISM backend."
      );
    } finally {
      setIsGenerating(false);
    }
  };

  const handleNewTransformation = () => {
    setSource("");
    setSourceTitle("");
    setControls(defaultControls);
    setSelectedOutputs(["linkedin"]);
    setResults(null);
    setActiveOutput("linkedin");
    setPage("workspace");
  };

  if (page === "landing") {
    return (
      <Landing
        onStart={() => setPage("workspace")}
      />
    );
  }

  if (page === "workspace") {
    return (
      <Workspace
        source={source}
        setSource={setSource}
        sourceTitle={sourceTitle}
        setSourceTitle={setSourceTitle}
        controls={controls}
        setControls={setControls}
        selectedOutputs={selectedOutputs}
        setSelectedOutputs={setSelectedOutputs}
        isGenerating={isGenerating}
        onGenerate={handleGenerate}
        onResults={() => {
          if (results) {
            setPage("results");
          }
        }}
        onLanding={() => setPage("landing")}
      />
    );
  }

  return (
    <Results
      results={results}
      outputs={outputs}
      active={active}
      activeOutput={activeOutput}
      setActiveOutput={setActiveOutput}
      activeSlide={activeSlide}
      setActiveSlide={setActiveSlide}
      onWorkspace={() => setPage("workspace")}
      onHistory={() =>
        alert("History will be connected later.")
      }
      onNew={handleNewTransformation}
    />
  );
}

/* =========================
   LANDING
========================= */

function Landing({ onStart }) {
  return (
    <div className="landing-page">
      <header className="landing-topbar">
        <div className="brand">
          <div className="brand-mark">P</div>

          <div>
            <div className="brand-name">PRISM</div>

            <div className="brand-subtitle">
              Intelligent Content Synthesis
            </div>
          </div>
        </div>

        <div className="topbar-status">
          <span className="status-dot" />
          System Ready
        </div>
      </header>

      <main className="landing-main">
        <section className="landing-hero">
          <div className="eyebrow">
            CONTENT INTELLIGENCE PLATFORM
          </div>

          <h1>
            Understand once.
            <br />
            <span>Generate everywhere.</span>
          </h1>

          <p>
            Transform a single source of truth into consistent,
            provenance-backed communication across every channel.
          </p>

          <button
            className="primary-button"
            onClick={onStart}
          >
            Create New Transformation
            <span>→</span>
          </button>
        </section>

        <section className="landing-pipeline">
          <div className="preview-header">
            <div>
              <span className="preview-label">
                PRISM WORKSPACE
              </span>

              <h2>Content Transformation</h2>
            </div>

            <div className="preview-badge">
              FACT GRAPH READY
            </div>
          </div>

          <div className="pipeline">
            {[
              ["01", "Source", "Upload or provide content"],
              ["02", "Understand", "Build verified facts"],
              ["03", "Generate", "Create all channels"],
              ["04", "Verify", "Check consistency"],
            ].map((item, index) => (
              <div
                className="pipeline-wrapper"
                key={item[0]}
              >
                <div className="pipeline-item">
                  <div className="pipeline-number">
                    {item[0]}
                  </div>

                  <div>
                    <h3>{item[1]}</h3>
                    <p>{item[2]}</p>
                  </div>
                </div>

                {index < 3 && (
                  <div className="pipeline-line" />
                )}
              </div>
            ))}
          </div>
        </section>
      </main>

      <footer className="landing-footer">
        <span>PRISM</span>
        <span>
          Provenance-Reasoned Intelligent Synthesis
        </span>
      </footer>
    </div>
  );
}

/* =========================
   WORKSPACE
========================= */

function Workspace({
  source,
  setSource,
  sourceTitle,
  setSourceTitle,
  controls,
  setControls,
  selectedOutputs,
  setSelectedOutputs,
  isGenerating,
  onGenerate,
  onResults,
  onLanding,
}) {
  const toggleOutput = (id) => {
    setSelectedOutputs((current) =>
      current.includes(id)
        ? current.filter((item) => item !== id)
        : [...current, id]
    );
  };

  const updateControl = (key, value) => {
    setControls((current) => ({
      ...current,
      [key]: value,
    }));
  };

  return (
    <div className="workspace-app">
      <AppHeader
        active="workspace"
        onWorkspace={() => {}}
        onResults={onResults}
        onHistory={() =>
          alert("History will be connected later.")
        }
        onLogo={onLanding}
      />

      <main className="workspace-main">
        <div className="workspace-heading">
          <div>
            <div className="eyebrow">
              NEW TRANSFORMATION
            </div>

            <h1>Turn one source into many.</h1>

            <p>
              PRISM understands your source once, builds a
              verified fact graph, then generates consistent
              content across channels.
            </p>
          </div>

          <div className="fact-indicator">
            <span className="fact-icon">◆</span>

            <div>
              <strong>Single Source of Truth</strong>
              <small>Fact Graph powered</small>
            </div>
          </div>
        </div>

        <div className="workspace-grid">
          {/* SOURCE */}

          <section className="workspace-card source-card">
            <div className="card-heading">
              <div>
                <span className="step-label">
                  01 · SOURCE
                </span>

                <h2>What should PRISM understand?</h2>
              </div>

              <button
                className="small-button"
                type="button"
                onClick={() =>
                  alert(
                    "File upload will be connected next. TXT · PDF · DOCX are supported by the backend."
                  )
                }
              >
                Upload file
              </button>
            </div>

            <input
              className="source-title-input"
              type="text"
              value={sourceTitle}
              onChange={(e) =>
                setSourceTitle(e.target.value)
              }
              placeholder="Source title (optional)"
            />

            <textarea
              value={source}
              onChange={(e) => setSource(e.target.value)}
              placeholder="Paste an article, report, advisory, incident report, research paper or any source content here..."
            />

            <div className="source-footer">
              <span>{source.length} characters</span>

              <span className="supported">
                TXT · PDF · DOCX
              </span>
            </div>
          </section>

          {/* CONTROLS */}

          <section className="workspace-card controls-card">
            <div className="card-heading">
              <div>
                <span className="step-label">
                  02 · CONTROLS
                </span>

                <h2>Shape the communication</h2>
              </div>
            </div>

            <div className="control-row">
              <label>Target audience</label>

              <select
                className="control-select"
                value={controls.targetAudience}
                onChange={(e) =>
                  updateControl(
                    "targetAudience",
                    e.target.value
                  )
                }
              >
                <option>General public</option>
                <option>General audience</option>
                <option>Customers</option>
                <option>Executives</option>
                <option>Employees</option>
                <option>Technical audience</option>
              </select>
            </div>

            <div className="control-row">
              <label>Tone</label>

              <select
                className="control-select"
                value={controls.tone}
                onChange={(e) =>
                  updateControl("tone", e.target.value)
                }
              >
                <option>Professional</option>
                <option>Formal</option>
                <option>Friendly</option>
                <option>Technical</option>
                <option>Persuasive</option>
              </select>
            </div>

            <div className="control-row">
              <label>Language</label>

              <select
                className="control-select"
                value={controls.language}
                onChange={(e) =>
                  updateControl(
                    "language",
                    e.target.value
                  )
                }
              >
                <option>English</option>
              </select>
            </div>

            <div className="control-row">
              <label>Level of detail</label>

              <select
                className="control-select"
                value={controls.detailLevel}
                onChange={(e) =>
                  updateControl(
                    "detailLevel",
                    e.target.value
                  )
                }
              >
                <option>Concise</option>
                <option>Balanced</option>
                <option>Detailed</option>
              </select>
            </div>

            <div className="control-row">
              <label>Communication objective</label>

              <select
                className="control-select"
                value={controls.objective}
                onChange={(e) =>
                  updateControl(
                    "objective",
                    e.target.value
                  )
                }
              >
                <option>Inform the audience</option>
                <option>Inform</option>
                <option>Persuade the audience</option>
                <option>Provide guidance</option>
                <option>Support decision making</option>
              </select>
            </div>

            <div className="control-row">
              <label>Content style</label>

              <select
                className="control-select"
                value={controls.contentStyle}
                onChange={(e) =>
                  updateControl(
                    "contentStyle",
                    e.target.value
                  )
                }
              >
                <option>Clear and factual</option>
                <option>Clear & concise</option>
                <option>Technical</option>
                <option>Executive</option>
                <option>Conversational</option>
              </select>
            </div>
          </section>
        </div>

        {/* OUTPUT SELECTION */}

        <section className="outputs-section">
          <div className="outputs-heading">
            <div>
              <span className="step-label">
                03 · OUTPUTS
              </span>

              <h2>Where should the content go?</h2>
            </div>

            <span className="selection-count">
              {selectedOutputs.length} of {outputs.length}{" "}
              selected
            </span>
          </div>

          <div className="output-grid">
            {outputs.map((output) => {
              const selected = selectedOutputs.includes(
                output.id
              );

              return (
                <button
                  key={output.id}
                  type="button"
                  className={`output-option ${
                    selected ? "selected" : ""
                  }`}
                  onClick={() =>
                    toggleOutput(output.id)
                  }
                >
                  <span className="output-icon">
                    {output.icon}
                  </span>

                  <span className="output-info">
                    <strong>{output.name}</strong>

                    <small>
                      {selected
                        ? "Included"
                        : "Not selected"}
                    </small>
                  </span>

                  <span className="checkbox">
                    {selected ? "✓" : ""}
                  </span>
                </button>
              );
            })}
          </div>
        </section>

        {/* GENERATE */}

        <section className="generation-bar">
          <div>
            <span className="generation-status">
              <span className="status-dot" />

              {isGenerating
                ? "PRISM is transforming..."
                : "Ready to transform"}
            </span>

            <p>
              {selectedOutputs.length} output type
              {selectedOutputs.length === 1 ? "" : "s"}{" "}
              will use the same verified fact graph.
            </p>
          </div>

          <button
            className="generate-button"
            disabled={
              isGenerating ||
              !source.trim() ||
              selectedOutputs.length === 0
            }
            onClick={onGenerate}
          >
            {isGenerating
              ? "Generating..."
              : "Generate with PRISM"}

            {!isGenerating && <span>→</span>}
          </button>
        </section>
      </main>
    </div>
  );
}

/* =========================
   RESULTS
========================= */

function Results({
  results,
  outputs,
  active,
  activeOutput,
  setActiveOutput,
  activeSlide,
  setActiveSlide,
  onWorkspace,
  onHistory,
  onNew,
}) {
  const generatedOutputs = results?.outputs || {};
  const generatedIds = Object.keys(generatedOutputs);

  const activeData = generatedOutputs[activeOutput];

  const activeContent = activeData?.content;

  const guardrail =
    results?.guardrails?.[activeOutput];

  const presentationUrl =
    results?.job_id && activeOutput === "presentation"
      ? `${API_URL}/outputs/${results.job_id}/presentation/presentation.pptx`
      : null;

  const renderContent = () => {
    if (activeContent === null || activeContent === undefined) {
      return "No content generated.";
    }

    if (typeof activeContent === "string") {
      return activeContent;
    }

    return JSON.stringify(activeContent, null, 2);
  };

  const copyContent = async () => {
    try {
      await navigator.clipboard.writeText(
        renderContent()
      );

      alert("Content copied.");
    } catch (error) {
      console.error("Copy failed:", error);
      alert("Unable to copy content.");
    }
  };

  return (
    <div className="results-app">
      <AppHeader
        active="results"
        onWorkspace={onWorkspace}
        onResults={() => {}}
        onHistory={onHistory}
      />

      <main className="results-main">
        <section className="results-heading">
          <div>
            <span className="eyebrow">
              TRANSFORMATION COMPLETE
            </span>

            <h1>Your content, everywhere.</h1>

            <p>
              Every output was generated from the same
              verified Fact Graph.
            </p>
          </div>

          <div className="verification-card">
            <div className="verification-icon">
              ✓
            </div>

            <div>
              <strong>Consistency checked</strong>

              <small>
                Source-backed generation
              </small>
            </div>
          </div>
        </section>

        <section className="results-layout">
          {/* SIDEBAR */}

          <aside className="output-sidebar">
            <div className="sidebar-title">
              <span>GENERATED OUTPUTS</span>

              <strong>{generatedIds.length}</strong>
            </div>

            {outputs
              .filter((output) =>
                generatedIds.includes(output.id)
              )
              .map((output) => {
                const outputGuardrail =
                  results?.guardrails?.[output.id];

                const passed =
                  outputGuardrail?.passed !== false;

                return (
                  <button
                    key={output.id}
                    type="button"
                    className={`result-item ${
                      activeOutput === output.id
                        ? "active"
                        : ""
                    }`}
                    onClick={() => {
                      setActiveOutput(output.id);
                      setActiveSlide(0);
                    }}
                  >
                    <span className="result-icon">
                      {output.icon}
                    </span>

                    <span className="result-name">
                      <strong>{output.name}</strong>

                      <small>
                        <span className="result-check">
                          {passed ? "✓" : "!"}
                        </span>{" "}
                        {passed
                          ? "Verified"
                          : "Review"}
                      </small>
                    </span>

                    <span className="result-arrow">
                      ›
                    </span>
                  </button>
                );
              })}
          </aside>

          {/* VIEWER */}

          <section className="output-viewer">
            <div className="viewer-header">
              <div>
                <span className="viewer-label">
                  GENERATED OUTPUT
                </span>

                <h2>{active.name}</h2>
              </div>

              <div className="viewer-actions">
                <button
                  className="secondary-button"
                  onClick={copyContent}
                  type="button"
                >
                  Copy
                </button>

                {presentationUrl ? (
                  <a
                    className="secondary-button"
                    href={presentationUrl}
                    target="_blank"
                    rel="noreferrer"
                    download="presentation.pptx"
                    style={{ textDecoration: "none" }}
                  >
                    Open / Download PPT
                  </a>
                ) : (
                  <button
                    className="secondary-button"
                    type="button"
                    onClick={copyContent}
                  >
                    Export
                  </button>
                )}

                <button
                  className="post-button"
                  disabled
                  type="button"
                >
                  Post
                  <span>Coming soon</span>
                </button>
              </div>
            </div>

            <div
              className={`content-preview ${active.type}`}
            >
              {activeOutput === "presentation" ? (
                (() => {
                  const slides = Array.isArray(activeContent?.slides)
                    ? activeContent.slides
                    : [];

                  if (slides.length === 0) {
                    return (
                      <div
                        className="visual-placeholder"
                        style={{ gap: "12px" }}
                      >
                        <span>{active.icon}</span>
                        <strong>{active.name}</strong>
                        <small>
                          Presentation generated successfully.
                        </small>
                        {presentationUrl && (
                          <a
                            className="primary-button"
                            href={presentationUrl}
                            target="_blank"
                            rel="noreferrer"
                            download="presentation.pptx"
                            style={{
                              textDecoration: "none",
                              marginTop: "8px",
                            }}
                          >
                            Open / Download PowerPoint →
                          </a>
                        )}
                      </div>
                    );
                  }

                  const slideIndex = Math.min(
                    activeSlide,
                    slides.length - 1
                  );
                  const slide = slides[slideIndex];

                  return (
                    <div
                      style={{
                        width: "100%",
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        gap: "18px",
                      }}
                    >
                      {/* PPT SLIDE PREVIEW */}
                      <div
                        style={{
                          width: "min(900px, 100%)",
                          aspectRatio: "16 / 9",
                          background: "#ffffff",
                          border: "1px solid #dfe4ef",
                          borderRadius: "16px",
                          boxShadow:
                            "0 18px 50px rgba(20, 30, 60, 0.12)",
                          padding: "42px 52px",
                          boxSizing: "border-box",
                          display: "flex",
                          flexDirection: "column",
                          justifyContent: "space-between",
                          overflow: "hidden",
                          textAlign: "left",
                        }}
                      >
                        <div>
                          <div
                            style={{
                              fontSize: "11px",
                              fontWeight: 700,
                              letterSpacing: "0.16em",
                              textTransform: "uppercase",
                              color: "#63708a",
                              marginBottom: "18px",
                            }}
                          >
                            PRISM · PRESENTATION
                          </div>

                          <h3
                            style={{
                              margin: 0,
                              fontSize: "clamp(28px, 4vw, 48px)",
                              lineHeight: 1.08,
                              color: "#121a2b",
                            }}
                          >
                            {slide.title}
                          </h3>

                          {slide.subtitle && (
                            <p
                              style={{
                                margin: "12px 0 0",
                                fontSize: "18px",
                                lineHeight: 1.4,
                                color: "#63708a",
                              }}
                            >
                              {slide.subtitle}
                            </p>
                          )}
                        </div>

                        <div
                          style={{
                            display: "flex",
                            flexDirection: "column",
                            gap: "14px",
                          }}
                        >
                          {(slide.content || []).map(
                            (item, index) => (
                              <div
                                key={index}
                                style={{
                                  display: "flex",
                                  gap: "12px",
                                  alignItems: "flex-start",
                                  color: "#273149",
                                  fontSize: "17px",
                                  lineHeight: 1.4,
                                }}
                              >
                                <span
                                  style={{
                                    flex: "0 0 auto",
                                    width: "8px",
                                    height: "8px",
                                    borderRadius: "50%",
                                    background: "#5267ff",
                                    marginTop: "8px",
                                  }}
                                />
                                <span>{item}</span>
                              </div>
                            )
                          )}

                          {slide.key_stat && (
                            <div
                              style={{
                                marginTop: "8px",
                                padding: "12px 16px",
                                borderRadius: "10px",
                                background: "#f3f5ff",
                                fontWeight: 700,
                                color: "#2638c9",
                              }}
                            >
                              {slide.key_stat}
                            </div>
                          )}
                        </div>

                        <div
                          style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            borderTop: "1px solid #e7eaf1",
                            paddingTop: "12px",
                            fontSize: "11px",
                            color: "#7a8498",
                          }}
                        >
                          <span>
                            {activeContent.title || "PRISM"}
                          </span>

                          <span>
                            Slide {slideIndex + 1} / {slides.length}
                          </span>
                        </div>
                      </div>

                      {/* SLIDE NAVIGATION */}
                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          gap: "12px",
                          flexWrap: "wrap",
                        }}
                      >
                        <button
                          className="secondary-button"
                          type="button"
                          disabled={slideIndex === 0}
                          onClick={() =>
                            setActiveSlide((current) =>
                              Math.max(current - 1, 0)
                            )
                          }
                        >
                          ← Previous
                        </button>

                        <span
                          style={{
                            minWidth: "100px",
                            textAlign: "center",
                            fontSize: "14px",
                            color: "#63708a",
                          }}
                        >
                          Slide {slideIndex + 1} of {slides.length}
                        </span>

                        <button
                          className="secondary-button"
                          type="button"
                          disabled={
                            slideIndex === slides.length - 1
                          }
                          onClick={() =>
                            setActiveSlide((current) =>
                              Math.min(
                                current + 1,
                                slides.length - 1
                              )
                            )
                          }
                        >
                          Next →
                        </button>
                      </div>

                      {presentationUrl && (
                        <a
                          className="primary-button"
                          href={presentationUrl}
                          target="_blank"
                          rel="noreferrer"
                          download="presentation.pptx"
                          style={{ textDecoration: "none" }}
                        >
                          Open / Download PowerPoint →
                        </a>
                      )}
                    </div>
                  );
                })()
              ) : active.type === "visual" ? (
                <div className="visual-placeholder">
                  <span>{active.icon}</span>
                  <strong>{active.name}</strong>
                  <small>Rendered asset preview</small>
                </div>
              ) : (
                <pre
                  style={{
                    whiteSpace: "pre-wrap",
                    fontFamily: "inherit",
                    margin: 0,
                  }}
                >
                  {renderContent()}
                </pre>
              )}
            </div>

            {/* GUARDRAIL */}

            <div className="provenance-panel">
              <div className="provenance-title">
                <span className="provenance-icon">
                  ◇
                </span>

                <div>
                  <strong>Provenance</strong>

                  <small>
                    Where this content came from
                  </small>
                </div>
              </div>

              <div className="provenance-source">
                <span>Source</span>

                <strong>
                  Original document · Fact Graph
                </strong>

                <em>
                  {guardrail?.passed === false
                    ? "Review required"
                    : "Checked"}
                </em>
              </div>

              {guardrail &&
                guardrail.issues?.length > 0 && (
                  <div
                    className="guardrail-issues"
                    style={{ marginTop: "16px" }}
                  >
                    <strong>
                      Guardrail findings
                    </strong>

                    {guardrail.issues.map(
                      (issue, index) => (
                        <div
                          key={`${issue.issue_type}-${index}`}
                          style={{
                            marginTop: "8px",
                          }}
                        >
                          <small>
                            <strong>
                              {issue.severity.toUpperCase()}
                            </strong>{" "}
                            — {issue.message}
                          </small>
                        </div>
                      )
                    )}
                  </div>
                )}
            </div>
          </section>
        </section>

        {/* FOOTER */}

        <section className="results-footer-bar">
          <div>
            <span className="status-dot" />

            <strong>
              {generatedIds.length} output
              {generatedIds.length === 1
                ? ""
                : "s"}{" "}
              generated
            </strong>

            <small>
              All outputs share the same verified source
              facts.
            </small>
          </div>

          <button
            className="new-transformation"
            onClick={onNew}
            type="button"
          >
            ← New transformation
          </button>
        </section>
      </main>
    </div>
  );
}

/* =========================
   HEADER
========================= */

function AppHeader({
  active,
  onWorkspace,
  onResults,
  onHistory,
  onLogo,
}) {
  return (
    <header className="workspace-topbar">
      <button
        className="brand brand-button"
        onClick={onLogo}
        type="button"
      >
        <div className="brand-mark">P</div>

        <div>
          <div className="brand-name">PRISM</div>

          <div className="brand-subtitle">
            Intelligent Content Synthesis
          </div>
        </div>
      </button>

      <div className="workspace-nav">
        <button
          className={
            active === "workspace"
              ? "nav-active"
              : ""
          }
          onClick={onWorkspace}
          type="button"
        >
          Workspace
        </button>

        <button
          className={
            active === "results"
              ? "nav-active"
              : ""
          }
          onClick={onResults}
          type="button"
        >
          Results
        </button>

        <button
          onClick={onHistory}
          type="button"
        >
          History
        </button>
      </div>

      <div className="topbar-status">
        <span className="status-dot" />
        System Ready
      </div>
    </header>
  );
}

export default App;