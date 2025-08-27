import pandas as pd
from pathlib import Path
from .utils import stamp, ensure_dirs

def generar_reporte(path_csv: str | Path):
    ensure_dirs()
    df = pd.read_csv(path_csv, encoding="utf-8")
    df.columns = [c.strip() for c in df.columns]
    if "categoria" not in df.columns:
        df["categoria"] = "Sin categorÃ­a"
    if "monto" not in df.columns:
        df["monto"] = 0
    if "id" not in df.columns:
        df["id"] = range(1, len(df) + 1)
    resumen = (df.groupby("categoria")
                 .agg(monto_total=("monto","sum"), items=("id","count"))
                 .reset_index())
    out_xlsx = stamp("reporte","xlsx")
    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as xw:
        df.to_excel(xw, index=False, sheet_name="Datos_Limpios")
        resumen.to_excel(xw, index=False, sheet_name="Resumen")
    return out_xlsx
