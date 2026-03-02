import json
from typing import List

from core.schemas import CodeChunk


def save_metadata(path: str, chunks: List[CodeChunk]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump([c.model_dump() for c in chunks], f)


def load_metadata(path: str) -> List[CodeChunk]:
    with open(path, "r", encoding="utf-8") as f:
        items = json.load(f)
    return [CodeChunk(**item) for item in items]
