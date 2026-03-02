import hashlib
from typing import List, Optional
from pydantic import BaseModel, Field


def _make_id(file_path: str, class_name: str, method_name: Optional[str]) -> str:
    key = f"{file_path}::{class_name}::{method_name or ''}"
    return hashlib.md5(key.encode()).hexdigest()


class CodeChunk(BaseModel):
    id: str
    file_path: str
    package_name: str
    class_name: str
    method_name: Optional[str] = None
    annotations: List[str] = Field(default_factory=list)
    imports: List[str] = Field(default_factory=list)
    chunk_type: str  # "class" | "method"
    code: str

    @classmethod
    def create(
        cls,
        file_path: str,
        package_name: str,
        class_name: str,
        method_name: Optional[str],
        annotations: List[str],
        imports: List[str],
        chunk_type: str,
        code: str,
    ) -> "CodeChunk":
        return cls(
            id=_make_id(file_path, class_name, method_name),
            file_path=file_path,
            package_name=package_name,
            class_name=class_name,
            method_name=method_name,
            annotations=annotations,
            imports=imports,
            chunk_type=chunk_type,
            code=code,
        )
