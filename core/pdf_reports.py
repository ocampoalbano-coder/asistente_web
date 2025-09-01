from __future__ import annotations

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .utils import ensure_dirs, stamp


def generar_pdf(csv_path: Path) -> Path:
    """Genera un PDF bÃ¡sico a partir del CSV y lo guarda en OUT_DIR."""
    ensure_dirs()
    csv_path = Path(csv_path)
    # Lectura robusta: infiere separador y hace fallback si falla
    try:
        if Path(csv_path).suffix.lower() in (".xlsx", ".xls"):
            df = pd.read_excel(csv_path, engine="openpyxl")
        else:
            # sep=None => infiere ; , \t, etc. (engine=python)
            df = pd.read_csv(csv_path, sep=None, engine="python", encoding="utf-8")
    except Exception:
        # Fallback 1: separador ; (muy común en regiones ES)
        try:
            df = pd.read_csv(csv_path, sep=";", engine="python", encoding="utf-8")
        except Exception:
            # Fallback 2: intentar como Excel por si la extensión está mal
            df = pd.read_excel(csv_path, engine="openpyxl")
    out_pdf = stamp("reporte", "pdf")
    doc = SimpleDocTemplate(str(out_pdf), pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Reporte", styles["Title"]))
    story.append(Spacer(1, 12))

    # Cabeceras + filas
    data = [list(df.columns)] + df.values.tolist()
    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a233b")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#2a3355")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#0f1628")),
            ]
        )
    )

    story.append(table)
    doc.build(story)
    return out_pdf


# --- caching wrapper (pdf) ---
try:
    import os
    import shutil
    import time

    from .cache import cached_output_paths

    _orig_generar_pdf = generar_pdf  # type: ignore[name-defined]

    def generar_pdf(csv_path):  # type: ignore[func-assign]
        paths = cached_output_paths(csv_path)
        tmpdir = os.environ.get("TMPDIR", "/tmp")
        os.makedirs(tmpdir, exist_ok=True)
        # 1) Si ya existe cache canónica, copiar a TMP y devolver
        if os.path.exists(paths["pdf"]):
            ts = time.strftime("%Y%m%d_%H%M%S")
            tmp = os.path.join(tmpdir, f"reporte_{ts}.pdf")
            try:
                shutil.copy2(paths["pdf"], tmp)
                return tmp
            except Exception:
                return paths["pdf"]
        # 2) Generar, guardar en cache canónica y devolver copia en TMP
        out = _orig_generar_pdf(csv_path)
        try:
            os.makedirs(os.path.dirname(paths["pdf"]), exist_ok=True)
            shutil.copy2(out, paths["pdf"])
        except Exception:
            pass
        try:
            ts = time.strftime("%Y%m%d_%H%M%S")
            tmp = os.path.join(tmpdir, f"reporte_{ts}.pdf")
            shutil.copy2(out, tmp)
            return tmp
        except Exception:
            return out

except Exception:
    # No romper si algo falla: usar comportamiento original
    pass
