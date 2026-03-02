from typing import List, Tuple
import numpy as np
import faiss

from core.config import EMBEDDING_DIMENSION
from core.schemas import CodeChunk
from storage.path_manager import get_faiss_path, get_metadata_path
from storage.metadata_store import save_metadata, load_metadata


class VectorStore:
    def add_documents(
        self,
        chunks: List[CodeChunk],
        embeddings: np.ndarray,
        repo: str,
        branch: str,
    ) -> None:
        index = faiss.IndexFlatL2(EMBEDDING_DIMENSION)
        index.add(embeddings)

        faiss_path = get_faiss_path(repo, branch)
        metadata_path = get_metadata_path(repo, branch)

        faiss.write_index(index, faiss_path)
        save_metadata(metadata_path, chunks)

        print(f"Saved FAISS index to {faiss_path}")
        print(f"Saved metadata to {metadata_path}")

    def search(
        self,
        query_embedding: np.ndarray,
        repo: str,
        branch: str,
        top_k: int = 20,
    ) -> List[Tuple[CodeChunk, float]]:
        faiss_path = get_faiss_path(repo, branch)
        metadata_path = get_metadata_path(repo, branch)

        index = faiss.read_index(faiss_path)
        chunks = load_metadata(metadata_path)

        distances, indices = index.search(query_embedding, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(chunks):
                continue
            results.append((chunks[idx], float(dist)))

        return results
