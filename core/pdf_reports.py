from __future__ import annotations
from pathlib import Path
from datetime import datetime

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

def generar_pdf(csv_path: Path) -> Path:
    csv_path = Path(csv_path)
    root = csv_path.resolve().parents[1]  # raíz del proyecto (asistente_web)
    out_dir = root / "salida"
    out_dir.mkdir(parents=True, exist_ok=True)

    # leer datos
    try:
        df = pd.read_csv(csv_path)
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="latin-1")

    if "categoria" not in df.columns or "monto" not in df.columns:
        raise ValueError("El CSV debe incluir columnas 'categoria' y 'monto'.")

    df["monto"] = pd.to_numeric(df["monto"], errors="coerce").fillna(0)
    resumen = (
        df.groupby("categoria", dropna=False)["monto"]
          .agg(monto_total="sum", items="count")
          .reset_index()
    )

    out_pdf = out_dir / f"reporte_{datetime.now():%Y%m%d_%H%M%S}.pdf"
    doc = SimpleDocTemplate(str(out_pdf), pagesize=A4)
    styles = getSampleStyleSheet()

    elems = [
        Paragraph("Reporte de Ventas", styles["Title"]),
        Paragraph(datetime.now().strftime("%d/%m/%Y %H:%M"), styles["Normal"]),
        Spacer(1, 12),
    ]

    data = [["categoria", "monto_total", "items"]] + resumen.values.tolist()
    table = Table(data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (1,1), (-1,-1), "RIGHT"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey]),
        ("LEFTPADDING",(0,0),(-1,-1),6), ("RIGHTPADDING",(0,0),(-1,-1),6)
    ]))
    elems.append(table)

    doc.build(elems)
    return out_pdf
