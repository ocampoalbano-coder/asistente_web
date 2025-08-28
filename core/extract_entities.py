import json
import re
from pathlib import Path

import yaml

try:
    import spacy

    NLP = spacy.load("es_core_news_md")
except Exception:
    NLP = None

from .utils import ensure_dirs, stamp


def _load_rules():
    rules = yaml.safe_load(
        (Path(__file__).resolve().parents[1] / "config" / "rules.yaml").read_text(encoding="utf-8")
    )
    ents = rules.get("entities", {})
    compiled = {k: re.compile(v, re.IGNORECASE) for k, v in ents.items()}
    return compiled


def extract_from_text(text: str):
    rules = _load_rules()
    found = {k: set() for k in rules.keys()}
    for kind, rgx in rules.items():
        for m in rgx.finditer(text):
            val = (m.group(1) if m.groups() else m.group(0)).strip()
            if val:
                found[kind].add(val)
    if NLP:
        doc = NLP(text)
        for ent in doc.ents:
            if ent.label_ in ("PER", "ORG"):
                kind = "contacto" if ent.label_ == "PER" else "empresa"
                found.setdefault(kind, set()).add(ent.text.strip())
    cleaned = {k: sorted(list(v)) for k, v in found.items()}
    return cleaned


def extract_to_excel(text: str):
    import pandas as pd

    ensure_dirs()
    ents = extract_from_text(text)
    writer_path = stamp("entidades", "xlsx")
    with pd.ExcelWriter(writer_path, engine="openpyxl") as writer:
        for kind, items in ents.items():
            pd.DataFrame({"valor": items}).to_excel(
                writer, index=False, sheet_name=(kind[:31] or "items")
            )
    out_json = stamp("entidades", "json")
    Path(out_json).write_text(json.dumps(ents, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"excel": writer_path, "json": out_json}
