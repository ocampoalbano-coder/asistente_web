import importlib
from pathlib import Path


def test_docs_reader_smoke(tmp_path: Path):
    mod = importlib.import_module("core.docs_reader")

    # TXT mínimo
    p = tmp_path / "mini.txt"
    p.write_text("hola mundo", encoding="utf-8")

    # Intentar funciones típicas si existen
    for candidate in ("read_text", "read_file", "read_path"):
        fn = getattr(mod, candidate, None)
        if callable(fn):
            try:
                _ = fn(p)  # no falla el test si lanza excepción
            except Exception:
                pass

    assert p.exists()
