from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

try:
    import tomllib  # py311+
except Exception:  # pragma: no cover
    tomllib = None  # type: ignore

# Raíz y carpetas
ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
DATA = ROOT / "data"

# Directorio de salida: local ./salida, en Render usar OUTPUT_DIR=/tmp/salida
OUT_DIR = Path(os.environ.get("OUTPUT_DIR", ROOT / "salida")).resolve()


def ensure_dirs() -> None:
    """Crea las carpetas necesarias (incluye OUT_DIR y DATA)."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)


def stamp(prefix: str, ext: str) -> Path:
    """Devuelve una ruta con timestamp dentro de OUT_DIR."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return OUT_DIR / f"{prefix}_{ts}.{ext}"
