import json
import logging
import os
import sys
import time
from pathlib import Path

from flask import Flask, g, render_template, request, send_from_directory
from flask import request as _request

# asegurar que el paquete core sea visible
sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.excel_reports import generar_reporte
from core.pdf_reports import generar_pdf
from core.utils import OUT_DIR, ensure_dirs

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/")
def index():
    try:
        formato = request.form.get("formato", "excel")
        demo = request.form.get("demo", "0") == "1"

        ensure_dirs()

        # CSV de entrada (demo o upload)
        if demo:
            import pandas as pd

            df = pd.DataFrame(
                [
                    {"categoria": "Ventas", "monto": 1200},
                    {"categoria": "Marketing", "monto": 300},
                    {"categoria": "Operaciones", "monto": 700},
                ]
            )
            csv_path = OUT_DIR / "demo.csv"
            df.to_csv(csv_path, index=False, encoding="utf-8")
        else:
            f = request.files.get("file")
            if not f or not f.filename:
                return render_template(
                    "index.html", error="Sube un archivo .csv o usa el botâ”œâ”‚n de demo."
                )
            csv_path = OUT_DIR / "upload.csv"
            f.save(str(csv_path))
        # --- Normalizar y validar columnas requeridas para reportes ---
        import pandas as pd

        try:
            if Path(csv_path).suffix.lower() in (".xlsx", ".xls"):
                df_in = pd.read_excel(csv_path, engine="openpyxl")
            else:
                try:
                    # Autodetecta separador (;, , \t). engine=python para sep=None
                    df_in = pd.read_csv(csv_path, sep=None, engine="python", encoding="utf-8")
                except Exception:
                    # Fallback comâ”œâ•‘n en ES: punto y coma
                    df_in = pd.read_csv(csv_path, sep=";", engine="python", encoding="utf-8")
        except Exception:
            # Si todo falla, intento final como Excel por si la extensiâ”œâ”‚n engaâ”œâ–’a
            df_in = pd.read_excel(csv_path, engine="openpyxl")

        # Validaciâ”œâ”‚n case-insensitive
        cols_lower = [str(c).lower() for c in df_in.columns]
        required = {"categoria", "monto"}
        if not required.issubset(set(cols_lower)):
            return render_template("index.html", error="debe tener columnas 'categoria' y 'monto'")

        # Renombrar a minâ”œâ•‘sculas para uso consistente y persistir CSV normalizado
        df_in.columns = cols_lower
        norm_csv = OUT_DIR / "norm.csv"
        df_in.to_csv(norm_csv, index=False, encoding="utf-8")
        csv_path = norm_csv
        excel_name = None
        pdf_name = None

        if formato in ("excel", "ambos"):
            xlsx = generar_reporte(csv_path)
            excel_name = os.path.basename(xlsx)

        if formato in ("pdf", "ambos"):
            pdf = generar_pdf(csv_path)
            pdf_name = os.path.basename(pdf)

        return render_template("result.html", excel=excel_name, pdf=pdf_name)
    except Exception as e:
        # Log en consola para que PyTest lo capture
        import sys
        import traceback

        print("!! ERROR en POST /:", e, file=sys.stderr)
        traceback.print_exc()
        return render_template("index.html", error=f"Error procesando el reporte: {e}")


@app.get("/download/<path:fname>")
def download(fname: str):
    # Sirve archivos generados en OUT_DIR (Render usa /tmp/salida)
    return send_from_directory(str(OUT_DIR), fname, as_attachment=True)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}, 200


@app.get("/debugz")
def debugz():
    try:
        ensure_dirs()
        files = sorted([p.name for p in OUT_DIR.glob("*")])
        return {
            "OUT_DIR": str(OUT_DIR),
            "exists": OUT_DIR.exists(),
            "is_dir": OUT_DIR.is_dir(),
            "files": files,
            "cwd": os.getcwd(),
            "env_OUTPUT_DIR": os.environ.get("OUTPUT_DIR"),
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    ensure_dirs()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)


# === JSON logging + request timing ===
class JsonFormatter(logging.Formatter):
    def format(self, record):
        data = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        return json.dumps(data, ensure_ascii=False)


_root = logging.getLogger()
if not _root.handlers:
    logging.basicConfig(level=logging.INFO)
for h in _root.handlers:
    try:
        h.setFormatter(JsonFormatter())
    except Exception:
        pass


@app.before_request
def _start_timer():
    g._t0 = time.time()


@app.after_request
def _log_request(resp):
    try:
        dt = (time.time() - getattr(g, "_t0", time.time())) * 1000.0
        logging.getLogger("request").info(
            f"{_request.method} {_request.path} -> {resp.status_code} ({dt:.1f} ms)"
        )
    except Exception:
        pass
    return resp
