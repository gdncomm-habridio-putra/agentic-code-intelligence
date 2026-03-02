from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer

from core.config import EMBEDDING_MODEL_NAME
from core.schemas import CodeChunk
from core.annotation_registry import load_annotation_registry


class EmbeddingModel:
    def __init__(self) -> None:
        self._model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self._registry: Dict[str, str] = load_annotation_registry()

    def _format_chunk(self, chunk: CodeChunk) -> str:
        lines = [
            f"FILE: {chunk.file_path}",
            f"PACKAGE: {chunk.package_name}",
            f"CLASS: {chunk.class_name}",
        ]
        if chunk.method_name:
            lines.append(f"METHOD: {chunk.method_name}")

        if chunk.annotations:
            lines.append("")
            lines.append("ANNOTATIONS:")
            for ann in chunk.annotations:
                desc = self._registry.get(ann)
                if desc:
                    lines.append(f"{ann} - {desc}")
                else:
                    lines.append(ann)

        if chunk.imports:
            lines.append("")
            lines.append("IMPORTS:")
            lines.extend(chunk.imports)

        lines.append("")
        lines.append("CODE:")
        lines.append(chunk.code)

        return "\n".join(lines)

    def embed_chunks(self, chunks: List[CodeChunk]) -> np.ndarray:
        texts = [self._format_chunk(c) for c in chunks]
        embeddings = self._model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        return embeddings.astype(np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        embedding = self._model.encode([query], convert_to_numpy=True)
        return embedding.astype(np.float32)
