# agentic-code-intelligence
Agentic AI for repository code intelligence, semantic indexing, and automated developer assistance using local embeddings and AST parsing.

# agentic-code-intelligence

Agentic AI system for repository code intelligence, semantic indexing, and developer productivity.

This project builds a local-first AI system that can understand source code structure, perform semantic search, and assist developers by analyzing repository content using AST parsing, local embeddings, and hybrid retrieval.

The system is designed to work with real backend repositories and support future agentic features such as unit test generation, integration test suggestion, and PR review.


---

## Goals

The purpose of this project is to create an internal AI assistant that can:

- Understand Java / Spring Boot source code
- Index repository per branch
- Perform semantic + keyword search
- Understand custom annotations
- Provide context-aware retrieval
- Enable future agentic automation

Future capabilities:

- Unit test generation
- Integration test generation
- PR review assistant
- Coverage analysis
- CI integration
- Multi-agent orchestration


---

## Design Principles

- Privacy first
- Local embeddings only
- No external embedding API
- Structure-aware parsing
- Deterministic indexing
- Repo-aware storage
- Branch-aware storage
- Annotation-aware retrieval
- Modular architecture


---

## Technology Stack

- Python 3.11
- tree-sitter
- sentence-transformers
- FAISS
- rank-bm25
- Pydantic


---

## High Level Architecture

```mermaid
flowchart TD

A[Java Repository] --> B[AST Parser]
B --> C[Metadata Extractor]
C --> D[Smart Chunker]

D --> E[Embedding Model]
E --> F[FAISS Vector Store]

D --> G[BM25 Index]

F --> H[Hybrid Retrieval]
G --> H

H --> I[Search Result]
```

---

## Indexing Flow

This flow runs when indexing a repository branch.

```mermaid
flowchart TD

A[Repo Path] --> B[Detect Repo Name]
B --> C[Detect Branch Name]

C --> D[Parse Java Files]
D --> E[Extract Classes / Methods / Annotations]

E --> F[Build Code Chunks]

F --> G[Format Chunk Text]
G --> H[Local Embedding Model]

H --> I[FAISS Index]
F --> J[Metadata JSON]

F --> K[BM25 Index]

I --> L[Stored per Repo / Branch]
J --> L
K --> L
```

---

## Retrieval Flow

This flow runs when searching code.

```mermaid
flowchart TD

A[User Query] --> B[Embed Query]
B --> C[Vector Search FAISS]

A --> D[Keyword Search BM25]

C --> E[Combine Scores]
D --> E

E --> F[Metadata Boost]

F --> G[Rank Results]
G --> H[Return Code Chunks]
```

---

## Storage Layout

Index data is stored per repository and per branch.

```
data/
  {repo_name}/
    {branch_name}/
      faiss_index.bin
      metadata.json
```

Example:

```
data/point-of-sale-backend-engine/master/faiss_index.bin
data/point-of-sale-backend-engine/master/metadata.json

data/point-of-sale-backend-engine/feature_custom_food/faiss_index.bin
data/point-of-sale-backend-engine/feature_custom_food/metadata.json
```


---

## Annotation Registry

Custom annotations can be described in:

```
config/annotation_registry.json
```

Example:

```
{
  "AuditLog": "Marks method for audit logging",
  "BusinessFlow": "Defines business flow identifier",
  "InternalKafkaConsumer": "Consumes internal kafka topic"
}
```

This improves semantic embedding quality.


---

## Agentic AI Roadmap

This project is designed for multiphase agentic system.

```mermaid
flowchart TD

A[Code Intelligence Core] --> B[Unit Test Agent]
B --> C[Integration Test Agent]
C --> D[PR Review Agent]
D --> E[Coverage Agent]
E --> F[CI Integration Agent]
F --> G[Multi-Agent System]
```

Phase 1
- Code parsing
- Chunking
- Embedding
- Retrieval

Phase 2
- Unit test generation

Phase 3
- Integration test generation

Phase 4
- PR analysis

Phase 5
- Multi-agent orchestration


---

## Future Agent Flow

```mermaid
flowchart TD

A[User Request] --> B[Planner Agent]

B --> C[Code Analyzer Agent]
B --> D[Test Generator Agent]
B --> E[PR Reviewer Agent]

C --> F[Hybrid Retrieval]
D --> F
E --> F

F --> G[Vector Store]
F --> H[BM25]

G --> I[Result]
H --> I
```

---

## Status

Phase 1 – Code Intelligence Core  
In progress


---

## Purpose

This repository is intended for internal developer productivity tooling and experimentation with agentic AI for source code understanding.

Sensitive source code should remain inside approved environments.

---

## Tutorial — How to use Code Intelligence Core

This section explains how to use the Code Intelligence Core to index a repository and perform semantic search.

The current phase supports:

- Java repository parsing
- AST-based chunking
- Local embeddings
- FAISS vector storage
- BM25 keyword search
- Hybrid retrieval
- Repo-aware indexing
- Branch-aware indexing
- Annotation registry support


---

### 1. Install dependencies

Create virtual environment:

```
python -m venv venv
source venv/bin/activate
```

Install required packages:

```
pip install sentence-transformers
pip install faiss-cpu
pip install tree-sitter
pip install rank-bm25
pip install pydantic
pip install numpy
```

You must also install tree-sitter-java grammar.


---

### 2. Prepare repository to index

Example repository:

```
/workspace/point-of-sale-backend-engine
```

Make sure repository is a git repo and has branch checked out.

Example:

```
git checkout feature/improvement-custom-food-ingridient
```


---

### 3. Optional — Configure annotation registry

Create file:

```
config/annotation_registry.json
```

Example:

```
{
  "AuditLog": "Marks method for audit logging",
  "BusinessFlow": "Defines business flow identifier",
  "InternalKafkaConsumer": "Consumes internal kafka topic",
  "CheckPermission": "Requires permission check"
}
```

This improves embedding quality for custom annotations.


---

### 4. Run indexing

Run:

```
python main.py /workspace/point-of-sale-backend-engine
```

The system will:

1. Detect repo name
2. Detect branch name
3. Parse Java files
4. Extract classes and methods
5. Build chunks
6. Generate embeddings locally
7. Save FAISS index
8. Save metadata.json
9. Build BM25 index


---

### 5. Storage result

Data will be stored automatically:

```
data/{repo_name}/{branch_name}/
```

Example:

```
data/point-of-sale-backend-engine/master/faiss_index.bin
data/point-of-sale-backend-engine/master/metadata.json

data/point-of-sale-backend-engine/feature_improvement_custom_food/faiss_index.bin
data/point-of-sale-backend-engine/feature_improvement_custom_food/metadata.json
```

Each branch has its own index.


---

### 6. Run search

After indexing, the system will run a sample query:

```
Find Kafka listener handling order events
```

Output example:

```
File: OrderConsumer.java
Class: OrderConsumer
Method: handleOrderCreated

@KafkaListener(...)
public void handleOrderCreated(...)
```


---

### 7. Switching branch

If you change branch:

```
git checkout feature/improvement-add-on-beverage
```

Run indexing again:

```
python main.py /workspace/point-of-sale-backend-engine
```

New index will be stored in a different folder.

Old index will not be overwritten.


---

### 8. Re-index behavior

Current version rebuilds index for the branch.

Future version may support incremental indexing.


---

### 9. Expected usage in future phases

This Code Intelligence Core will be used by future agents:

- Unit test generator
- Integration test generator
- PR reviewer
- Coverage analyzer
- CI agent

All agents will use hybrid retrieval from this index.


---

### 10. Notes

- Embeddings run locally
- No source code sent to external API
- Safe for internal repository
- Supports custom annotations
- Supports multiple branches
- Supports multiple repositories