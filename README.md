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
