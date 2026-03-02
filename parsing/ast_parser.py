from dataclasses import dataclass, field
from typing import List, Optional
import tree_sitter_java
from tree_sitter import Language, Parser, Node


@dataclass
class ParsedMethod:
    name: str
    annotations: List[str]
    code: str


@dataclass
class ParsedClass:
    name: str
    annotations: List[str]
    body: str
    methods: List[ParsedMethod] = field(default_factory=list)


@dataclass
class ParsedFile:
    file_path: str
    package_name: str
    imports: List[str]
    classes: List[ParsedClass]


def _node_text(node: Node, source: bytes) -> str:
    return source[node.start_byte:node.end_byte].decode("utf-8", errors="replace")


def _extract_annotations(modifiers_node: Optional[Node], source: bytes) -> List[str]:
    if modifiers_node is None:
        return []
    annotations = []
    for child in modifiers_node.children:
        if child.type in ("marker_annotation", "annotation"):
            name_node = child.child_by_field_name("name")
            if name_node:
                annotations.append(_node_text(name_node, source))
    return annotations


def _find_modifiers(node: Node) -> Optional[Node]:
    for child in node.children:
        if child.type == "modifiers":
            return child
    return None


def _extract_methods(class_body: Node, source: bytes) -> List[ParsedMethod]:
    methods = []
    for child in class_body.children:
        if child.type == "method_declaration":
            modifiers = _find_modifiers(child)
            annotations = _extract_annotations(modifiers, source)
            name_node = child.child_by_field_name("name")
            if name_node is None:
                continue
            name = _node_text(name_node, source)
            code = _node_text(child, source)
            methods.append(ParsedMethod(name=name, annotations=annotations, code=code))
    return methods


def _extract_classes(root: Node, source: bytes) -> List[ParsedClass]:
    classes = []
    _walk_for_classes(root, source, classes)
    return classes


def _walk_for_classes(node: Node, source: bytes, classes: List[ParsedClass]) -> None:
    if node.type == "class_declaration":
        modifiers = _find_modifiers(node)
        annotations = _extract_annotations(modifiers, source)
        name_node = node.child_by_field_name("name")
        if name_node:
            class_name = _node_text(name_node, source)
            body_node = node.child_by_field_name("body")
            body_text = _node_text(body_node, source) if body_node else ""
            methods = _extract_methods(body_node, source) if body_node else []
            classes.append(
                ParsedClass(
                    name=class_name,
                    annotations=annotations,
                    body=body_text,
                    methods=methods,
                )
            )
            # recurse into body for nested classes
            if body_node:
                for child in body_node.children:
                    _walk_for_classes(child, source, classes)
            return  # don't double-recurse from the class node itself

    for child in node.children:
        _walk_for_classes(child, source, classes)


class JavaASTParser:
    def __init__(self) -> None:
        self._parser = Parser(Language(tree_sitter_java.language()))

    def parse_file(self, file_path: str) -> Optional[ParsedFile]:
        try:
            with open(file_path, "rb") as f:
                source = f.read()
        except OSError:
            return None

        tree = self._parser.parse(source)
        root = tree.root_node

        package_name = self._extract_package(root, source)
        imports = self._extract_imports(root, source)
        classes = _extract_classes(root, source)

        return ParsedFile(
            file_path=file_path,
            package_name=package_name,
            imports=imports,
            classes=classes,
        )

    def _extract_package(self, root: Node, source: bytes) -> str:
        for child in root.children:
            if child.type == "package_declaration":
                # look for scoped_identifier or identifier child
                for sub in child.children:
                    if sub.type in ("scoped_identifier", "identifier"):
                        return _node_text(sub, source)
        return ""

    def _extract_imports(self, root: Node, source: bytes) -> List[str]:
        imports = []
        for child in root.children:
            if child.type == "import_declaration":
                imports.append(_node_text(child, source).strip())
        return imports
