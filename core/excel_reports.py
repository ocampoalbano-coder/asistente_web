from __future__ import annotations

from pathlib import Path

import pandas as pd

from .utils import ensure_dirs, stamp


def generar_reporte(path_csv: str | Path) -> Path:
    """Lee un CSV y exporta un Excel simple en OUT_DIR."""
    ensure_dirs()
    path_csv = Path(path_csv)
    df = pd.read_csv(path_csv, encoding="utf-8")
    out_xlsx = stamp("reporte", "xlsx")
    with pd.ExcelWriter(out_xlsx, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Datos")
    return out_xlsx


# --- caching wrapper (xlsx) ---
try:
    import os
    import shutil
    import time

    from .cache import cached_output_paths

    _orig_generar_reporte = generar_reporte  # type: ignore[name-defined]

    def generar_reporte(csv_path):  # type: ignore[func-assign]
        paths = cached_output_paths(csv_path)
        tmpdir = os.environ.get("TMPDIR", "/tmp")
        os.makedirs(tmpdir, exist_ok=True)
        # 1) Si ya existe cache canónica, copiar a TMP y devolver
        if os.path.exists(paths["xlsx"]):
            ts = time.strftime("%Y%m%d_%H%M%S")
            tmp = os.path.join(tmpdir, f"reporte_{ts}.xlsx")
            try:
                shutil.copy2(paths["xlsx"], tmp)
                return tmp
            except Exception:
                return paths["xlsx"]
        # 2) Generar, guardar en cache canónica y devolver copia en TMP
        out = _orig_generar_reporte(csv_path)
        try:
            os.makedirs(os.path.dirname(paths["xlsx"]), exist_ok=True)
            shutil.copy2(out, paths["xlsx"])
        except Exception:
            pass
        try:
            ts = time.strftime("%Y%m%d_%H%M%S")
            tmp = os.path.join(tmpdir, f"reporte_{ts}.xlsx")
            shutil.copy2(out, tmp)
            return tmp
        except Exception:
            return out

except Exception:
    # No romper si algo falla: usar comportamiento original
    pass
