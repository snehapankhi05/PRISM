````markdown
# PRISM — GenAI Content Transformation Platform

PRISM is a production-oriented GenAI content transformation platform that converts a single authoritative source into multiple communication formats while maintaining factual consistency across every generated output.

The core idea is:

> **Understand Once → Generate Many**

Instead of asking an LLM to independently generate every format from the original text, PRISM first builds a structured understanding of the source and then uses that shared knowledge to generate channel-specific outputs.

---

## ✨ Key Features

- **Single-source content transformation**
- **Fact Graph** for structured and traceable information
- **Retrieval-Augmented Generation (RAG)**
- **Local embeddings** for source retrieval
- **ChromaDB** vector storage
- **LangGraph** orchestration
- **Groq LLM** integration
- **Multiple specialized output generators**
- **Source-grounded generation**
- **Guardrails and factual validation**
- **Bounded revision workflow**
- **PowerPoint presentation generation**
- **PowerPoint slide preview directly in the frontend**
- **PowerPoint open/download support**
- **Infographic generation**
- **Video scene/manifest generation**
- **Executive summaries**
- **LinkedIn and Twitter/X content**
- **Security advisory generation**
- **PostgreSQL persistence**
- **FastAPI backend**
- **React + Vite + Tailwind frontend**
- **Automated test suite**

---

## 🧠 Architecture

```text
                    ┌──────────────────────┐
                    │      User Source     │
                    │ Text / Uploaded File  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Ingestion       │
                    │   Normalization      │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
       ┌─────────────────┐          ┌─────────────────┐
       │    Fact Graph   │          │       RAG       │
       │ Structured Facts│          │ Chroma + Local  │
       │ Entities        │          │ Embeddings      │
       │ Relationships   │          │                 │
       └────────┬────────┘          └────────┬────────┘
                │                            │
                └─────────────┬──────────────┘
                              ▼
                    ┌──────────────────────┐
                    │  Knowledge Context   │
                    │ Facts + Evidence     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      LangGraph       │
                    │    Orchestration      │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
       ┌──────────┐      ┌──────────┐      ┌──────────┐
       │ LinkedIn │      │ Twitter  │      │ Advisory │
       └──────────┘      └──────────┘      └──────────┘
             │                 │                 │
             ├─────────────────┼─────────────────┤
             ▼                 ▼                 ▼
       ┌──────────────┐ ┌─────────────┐ ┌─────────────┐
       │ Executive    │ │Presentation │ │ Infographic │
       │ Summary      │ │   (PPTX)    │ │    (PNG)    │
       └──────────────┘ └─────────────┘ └─────────────┘
                               │
                               ▼
                         ┌───────────┐
                         │   Video   │
                         │  Scenes   │
                         └───────────┘

                               │
                               ▼
                    ┌──────────────────────┐
                    │      Guardrails      │
                    │ Provenance / Factual │
                    │ LLM Critic / Revision│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Rendering & Storage  │
                    │ PostgreSQL / Outputs │
                    └──────────────────────┘
````

---

## 🔄 Transformation Pipeline

PRISM follows a deterministic multi-stage pipeline:

### 1. Ingestion

The system accepts authoritative source content and normalizes it into a consistent internal document representation.

### 2. Fact Graph Extraction

The source is analyzed to extract structured facts including:

* Facts
* Entities
* Relationships
* Numbers
* Dates
* Source references
* Confidence information

This creates a structured representation of the source rather than relying only on raw text.

### 3. RAG Indexing

The normalized source is converted into embeddings and indexed in ChromaDB.

PRISM uses local embeddings for retrieval so the source can be searched semantically without requiring a paid embedding API.

### 4. Knowledge Context

The Fact Graph and retrieved evidence are combined into a shared knowledge context.

This context is passed to the generation layer.

### 5. LangGraph Orchestration

LangGraph coordinates the transformation workflow and routes the shared knowledge to the required specialists.

### 6. Specialist Generation

Each output type has its own specialist responsible for its communication format.

Supported outputs:

```text
linkedin
twitter
advisory
executive_summary
presentation
infographic
video
```

### 7. Guardrails

Generated outputs pass through validation layers designed to identify:

* Unsupported claims
* Incorrect numbers
* Incorrect dates
* Missing source support
* Factual inconsistencies

A bounded revision process can revise problematic outputs using the available evidence.

### 8. Rendering

Validated outputs are converted into their final formats.

Examples:

```text
LinkedIn       → TXT
Twitter/X      → TXT
Advisory       → TXT
Executive      → TXT
Presentation   → PPTX
Infographic    → PNG
Video          → Manifest + Scenes
```

---

# 🛠️ Tech Stack

## Frontend

* React
* Vite
* Tailwind CSS
* JavaScript

## Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy

## AI / LLM

* Groq
* LangGraph
* Local embedding models

## RAG

* ChromaDB
* Sentence Transformers
* Local embeddings

## Database

* PostgreSQL

## Document Generation

* python-pptx
* PNG rendering for infographics
* Structured video scene generation

## Testing

* Pytest

## Development

* Git
* Docker
* Docker Compose

---

# 📁 Project Structure

```text
PRISM/
│
├── backend/
│   └── app/
│       ├── api/
│       │   ├── health.py
│       │   ├── router.py
│       │   └── transform.py
│       │
│       ├── core/
│       │   └── config.py
│       │
│       ├── db/
│       │   ├── dependencies.py
│       │   └── session.py
│       │
│       ├── models/
│       │
│       ├── schemas/
│       │
│       └── services/
│           ├── ingestion/
│           ├── llm/
│           ├── fact_graph/
│           ├── rag/
│           ├── knowledge/
│           ├── orchestration/
│           │   ├── graph.py
│           │   ├── generation.py
│           │   ├── guardrails.py
│           │   ├── rendering.py
│           │   ├── runtime.py
│           │   └── specialists/
│           │
│           ├── guardrails/
│           │
│           └── rendering/
│               ├── infographic/
│               ├── presentation/
│               └── video/
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── ...
│
├── data/
│   ├── chroma/
│   ├── outputs/
│   └── test_ppt/
│
├── tests/
│
├── docs/
│
├── scripts/
│
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

# ⚙️ Requirements

Make sure the following are installed:

* Python 3.11+
* Node.js
* npm
* Git
* Docker Desktop
* PostgreSQL / Docker PostgreSQL

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/snehapankhi05/PRISM.git
cd PRISM
```

---

## 2. Create Python virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install backend dependencies

```powershell
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file according to the project's configuration.

Example:

```env
LLM_API_KEY=your_groq_api_key
LLM_MODEL=your_configured_groq_model

DATABASE_URL=postgresql+psycopg://prism:your_password@localhost:5432/prism
```

Do not commit `.env` or API keys to GitHub.

---

# 🐘 Start PostgreSQL

If using Docker Compose:

```powershell
docker compose up -d
```

Check running containers:

```powershell
docker ps
```

The PostgreSQL service should be available on:

```text
localhost:5432
```

---

# ▶️ Run the Backend

From the project root:

```powershell
uvicorn backend.app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# ❤️ Health Check

Test the backend:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected response:

```text
status   service
------   -------
healthy  prism-api
```

---

# 🎨 Run the Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

The Vite development server will normally run at:

```text
http://localhost:5173
```

---

# 🔌 API

## Health

```http
GET /health
```

Used to verify that the PRISM backend is running.

---

## Transform

```http
POST /transform
```

The transformation endpoint accepts source content, generation controls, and requested output types.

Example request:

```json
{
  "content": "PRISM is a GenAI content transformation platform.",
  "title": "PRISM Overview",
  "controls": {
    "target_audience": "General audience",
    "tone": "Professional",
    "language": "English",
    "level_of_detail": "Concise",
    "communication_objective": "Inform",
    "content_style": "Professional"
  },
  "output_types": [
    "linkedin",
    "twitter",
    "advisory",
    "executive_summary",
    "presentation",
    "infographic",
    "video"
  ]
}
```

---

# 📊 PowerPoint Generation

PRISM can generate a PowerPoint presentation from the same verified knowledge context used by the other output specialists.

The presentation pipeline produces:

```text
presentation.pptx
```

Generated files are stored under:

```text
data/outputs/
```

The frontend provides:

* Presentation preview
* Slide navigation
* Slide count
* Open PowerPoint
* Download PowerPoint

The browser preview uses the structured presentation content, while the generated `.pptx` remains available as the actual PowerPoint file.

---

# 🖼️ Infographic Generation

The infographic specialist produces a rendered image:

```text
infographic.png
```

Output location:

```text
data/outputs/<job_id>/infographic/
```

---

# 🎬 Video Output

The current video pipeline generates a structured video manifest and scene files.

Example:

```text
video/
├── video_manifest.txt
└── scenes/
    ├── scene_1.txt
    ├── scene_2.txt
    ├── scene_3.txt
    └── ...
```

This provides the structured content required for a presentation-style video workflow.

---

# 🧪 Testing

Run the complete test suite:

```powershell
pytest -q
```

Example successful result:

```text
15 passed
```

Run the orchestration presentation-generation test specifically:

```powershell
pytest tests\test_orchestration_graph.py::test_prism_generates_multiple_outputs -q
```

---

# 🔍 Verify Registered Outputs

To verify that all output renderers are registered:

```powershell
python -c "from backend.app.services.rendering.registry import create_default_registry; r=create_default_registry(); print(r.supported_outputs())"
```

Expected output:

```text
[
    'linkedin',
    'twitter',
    'advisory',
    'executive_summary',
    'presentation',
    'infographic',
    'video'
]
```

---

# 📦 Generated Output Example

A successful transformation can produce:

```text
data/
└── outputs/
    └── <job_id>/
        ├── linkedin/
        │   └── linkedin.txt
        │
        ├── twitter/
        │   └── twitter.txt
        │
        ├── advisory/
        │   └── advisory.txt
        │
        ├── executive_summary/
        │   └── executive_summary.txt
        │
        ├── presentation/
        │   └── presentation.pptx
        │
        ├── infographic/
        │   └── infographic.png
        │
        └── video/
            ├── video_manifest.txt
            └── scenes/
                ├── scene_1.txt
                ├── scene_2.txt
                └── ...
```

---

# 🛡️ Source Grounding

A core design principle of PRISM is that generated outputs should be grounded in the source material.

The system separates:

```text
Source
   ↓
Facts
   ↓
Evidence
   ↓
Knowledge Context
   ↓
Generation
   ↓
Validation
   ↓
Rendering
```

This allows the same underlying information to be reused across different communication formats rather than independently regenerated for every channel.

---

# 🧩 Specialist Architecture

PRISM uses independent specialists for each output format.

```text
SpecialistAgent
      │
      ├── LinkedInSpecialist
      ├── TwitterSpecialist
      ├── AdvisorySpecialist
      ├── ExecutiveSummarySpecialist
      ├── PresentationSpecialist
      ├── InfographicSpecialist
      └── VideoSpecialist
```

Specialists receive a shared `KnowledgeContext` and generation controls.

This keeps channel-specific formatting separate from the core source-understanding pipeline.

---

# 🔐 Guardrail Architecture

PRISM includes multiple validation layers:

```text
Generated Output
       │
       ▼
Provenance Validation
       │
       ▼
Basic Guardrail
       │
       ▼
Factual Guardrail
       │
       ▼
LLM Critic
       │
       ▼
Bounded Revision
       │
       ▼
Final Output
```

The purpose is to identify unsupported or inconsistent information before the output reaches the rendering stage.

---

# 🎯 Design Principles

### Understand Once, Generate Many

The source is interpreted once and reused across output formats.

### Source First

Generated content should originate from the supplied source and retrieved evidence.

### Separation of Responsibilities

Ingestion, knowledge construction, generation, validation, and rendering are separate stages.

### Specialized Generation

Each communication channel has its own specialist rather than relying on one generic prompt.

### Deterministic Orchestration

The workflow is explicitly orchestrated through LangGraph rather than relying on an uncontrolled sequence of LLM calls.

### Renderable Outputs

The system produces actual usable artifacts such as:

* `.pptx`
* `.png`
* `.txt`
* structured scene manifests

---

# 🖥️ Frontend Workflow

The intended user workflow is:

```text
Open PRISM
    ↓
Enter or provide source content
    ↓
Configure generation controls
    ↓
Select output formats
    ↓
Generate
    ↓
PRISM processes the source
    ↓
Fact Graph + RAG
    ↓
Specialists generate outputs
    ↓
Guardrails validate outputs
    ↓
Rendered results appear in frontend
    ↓
Preview / Open / Download
```

For presentations:

```text
Source
  ↓
Presentation Specialist
  ↓
Structured Presentation Content
  ↓
PPTX Renderer
  ↓
presentation.pptx
  ↓
Frontend
  ├── Slide Preview
  ├── Previous / Next
  ├── Open PPT
  └── Download PPT
```

---

# 🧪 Current Validation

The project includes automated tests covering the core orchestration workflow.

Current test verification includes:

```text
pytest -q

15 passed
```

The presentation renderer and output registration are also verified through the project's existing rendering and orchestration tests.

---

# 🔮 Future Improvements

Potential future extensions include:

* More input file formats
* PDF/DOCX ingestion
* Richer PowerPoint templates
* Editable presentation themes
* More advanced infographic layouts
* Actual video rendering
* Authentication and user accounts
* Background job processing
* Production object storage
* Advanced observability
* More comprehensive evaluation datasets
* Additional communication channels

---

# 📌 Project Status

PRISM is an end-to-end GenAI content transformation platform with a working backend transformation pipeline, structured knowledge layer, multi-output generation architecture, guardrails, rendering system, and frontend presentation workflow.

The architecture is designed to support further productionization without changing the fundamental:

```text
UNDERSTAND ONCE
       ↓
GENERATE MANY
       ↓
VALIDATE
       ↓
RENDER
```

---

## 👩‍💻 Author

**Sneha Pankhi**

Computer Engineering — AI/ML

GitHub:
[https://github.com/snehapankhi05](https://github.com/snehapankhi05)

---

## 📄 License

This project is intended for educational, development, and portfolio purposes unless a separate license is added to the repository.
