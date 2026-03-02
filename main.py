import sys
from typing import List

from core.embedding_model import EmbeddingModel
from core.schemas import CodeChunk
from parsing.metadata_extractor import MetadataExtractor
from parsing.chunker import build_chunks
from storage.path_manager import get_repo_name, get_branch_name
from storage.vector_store import VectorStore
from retrieval.bm25_index import build_index
from retrieval.hybrid_search import HybridSearch

DEFAULT_QUERY = "Find Kafka listener handling order events"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py <repo_path> [query]")
        sys.exit(1)

    repo_path = sys.argv[1]
    query = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_QUERY

    # --- repo identity ---
    repo = get_repo_name(repo_path)
    branch = get_branch_name(repo_path)
    print(f"Repo: {repo}  Branch: {branch}")

    # --- parse ---
    extractor = MetadataExtractor()
    parsed_files = extractor.extract_from_repo(repo_path)
    print(f"Parsed files: {len(parsed_files)}")

    # --- chunk ---
    all_chunks: List[CodeChunk] = []
    for pf in parsed_files:
        all_chunks.extend(build_chunks(pf))
    print(f"Total chunks: {len(all_chunks)}")

    if not all_chunks:
        print("No chunks found. Exiting.")
        return

    # --- embed ---
    model = EmbeddingModel()
    embeddings = model.embed_chunks(all_chunks)
    print(f"Embedding shape: {embeddings.shape}")

    # --- index & store ---
    store = VectorStore()
    store.add_documents(all_chunks, embeddings, repo, branch)

    # --- build BM25 ---
    bm25_index = build_index(all_chunks)

    # --- search ---
    print(f"\nQuery: {query!r}")
    query_embedding = model.embed_query(query)
    vector_results = store.search(query_embedding, repo, branch, top_k=20)

    hybrid = HybridSearch()
    top_results = hybrid.search(query, all_chunks, bm25_index, vector_results, top_k=5)

    # --- print results ---
    print(f"\nTop {len(top_results)} results:")
    for rank, (chunk, score) in enumerate(top_results, start=1):
        ann_str = ", ".join(chunk.annotations) if chunk.annotations else "—"
        method_str = chunk.method_name or "—"
        print(
            f"\n[{rank}] score={score:.4f}\n"
            f"  file:        {chunk.file_path}\n"
            f"  class:       {chunk.class_name}\n"
            f"  method:      {method_str}\n"
            f"  annotations: {ann_str}\n"
            f"  type:        {chunk.chunk_type}"
        )


if __name__ == "__main__":
    main()
