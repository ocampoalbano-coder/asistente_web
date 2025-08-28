from pathlib import Path

import yaml

from . import docs_reader, excel_reports, extract_entities

RULES = yaml.safe_load(
    (Path(__file__).resolve().parents[1] / "config" / "rules.yaml").read_text(encoding="utf-8")
)


def route(command: str):
    cmd = command.lower()
    if any(k in cmd for k in RULES["router"]["reporte"]):
        csv = _first_path_like(cmd, [".csv", ".xlsx"])
        if not csv:
            return "ðŸ”Ž Decime el archivo CSV/XLSX, ej: data/ventas.csv"
        out = excel_reports.generar_reporte(csv)
        return f"âœ… Reporte generado: {out}"
    if any(k in cmd for k in RULES["router"]["extraer"]):
        path = _first_path_like(cmd, [".pdf", ".docx", ".txt"])
        if not path:
            return "ðŸ”Ž Decime el archivo (PDF/DOCX/TXT) del que extraigo entidades."
        text = docs_reader.read_text(path)
        outs = extract_entities.extract_to_excel(text)
        return f"âœ… Entidades extraÃ­das â†’ Excel: {outs['excel']} | JSON: {outs['json']}"
    return "ðŸ¤– No entendÃ­ la intenciÃ³n. ProbÃ¡ con 'reporte ... ventas.csv' o 'extraer ... contrato.pdf'."


def _first_path_like(text: str, exts: list[str]):
    tokens = [t.strip(",.;:") for t in text.split()]
    for t in tokens:
        if any(t.endswith(ext) for ext in exts):
            p = Path(t)
            if p.exists():
                return p
    return None
