from typing import List

from core.schemas import CodeChunk
from parsing.ast_parser import ParsedFile


def build_chunks(parsed_file: ParsedFile) -> List[CodeChunk]:
    chunks: List[CodeChunk] = []

    for cls in parsed_file.classes:
        # class-level chunk
        chunks.append(
            CodeChunk.create(
                file_path=parsed_file.file_path,
                package_name=parsed_file.package_name,
                class_name=cls.name,
                method_name=None,
                annotations=cls.annotations,
                imports=parsed_file.imports,
                chunk_type="class",
                code=cls.body,
            )
        )

        # method-level chunks
        for method in cls.methods:
            chunks.append(
                CodeChunk.create(
                    file_path=parsed_file.file_path,
                    package_name=parsed_file.package_name,
                    class_name=cls.name,
                    method_name=method.name,
                    annotations=method.annotations,
                    imports=parsed_file.imports,
                    chunk_type="method",
                    code=method.code,
                )
            )

    return chunks
