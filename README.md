<<<<<<< HEAD
# Nevara

Nevara is an experimental local agentic system for interactive assistance and autonomous system repair. It combines a conversational agent, document retrieval, and a background system-monitoring agent to help users work with local documents and to reason about system health using journal logs.

This repository is split into two main parts:

- `nevara/` — the Python backend built on LangChain, LangGraph, FastAPI, and FAISS.
- `nevara-cli/` — a Rust command-line client that connects to the local API and streams agent responses.

## What it does

- Chat with a local conversational agent powered by Ollama models.
- Search the web through DuckDuckGo when the answer is not already known.
- Retrieve content from uploaded files using a vector store.
- Monitor system logs (`journalctl`) and decide whether a repair action is warranted.
- Expose the agent via a streaming FastAPI endpoint for interactive use.
- Offer a Rust-based CLI to interact with the agent in a terminal.

## Architecture

```text
+---------------------------+
| nevara-cli (Rust)        |
| - interactive terminal    |
| - SSE streaming UI        |
+------------+--------------+
             |
             | HTTP / SSE
             v
+---------------------------+
| FastAPI app               |
| nevara/src/nevara/server.py|
| - /invoke                 |
| - /invoke_v2             |
| - /upload                |
| - /remove_upload         |
+------------+--------------+
             |
             v
+---------------------------+
| Agent orchestration       |
| nevara/src/Agents          |
| - ConvAgent               |
| - SystemAgent             |
| - tool routing / state    |
+------------+--------------+
             |
             v
+---------------------------+
| Retrieval / knowledge     |
| - FAISS vector store      |
| - document loaders        |
| - uploaded file support   |
+---------------------------+
```

## Repository layout

```text
.
├── README.md
├── nevara/
│   ├── README.md
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── .python-version
│   └── src/
│       ├── Agents/
│       │   ├── ConvAgent/
│       │   └── SystemAgent/
│       ├── DocRetriever/
│       ├── Loader/
│       └── nevara/
│           ├── __init__.py
│           ├── globalOp.py
│           └── server.py
└── nevara-cli/
    ├── Cargo.toml
    ├── Cargo.lock
    └── src/
        ├── components.rs
        ├── main.rs
        ├── schema.rs
        └── figlet.txt
```

## Core components

### Python backend (`nevara/`)

The Python service is built around a LangChain + LangGraph agent stack:

- `nevara/src/Agents/ConvAgent/`
  - conversational frontend agent
  - uses `ChatOllama`
  - binds tools such as document retrieval and web search
- `nevara/src/Agents/SystemAgent/`
  - system-monitoring agent
  - reads `journalctl` logs
  - decides whether a repair workflow is appropriate
- `nevara/src/DocRetriever/`
  - loads files from `./res`
  - creates a FAISS vector database for document retrieval
- `nevara/src/nevara/server.py`
  - FastAPI app exposing streaming and upload endpoints

### Rust CLI (`nevara-cli/`)

The Rust client talks to `http://localhost:8000` and supports:

- interactive user input
- slash commands such as `/list_files`, `/upload_file`, and `/remove_file`
- streaming SSE responses from the agent
- a simple terminal UI with colored output and a logo

## Requirements

Before running the project, install:

- Python 3.12+
- `uv` (recommended) or `pip`
- Rust and Cargo
- Ollama with local models available:
  - `qwen3.5:2b` (used by the conversation agent in `ConvAgent/model.py`)
  - `mxbai-embed-large` (used by the retriever embeddings in `DocRetriever/__init__.py`)

The project is designed to run locally; it expects Ollama to be running on the machine.

## Quick start

### 1) Start the Python backend

From the repository root:

```bash
cd nevara
uv sync
uv run uvicorn nevara.server:app --host 0.0.0.0 --port 8000
```

If you are not using `uv`, the equivalent install flow is:

```bash
cd nevara
python -m pip install -e .
python -m uvicorn nevara.server:app --host 0.0.0.0 --port 8000
```

### 2) Start the Rust CLI

In a second terminal:

```bash
cd nevara-cli
cargo run
```

The CLI connects to `http://localhost:8000` by default and starts an interactive session.

## API overview

The backend exposes these endpoints:

- `GET /invoke?message=...`
  - legacy non-streaming invoke endpoint
- `POST /invoke_v2`
  - streaming endpoint returning SSE events
- `POST /upload`
  - upload a file into the `./res` directory and rebuild the vector store
- `GET /get_uploads`
  - list uploaded files
- `POST /remove_upload`
  - remove a file and rebuild the vector store

Uploaded documents are stored under `./res` inside the Python project when the server is running.

## Notes and caveats

- This is an experimental project rather than a production-ready agent platform.
- Several pieces are intentionally local-first and rely on a machine running Ollama.
- The system agent is designed for local system reasoning and repair workflows but should be used carefully because it may execute shell commands.
- Some code paths are still rough and may require environment-specific adjustments.

## Future direction

The current project description suggests a progression toward:

- more specialized workflow agents
- deeper agent reasoning loops
- custom thinking flows for autonomous system tasks
- richer multi-agent orchestration

## License

This repository does not currently declare a project license in the root files that were inspected.

## Contributing

If you want to work on the project, the best places to start are:

- `nevara/src/Agents/ConvAgent/`
- `nevara/src/Agents/SystemAgent/`
- `nevara/src/nevara/server.py`
- `nevara-cli/src/main.rs`

These are the main integration points for the agent behaviour and the client experience.
=======
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&text=TSUKUYOMI%20%7C%20BUILDING%20SMART%20SYSTEMS&fontSize=42&height=180&desc=AI%20%7C%20ML%20%7C%20ENGINEERING&descAlignY=75&descAlign=50" alt="Profile banner" />
</p>

<div align="center">
  <img src="https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif" width="420" alt="Coding and innovation animation" />
</div>

<h1 align="center">Hi, I'm Tsukuyomi 👋</h1>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=8B5CF6&center=true&vCenter=true&width=700&lines=Software+Engineer;Python+Developer;AI+%2F+ML+Explorer;Systems+Builder;Creative+Problem+Solver" alt="Typing SVG" />
</p>

<p align="center">
  I build software that blends <b>engineering</b>, <b>intelligence</b>, <b>automation</b>, and <b>creative interfaces</b>.
  <br>
  My work spans <b>Python</b>, <b>JavaScript/TypeScript</b>, <b>QML</b>, <b>ML</b>, <b>tooling</b>, and experimental systems.
</p>

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="JavaScript" src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" />
  <img alt="QML" src="https://img.shields.io/badge/QML-41CD52?style=for-the-badge&logo=qt&logoColor=white" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img alt="Linux" src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" />
  <img alt="Machine Learning" src="https://img.shields.io/badge/ML-AI%2FData-7C3AED?style=for-the-badge" />
  <img alt="Open Source" src="https://img.shields.io/badge/Open%20Source-Yes-2ea44f?style=for-the-badge" />
</p>

---

## About Me

I’m a developer focused on building useful systems and intelligent tools with a strong eye for design and performance.

My interests include:
- AI and machine learning experiments
- Automation and developer tooling
- Compiler/transpiler concepts
- Interactive UIs and futuristic desktop experiences
- Clean architecture, reusable libraries, and practical software design

I enjoy turning ideas into working prototypes and turning complex problems into elegant systems.

---

## Featured Projects

### 🧠 arcane-shell
A futuristic QML-based desktop shell and UI concept with mystical, immersive design.

- Repo: https://github.com/tsukuyomi-0001/arcane-shell
- Focus: custom UI experiences, visual systems, interface design

### ⚙️ Avntum
A high-level transpiler/compiler project aiming to bring fast, expressive programming workflows closer to native performance.

- Repo: https://github.com/tsukuyomi-0001/Avntum
- Focus: language tooling, transpilation, compiler design, developer ergonomics

### 🧪 corpus
A Python library focused on simplifying ML/data workflows and reducing repetitive boilerplate.

- Repo: https://github.com/tsukuyomi-0001/corpus
- Focus: data science, ML utilities, abstractions, reusable components

### 🧩 Ultron
TypeScript-based software with a systems-oriented approach to modern application development.

- Repo: https://github.com/tsukuyomi-0001/Ultron
- Focus: tooling, application architecture, experimentation

### 🤖 ML & DL Experimentation
Exploratory projects in machine learning and deep learning with practical hands-on learning.

- DL-project-1
- ML-project-1
- ML-project-2

---

## Tech Stack

<p align="left">
  <img src="https://img.shields.io/badge/Python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" />
  <img src="https://img.shields.io/badge/JavaScript-323330?style=flat-square&logo=javascript&logoColor=F7DF1E" />
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=flat-square&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/QML-41CD52?style=flat-square&logo=qt&logoColor=white" />
  <img src="https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white" />
  <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white" />
  <img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black" />
  <img src="https://img.shields.io/badge/ML-PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/Automation-Scripting-8B5CF6?style=flat-square" />
</p>

---

## GitHub Stats

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=tsukuyomi-0001&show_icons=true&theme=radical&hide_border=true&count_private=true" alt="GitHub Stats" height="180" />
  <img src="https://github-readme-streak-stats.herokuapp.com/?user=tsukuyomi-0001&theme=radical&hide_border=true" alt="GitHub Streak" height="180" />
</p>

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=tsukuyomi-0001&theme=react-dark&hide_border=true&area=true" alt="Contribution Graph" />
</p>

---

## Current Focus

- Building intelligent, practical tools
- Exploring AI/ML workflows and automation
- Designing better developer experiences
- Prototyping polished interfaces and desktop system concepts
- Continuing to learn, iterate, and ship meaningful projects

---

## Collaboration

Open to:
- AI / ML experiments
- developer tools
- automation systems
- creative software ideas
- research-driven prototypes
- open-source collaboration

If you’re building something ambitious, I’d love to connect and contribute.

---

<p align="center">
  <img src="https://img.shields.io/badge/Code%20with%20Purpose-Always-0A84FF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Build%20the%20Future-Now-8B5CF6?style=for-the-badge" />
</p>

<p align="center">
  <sub>Made with curiosity, code, and a love for building things that matter.</sub>
</p>
>>>>>>> 1d7db16 (improv v1)
