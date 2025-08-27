from flask import Flask, render_template, request, send_from_directory
from pathlib import Path
import os, sys
import pandas as pd

# asegurar que el paquete core sea visible
sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.excel_reports import generar_reporte
from core.pdf_reports import generar_pdf
from core.utils import ensure_dirs

ROOT = Path(__file__).resolve().parents[1]
UPLOAD_DIR = ROOT / "data"
OUT_DIR    = ROOT / "salida"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, template_folder="templates", static_folder="../static")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        f = request.files.get("file")
        formato = (request.form.get("formato") or "excel").lower()
        if not f or not f.filename:
            return render_template("index.html", error="Sube un archivo CSV/XLSX.")

        if not (f.filename.lower().endswith(".csv") or f.filename.lower().endswith(".xlsx")):
            return render_template("index.html", error="Formato inválido. Solo CSV o XLSX.")

        # guardar
        save_path = UPLOAD_DIR / f.filename
        save_path.parent.mkdir(parents=True, exist_ok=True)
        f.save(save_path)

        # convertir xlsx -> csv si hace falta
        csv_path = save_path
        if save_path.suffix.lower() == ".xlsx":
            df_x = pd.read_excel(save_path)
            csv_path = save_path.with_suffix(".csv")
            df_x.to_csv(csv_path, index=False)

        # validaciones mínimas
        try:
            try:
                df = pd.read_csv(csv_path)
            except UnicodeDecodeError:
                df = pd.read_csv(csv_path, encoding="latin-1")
        except Exception as e:
            return render_template("index.html", error=f"Error leyendo el archivo: {e}")

        if "categoria" not in df.columns or "monto" not in df.columns:
            return render_template("index.html", error="Tu archivo debe tener columnas 'categoria' y 'monto'.")

        # generar salidas
        excel_name = pdf_name = None
        if formato in ("excel", "ambos"):
            xlsx = generar_reporte(csv_path)
            excel_name = Path(xlsx).name
        if formato in ("pdf", "ambos"):
            pdf = generar_pdf(csv_path)
            pdf_name = Path(pdf).name

        return render_template("result.html", excel=excel_name, pdf=pdf_name)

    return render_template("index.html")

@app.route("/download/<path:fname>")
def download(fname: str):
    return send_from_directory(OUT_DIR, fname, as_attachment=True)

if __name__ == "__main__":
    ensure_dirs()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
