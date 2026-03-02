from typing import List, Tuple
from rank_bm25 import BM25Okapi

from core.schemas import CodeChunk


def build_index(chunks: List[CodeChunk]) -> BM25Okapi:
    corpus = [chunk.code.lower().split() for chunk in chunks]
    return BM25Okapi(corpus)


def keyword_search(
    index: BM25Okapi,
    query: str,
    chunks: List[CodeChunk],
    top_k: int,
) -> List[Tuple[CodeChunk, float]]:
    tokenised_query = query.lower().split()
    scores = index.get_scores(tokenised_query)

    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
    return [(chunks[i], float(score)) for i, score in ranked]
