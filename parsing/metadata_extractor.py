import os
from typing import List

from parsing.ast_parser import JavaASTParser, ParsedFile

_SKIP_DIRS = {".git", "target", "build", "out"}


class MetadataExtractor:
    def __init__(self) -> None:
        self._parser = JavaASTParser()

    def extract_from_repo(self, repo_path: str) -> List[ParsedFile]:
        parsed_files: List[ParsedFile] = []

        for dirpath, dirnames, filenames in os.walk(repo_path):
            # prune skipped directories in-place
            dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]

            for filename in filenames:
                if not filename.endswith(".java"):
                    continue
                full_path = os.path.join(dirpath, filename)
                parsed = self._parser.parse_file(full_path)
                if parsed is None:
                    continue
                if not parsed.classes:
                    continue
                parsed_files.append(parsed)

        return parsed_files
