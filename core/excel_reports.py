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
