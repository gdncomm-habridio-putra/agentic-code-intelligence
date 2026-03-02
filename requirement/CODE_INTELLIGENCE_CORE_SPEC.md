# Code Intelligence Core Specification

## Objective

Build a Python 3.11 project that indexes a Java repository and provides semantic and keyword retrieval over source code.

The system must:

- Parse Java source code using AST
- Extract structured metadata
- Create structure-aware chunks
- Generate embeddings locally
- Store embeddings in FAISS
- Store metadata in JSON
- Support repository-aware storage
- Support branch-aware storage
- Support hybrid retrieval (vector + BM25 + metadata boost)
- Support custom annotation knowledge registry

This specification defines exact architecture, data model, storage layout, and behavior.


--------------------------------------------------

## Project Root Definition

Agent project root:

agentic-code-intelligence/

Indexed repository path is provided at runtime.

Example:

python main.py /workspace/point-of-sale-backend-engine


--------------------------------------------------

## Technology Stack

Language:
- Python 3.11+

Embedding:
- sentence-transformers
- model: BAAI/bge-large-en-v1.5
- embedding dimension = 1024
- embedding dtype = float32

Vector DB:
- FAISS
- index type: IndexFlatL2

AST parser:
- tree-sitter
- tree-sitter-java

Keyword search:
- rank-bm25

Validation:
- Pydantic

Array library:
- numpy


--------------------------------------------------

## Project Structure

agentic-code-intelligence/
core/
config.py
embedding_model.py
schemas.py
annotation_registry.py

    parsing/
        ast_parser.py
        metadata_extractor.py
        chunker.py

    storage/
        vector_store.py
        metadata_store.py
        path_manager.py

    retrieval/
        bm25_index.py
        hybrid_search.py

    config/
        annotation_registry.json

    data/

    requirement/

    main.py


--------------------------------------------------

## Annotation Registry

Location:

agentic-code-intelligence/config/annotation_registry.json

This file belongs to the agent project.

This file is optional.

If file does not exist, system must use empty registry.

Example:

{
"AuditLog": "Marks method for audit logging",
"BusinessFlow": "Defines business flow identifier",
"InternalKafkaConsumer": "Consumes internal kafka topic",
"CheckPermission": "Requires permission check"
}


File: core/annotation_registry.py

Functions:

load_annotation_registry() -> Dict[str, str]

get_annotation_description(name: str) -> Optional[str]


--------------------------------------------------

## Repository and Branch Aware Storage

Storage root:

agentic-code-intelligence/data/

Structure:

data/{repo_name}/{branch_name}/

Files:

faiss_index.bin
metadata.json


Example:

data/point-of-sale-backend-engine/master/faiss_index.bin
data/point-of-sale-backend-engine/master/metadata.json

Branch sanitize rules:

replace "/" -> "_"
replace "-" -> "_"


--------------------------------------------------

## Path Manager

File: storage/path_manager.py

Functions:

get_repo_name(repo_path: str) -> str

get_branch_name(repo_path: str) -> str

Use command:

git rev-parse --abbrev-ref HEAD

get_storage_dir(repo, branch) -> str

get_faiss_path(repo, branch) -> str

get_metadata_path(repo, branch) -> str

Must create directory if not exists.


--------------------------------------------------

## Data Model

File: core/schemas.py

Class CodeChunk

Fields:

id: str
file_path: str
package_name: str
class_name: str
method_name: Optional[str]
annotations: List[str]
imports: List[str]
chunk_type: str
code: str

chunk_type allowed:

class
method


Chunk id rule:

id must be unique string

Format:

file_path + class_name + method_name


--------------------------------------------------

## AST Parser

File: parsing/ast_parser.py

Use tree-sitter-java.

Extract:

package name
imports
class name
method name
annotations
method body
class body

Return structured data.


--------------------------------------------------

## Chunking

File: parsing/chunker.py

Function:

build_chunks(parsed_file_data) -> List[CodeChunk]

Rules:

Create class chunk

Create method chunk per method

Fill all fields.


--------------------------------------------------

## Embedding Model

File: core/embedding_model.py

Model:

SentenceTransformer("BAAI/bge-large-en-v1.5")

Embedding dimension = 1024

Function:

embed_chunks(chunks: List[CodeChunk]) -> numpy.ndarray

Return:

numpy.ndarray
dtype float32
shape (N, 1024)


Text format:

FILE: ...
PACKAGE: ...
CLASS: ...
METHOD: ...

ANNOTATIONS:
name - description

IMPORTS:
...

CODE:
...


--------------------------------------------------

## Vector Store

File: storage/vector_store.py

Use:

faiss.IndexFlatL2(1024)

Store file:

faiss_index.bin

Metadata file:

metadata.json

Mapping rule:

embedding index == metadata index

Implement class:

VectorStore

Methods:

add_documents(chunks, embeddings, repo, branch)

search(query_embedding, repo, branch, top_k)


Behavior:

overwrite index for branch


--------------------------------------------------

## Metadata Store

File: storage/metadata_store.py

save_metadata(path, chunks)

load_metadata(path)


Store as JSON list.


--------------------------------------------------

## BM25

File: retrieval/bm25_index.py

Use rank-bm25

Index:

chunk.code

Functions:

build_index

keyword_search


--------------------------------------------------

## Hybrid Search

File: retrieval/hybrid_search.py

final_score =
0.6 vector
0.3 bm25
0.1 metadata

boost rules:

+0.05 method
+0.05 annotation


--------------------------------------------------

## Main Flow

main.py

Steps:

read repo path

detect repo

detect branch

parse

chunk

embed

store

build bm25

query

print result


--------------------------------------------------

## Code Quality

- Use type hints
- Use classes
- Use docstrings
- Handle missing files
- Create directories automatically
- No global state
- Configurable paths


--------------------------------------------------

## Output Requirement

- Generate full project
- Include install steps
- Include run steps
- Include explanation