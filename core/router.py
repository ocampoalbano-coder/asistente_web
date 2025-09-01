from pathlib import Path

import yaml

# --- parche: sanear YAML para quitar BOM y caracteres de control ---
try:
    import re as _re

    _yaml_safe_load_orig = yaml.safe_load

    def yaml_safe_load_sanitized(data, *a, **k):
        # Decodificar bytes ignorando errores
        if isinstance(data, bytes | bytearray):
            try:
                data = bytes(data).decode("utf-8", errors="ignore")
            except Exception:
                data = str(data)
        # Quitar BOM y caracteres de control no imprimibles
        if isinstance(data, str):
            data = data.lstrip("\ufeff")
            data = _re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]", "", data)
        return _yaml_safe_load_orig(data, *a, **k)

    yaml.safe_load = yaml_safe_load_sanitized
except Exception:
    # En caso de cualquier problema, seguimos con el safe_load normal
    pass
# --- fin parche ---
from . import docs_reader, excel_reports, extract_entities

RULES = yaml.safe_load(
    (Path(__file__).resolve().parents[1] / "config" / "rules.yaml").read_text(encoding="utf-8")
)


def route(command: str):
    cmd = command.lower()
    if any(k in cmd for k in RULES["router"]["reporte"]):
        csv = _first_path_like(cmd, [".csv", ".xlsx"])
        if not csv:
            return "Ã°Å¸â€Å½ Decime el archivo CSV/XLSX, ej: data/ventas.csv"
        out = excel_reports.generar_reporte(csv)
        return f"Ã¢Å“â€¦ Reporte generado: {out}"
    if any(k in cmd for k in RULES["router"]["extraer"]):
        path = _first_path_like(cmd, [".pdf", ".docx", ".txt"])
        if not path:
            return "Ã°Å¸â€Å½ Decime el archivo (PDF/DOCX/TXT) del que extraigo entidades."
        text = docs_reader.read_text(path)
        outs = extract_entities.extract_to_excel(text)
        return (
            f"Ã¢Å“â€¦ Entidades extraÃƒÂ­das Ã¢â€ â€™ Excel: {outs['excel']} | JSON: {outs['json']}"
        )
    return "Ã°Å¸Â¤â€“ No entendÃƒÂ­ la intenciÃƒÂ³n. ProbÃƒÂ¡ con 'reporte ... ventas.csv' o 'extraer ... contrato.pdf'."


def _first_path_like(text: str, exts: list[str]):
    tokens = [t.strip(",.;:") for t in text.split()]
    for t in tokens:
        if any(t.endswith(ext) for ext in exts):
            p = Path(t)
            if p.exists():
                return p
    return None
