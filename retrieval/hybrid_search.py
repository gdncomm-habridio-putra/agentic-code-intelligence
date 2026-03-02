from typing import List, Tuple, Dict
from rank_bm25 import BM25Okapi

from core.config import VECTOR_WEIGHT, BM25_WEIGHT, METHOD_BOOST, ANNOTATION_BOOST
from core.schemas import CodeChunk
from retrieval.bm25_index import keyword_search


class HybridSearch:
    def search(
        self,
        query: str,
        chunks: List[CodeChunk],
        bm25_index: BM25Okapi,
        vector_results: List[Tuple[CodeChunk, float]],
        top_k: int = 5,
    ) -> List[Tuple[CodeChunk, float]]:
        # --- vector scores ---
        if vector_results:
            max_l2 = max(dist for _, dist in vector_results) or 1.0
        else:
            max_l2 = 1.0

        vector_score_map: Dict[str, float] = {}
        for chunk, dist in vector_results:
            vector_score_map[chunk.id] = 1.0 - (dist / max_l2)

        # --- BM25 scores (full corpus) ---
        bm25_results = keyword_search(bm25_index, query, chunks, top_k=len(chunks))
        max_bm25 = max((score for _, score in bm25_results), default=1.0) or 1.0

        bm25_score_map: Dict[str, float] = {
            chunk.id: score / max_bm25 for chunk, score in bm25_results
        }

        # --- combine over all chunks that appear in either result set ---
        candidate_ids = set(vector_score_map) | set(bm25_score_map)
        chunk_by_id: Dict[str, CodeChunk] = {c.id: c for c in chunks}

        scored: List[Tuple[CodeChunk, float]] = []
        for cid in candidate_ids:
            chunk = chunk_by_id.get(cid)
            if chunk is None:
                continue

            v_score = vector_score_map.get(cid, 0.0)
            b_score = bm25_score_map.get(cid, 0.0)

            metadata_boost = 0.0
            if chunk.chunk_type == "method":
                metadata_boost += METHOD_BOOST
            if chunk.annotations:
                metadata_boost += ANNOTATION_BOOST

            final = VECTOR_WEIGHT * v_score + BM25_WEIGHT * b_score + metadata_boost
            scored.append((chunk, final))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
