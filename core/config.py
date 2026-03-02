import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")
ANNOTATION_REGISTRY_PATH = os.path.join(CONFIG_DIR, "annotation_registry.json")

EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"
EMBEDDING_DIMENSION = 1024

VECTOR_WEIGHT = 0.6
BM25_WEIGHT = 0.3
METADATA_WEIGHT = 0.1

METHOD_BOOST = 0.05
ANNOTATION_BOOST = 0.05
