import { useMemo, useState } from "react";
import "./index.css";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

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

  const generatedOutputs = results?.outputs || {};
  const availableOutputIds = Object.keys(generatedOutputs);

  const active =
    outputs.find((item) => item.id === activeOutput) ||
    outputs.find((item) =>
      availableOutputIds.includes(item.id)
    ) ||
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

      let data = null;

      try {
        data = await response.json();
      } catch {
        throw new Error(
          "The PRISM backend returned an invalid response."
        );
      }

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
      onWorkspace={() => setPage("workspace")}
      onHistory={() =>
        alert("History will be connected later.")
      }
      onNew={handleNewTransformation}
    />
  );
}

/* =========================================================
   LANDING
========================================================= */

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
            type="button"
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

/* =========================================================
   WORKSPACE
========================================================= */

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
            type="button"
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

/* =========================================================
   RESULTS
========================================================= */

function Results({
  results,
  outputs,
  active,
  activeOutput,
  setActiveOutput,
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

  const renderContentForCopy = () => {
    return serializeContent(activeContent);
  };

  const copyContent = async () => {
    try {
      await navigator.clipboard.writeText(
        renderContentForCopy()
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
        onLogo={onWorkspace}
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
                    onClick={() =>
                      setActiveOutput(output.id)
                    }
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

                <button
                  className="secondary-button"
                  type="button"
                  onClick={() =>
                    alert(
                      "Export will be connected to the rendering assets next."
                    )
                  }
                >
                  Export
                </button>

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
              <OutputRenderer
                outputType={activeOutput}
                content={activeContent}
              />
            </div>

            {/* PROVENANCE / GUARDRAIL */}

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

/* =========================================================
   OUTPUT RENDERER
========================================================= */

function OutputRenderer({
  outputType,
  content,
}) {
  if (
    content === null ||
    content === undefined ||
    content === ""
  ) {
    return (
      <div className="empty-output">
        <strong>No content generated.</strong>
        <span>
          PRISM did not return content for this output.
        </span>
      </div>
    );
  }

  /*
   * Text specialists return strings.
   *
   * ReactMarkdown + remarkGfm renders:
   * - bold
   * - headings
   * - lists
   * - tables
   * - links
   * - blockquotes
   */
  if (typeof content === "string") {
    return (
      <article className="markdown-output">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            a: ({ node, ...props }) => (
              <a
                {...props}
                target="_blank"
                rel="noopener noreferrer"
              />
            ),
          }}
        >
          {content}
        </ReactMarkdown>
      </article>
    );
  }

  /*
   * Structured output rendering.
   */
  switch (outputType) {
    case "presentation":
      return (
        <PresentationRenderer content={content} />
      );

    case "infographic":
      return (
        <InfographicRenderer content={content} />
      );

    case "video":
      return <VideoRenderer content={content} />;

    case "executive_summary":
      return (
        <ExecutiveSummaryRenderer
          content={content}
        />
      );

    default:
      return (
        <article className="markdown-output">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {JSON.stringify(content, null, 2)}
          </ReactMarkdown>
        </article>
      );
  }
}

/* =========================================================
   PRESENTATION
========================================================= */

function PresentationRenderer({ content }) {
  const slides = Array.isArray(content?.slides)
    ? content.slides
    : [];

  return (
    <div className="presentation-preview">
      <div className="presentation-header">
        <div>
          <span className="structured-label">
            PRESENTATION
          </span>

          <h3>{content?.title || "Presentation"}</h3>

          {content?.subtitle && (
            <p>{content.subtitle}</p>
          )}
        </div>

        {content?.audience && (
          <span className="structured-badge">
            {content.audience}
          </span>
        )}
      </div>

      <div className="slide-list">
        {slides.map((slide, index) => (
          <article
            className="presentation-slide"
            key={
              slide.slide_number ??
              `slide-${index}`
            }
          >
            <div className="slide-number">
              {String(
                slide.slide_number ?? index + 1
              ).padStart(2, "0")}
            </div>

            <div className="slide-body">
              <h4>{slide.title}</h4>

              {slide.subtitle && (
                <p className="slide-subtitle">
                  {slide.subtitle}
                </p>
              )}

              {slide.key_stat && (
                <div className="slide-stat">
                  {slide.key_stat}
                </div>
              )}

              <ul>
                {(slide.content || []).map(
                  (point, pointIndex) => (
                    <li key={pointIndex}>
                      {point}
                    </li>
                  )
                )}
              </ul>

              {slide.speaker_notes && (
                <details className="speaker-notes">
                  <summary>
                    Speaker notes
                  </summary>

                  <p>{slide.speaker_notes}</p>
                </details>
              )}

              {slide.source_references?.length > 0 && (
                <div className="source-references">
                  Source:{" "}
                  {slide.source_references.join(", ")}
                </div>
              )}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}

/* =========================================================
   INFOGRAPHIC
========================================================= */

function InfographicRenderer({ content }) {
  const metrics = Array.isArray(
    content?.headline_metrics
  )
    ? content.headline_metrics
    : [];

  const timeline = Array.isArray(content?.timeline)
    ? content.timeline
    : [];

  const sections = Array.isArray(content?.sections)
    ? content.sections
    : [];

  return (
    <div className="infographic-preview">
      <div className="infographic-header">
        <span className="structured-label">
          INFOGRAPHIC
        </span>

        <h3>{content?.title || "Infographic"}</h3>

        {content?.subtitle && (
          <p>{content.subtitle}</p>
        )}
      </div>

      {metrics.length > 0 && (
        <section className="metric-grid">
          {metrics.map((metric, index) => (
            <article
              className="metric-card"
              key={`${metric.label}-${index}`}
            >
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>

              {metric.explanation && (
                <small>
                  {metric.explanation}
                </small>
              )}
            </article>
          ))}
        </section>
      )}

      {timeline.length > 0 && (
        <section className="timeline-section">
          <div className="structured-section-heading">
            <span>Timeline</span>
          </div>

          <div className="timeline">
            {timeline.map((item, index) => (
              <div
                className="timeline-item"
                key={`${item.time}-${index}`}
              >
                <div className="timeline-marker">
                  {index + 1}
                </div>

                <div>
                  <strong>{item.time}</strong>
                  <p>{item.event}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="infographic-sections">
        {sections.map((section, index) => (
          <article
            className="info-section"
            key={`${section.heading}-${index}`}
          >
            <h4>{section.heading}</h4>

            <ul>
              {(section.key_points || []).map(
                (point, pointIndex) => (
                  <li key={pointIndex}>
                    {point}
                  </li>
                )
              )}
            </ul>
          </article>
        ))}
      </section>

      {content?.footer_note && (
        <div className="infographic-footer">
          {content.footer_note}
        </div>
      )}
    </div>
  );
}

/* =========================================================
   VIDEO
========================================================= */

function VideoRenderer({ content }) {
  const scenes = Array.isArray(content?.scenes)
    ? content.scenes
    : [];

  const totalDuration = Number(
    content?.total_duration_seconds || 0
  );

  const totalMinutes = Math.floor(totalDuration / 60);
  const totalSeconds = totalDuration % 60;

  const formattedDuration =
    totalMinutes > 0
      ? `${String(totalMinutes).padStart(2, "0")}:${String(
          totalSeconds
        ).padStart(2, "0")}`
      : `00:${String(totalSeconds).padStart(2, "0")}`;

  return (
    <div className="video-production-preview">

      {/* =====================================================
          VIDEO HEADER
      ===================================================== */}

      <div className="video-production-header">
        <div className="video-title-block">
          <div className="video-kicker">
            <span className="video-live-dot" />
            AI VIDEO STORYBOARD
          </div>

          <h3>
            {content?.title || "Untitled Video"}
          </h3>

          {content?.description && (
            <p>{content.description}</p>
          )}
        </div>

        <div className="video-duration-card">
          <span>Total duration</span>
          <strong>{formattedDuration}</strong>
          <small>
            {scenes.length} scenes
          </small>
        </div>
      </div>

      {/* =====================================================
          STORYBOARD TIMELINE
      ===================================================== */}

      <div className="video-timeline">
        {scenes.map((scene, index) => (
          <div
            className="video-timeline-item"
            key={
              scene.scene_number ??
              `scene-${index}`
            }
          >
            <div
              className={`video-timeline-node ${
                index === 0 ? "active" : ""
              }`}
            >
              {String(
                scene.scene_number ??
                  index + 1
              ).padStart(2, "0")}
            </div>

            {index < scenes.length - 1 && (
              <div className="video-timeline-line" />
            )}
          </div>
        ))}
      </div>

      {/* =====================================================
          SCENES
      ===================================================== */}

      <div className="video-scenes">

        {scenes.map((scene, index) => {
          const sceneNumber =
            scene.scene_number ?? index + 1;

          const duration =
            Number(scene.duration_seconds) || 0;

          return (
            <article
              className="video-production-scene"
              key={sceneNumber}
            >

              {/* ---------------------------------------------
                  SCENE TOP
              --------------------------------------------- */}

              <div className="video-scene-header">

                <div className="video-scene-number">
                  <span>
                    SCENE
                  </span>

                  <strong>
                    {String(sceneNumber).padStart(
                      2,
                      "0"
                    )}
                  </strong>
                </div>

                <div className="video-scene-heading">
                  <h4>
                    {scene.title}
                  </h4>

                  <span>
                    Production sequence · Scene{" "}
                    {sceneNumber}
                  </span>
                </div>

                <div className="video-scene-duration">
                  <span>Duration</span>
                  <strong>
                    {String(
                      Math.floor(duration / 60)
                    ).padStart(2, "0")}
                    :
                    {String(
                      duration % 60
                    ).padStart(2, "0")}
                  </strong>
                </div>

              </div>

              {/* ---------------------------------------------
                  VISUAL PREVIEW + CORE INFORMATION
              --------------------------------------------- */}

              <div className="video-scene-main">

                <div className="video-visual-frame">

                  <div className="video-frame-grid" />

                  <div className="video-frame-content">

                    <div className="video-frame-play">
                      ▶
                    </div>

                    <span>
                      SCENE {String(
                        sceneNumber
                      ).padStart(2, "0")}
                    </span>

                    <strong>
                      {scene.on_screen_text ||
                        scene.title}
                    </strong>

                  </div>

                  <div className="video-frame-footer">
                    <span>
                      PRISM VISUAL PREVIEW
                    </span>

                    <span>
                      {duration}s
                    </span>
                  </div>
                </div>

                <div className="video-scene-information">

                  {/* ON SCREEN TEXT */}

                  {scene.on_screen_text && (
                    <div className="video-info-block featured">
                      <div className="video-info-label">
                        <span>01</span>
                        ON-SCREEN TEXT
                      </div>

                      <div className="video-onscreen-text">
                        {scene.on_screen_text}
                      </div>
                    </div>
                  )}

                  {/* NARRATION */}

                  {scene.narration && (
                    <div className="video-info-block">
                      <div className="video-info-label">
                        <span>02</span>
                        NARRATION
                      </div>

                      <p className="video-narration">
                        {scene.narration}
                      </p>
                    </div>
                  )}

                </div>
              </div>

              {/* ---------------------------------------------
                  PRODUCTION DETAILS
              --------------------------------------------- */}

              <div className="video-production-details">

                <VideoProductionDetail
                  number="03"
                  label="Visual direction"
                  value={scene.video_prompt}
                />

                <VideoProductionDetail
                  number="04"
                  label="Character"
                  value={scene.character_description}
                />

                <VideoProductionDetail
                  number="05"
                  label="Environment"
                  value={scene.environment}
                />

                <VideoProductionDetail
                  number="06"
                  label="Camera"
                  value={scene.camera_direction}
                />

                <VideoProductionDetail
                  number="07"
                  label="Action"
                  value={scene.action}
                />

                <VideoProductionDetail
                  number="08"
                  label="Negative prompt"
                  value={scene.negative_prompt}
                />

              </div>

              {/* ---------------------------------------------
                  SOURCE
              --------------------------------------------- */}

              {scene.source_references?.length > 0 && (
                <div className="video-source-row">
                  <span>
                    SOURCE REFERENCE
                  </span>

                  <div>
                    {scene.source_references.map(
                      (reference) => (
                        <span
                          key={reference}
                          className="video-source-chip"
                        >
                          {reference}
                        </span>
                      )
                    )}
                  </div>
                </div>
              )}

            </article>
          );
        })}

      </div>

      {/* =====================================================
          PRODUCTION FOOTER
      ===================================================== */}

      <div className="video-production-footer">

        <div>
          <span className="video-footer-icon">
            ✓
          </span>

          <div>
            <strong>
              Storyboard ready
            </strong>

            <small>
              All scenes are grounded in the
              verified Fact Graph.
            </small>
          </div>
        </div>

        <span className="video-footer-status">
          {scenes.length} scenes ·{" "}
          {formattedDuration}
        </span>

      </div>
    </div>
  );
}
function VideoProductionDetail({
  number,
  label,
  value,
}) {
  if (!value) {
    return null;
  }

  return (
    <div className="video-production-detail">

      <div className="video-detail-label">
        <span>{number}</span>
        {label}
      </div>

      <p>{value}</p>

    </div>
  );
}

function SceneField({ label, value }) {
  if (!value) {
    return null;
  }

  return (
    <div className="scene-field">
      <span>{label}</span>
      <p>{value}</p>
    </div>
  );
}

/* =========================================================
   EXECUTIVE SUMMARY
========================================================= */

function ExecutiveSummaryRenderer({
  content,
}) {
  const findings = Array.isArray(
    content?.key_findings
  )
    ? content.key_findings
    : [];

  const response = Array.isArray(
    content?.response
  )
    ? content.response
    : [];

  const recommendations = Array.isArray(
    content?.recommendations
  )
    ? content.recommendations
    : [];

  return (
    <div className="executive-summary-preview">
      <div className="executive-header">
        <span className="structured-label">
          EXECUTIVE SUMMARY
        </span>

        <h3>
          {content?.title ||
            "Executive Summary"}
        </h3>
      </div>

      {content?.overview && (
        <section className="executive-section overview">
          <span>Overview</span>
          <p>{content.overview}</p>
        </section>
      )}

      {findings.length > 0 && (
        <ExecutiveListSection
          title="Key findings"
          items={findings}
        />
      )}

      {content?.impact && (
        <section className="executive-section">
          <span>Impact</span>
          <p>{content.impact}</p>
        </section>
      )}

      {response.length > 0 && (
        <ExecutiveListSection
          title="Response"
          items={response}
        />
      )}

      {recommendations.length > 0 && (
        <ExecutiveListSection
          title="Recommendations"
          items={recommendations}
        />
      )}

      {content?.source_references?.length > 0 && (
        <div className="source-references">
          Source:{" "}
          {content.source_references.join(", ")}
        </div>
      )}
    </div>
  );
}

function ExecutiveListSection({
  title,
  items,
}) {
  return (
    <section className="executive-section">
      <span>{title}</span>

      <ul>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </section>
  );
}

/* =========================================================
   CONTENT SERIALIZATION
========================================================= */

function serializeContent(content) {
  if (
    content === null ||
    content === undefined
  ) {
    return "";
  }

  if (typeof content === "string") {
    return content;
  }

  return JSON.stringify(content, null, 2);
}

/* =========================================================
   HELPERS
========================================================= */

function formatDuration(seconds) {
  const value = Number(seconds);

  if (!Number.isFinite(value)) {
    return "";
  }

  const minutes = Math.floor(value / 60);
  const remainingSeconds = value % 60;

  if (minutes === 0) {
    return `${remainingSeconds}s`;
  }

  return `${minutes}m ${remainingSeconds}s`;
}

/* =========================================================
   HEADER
========================================================= */

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