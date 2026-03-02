import os
import subprocess

from core.config import DATA_DIR


def get_repo_name(repo_path: str) -> str:
    return os.path.basename(os.path.abspath(repo_path))


def get_branch_name(repo_path: str) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        branch = result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        branch = "unknown"

    # sanitise: / → _, - → _
    branch = branch.replace("/", "_").replace("-", "_")
    return branch


def get_storage_dir(repo: str, branch: str) -> str:
    path = os.path.join(DATA_DIR, repo, branch)
    os.makedirs(path, exist_ok=True)
    return path


def get_faiss_path(repo: str, branch: str) -> str:
    return os.path.join(get_storage_dir(repo, branch), "faiss_index.bin")


def get_metadata_path(repo: str, branch: str) -> str:
    return os.path.join(get_storage_dir(repo, branch), "metadata.json")
