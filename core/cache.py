import hashlib
import os

from .utils import OUT_DIR, ensure_dirs


def file_sha256(path, chunk_size=65536):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def cached_output_paths(csv_path):
    ensure_dirs()
    h = file_sha256(csv_path)
    base = os.path.join(OUT_DIR, f"reporte_{h}")
    return {"hash": h, "xlsx": base + ".xlsx", "pdf": base + ".pdf"}
