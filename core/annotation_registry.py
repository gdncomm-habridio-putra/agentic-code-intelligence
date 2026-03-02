import json
from typing import Dict, Optional
from core.config import ANNOTATION_REGISTRY_PATH


def load_annotation_registry() -> Dict[str, str]:
    try:
        with open(ANNOTATION_REGISTRY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
        return {}
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def get_annotation_description(name: str) -> Optional[str]:
    registry = load_annotation_registry()
    return registry.get(name)
