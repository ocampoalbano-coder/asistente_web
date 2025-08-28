import tomllib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
DATA = ROOT / "data"
SALIDA = ROOT / "salida"


def load_settings():
    with open(CONFIG / "settings.toml", "rb") as f:
        return tomllib.load(f)


def ensure_dirs():
    SALIDA.mkdir(parents=True, exist_ok=True)


def stamp(prefix: str, ext: str):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return SALIDA / f"{prefix}_{ts}.{ext}"
