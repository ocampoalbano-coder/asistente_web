from pathlib import Path

from docx import Document
from PyPDF2 import PdfReader


def read_text(path: str | Path) -> str:
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        return _read_pdf(p)
    if p.suffix.lower() in [".docx", ".doc"]:
        return _read_docx(p)
    return p.read_text(encoding="utf-8", errors="ignore")


def _read_pdf(p: Path) -> str:
    text = []
    with open(p, "rb") as f:
        pdf = PdfReader(f)
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)


def _read_docx(p: Path) -> str:
    doc = Document(p)
    return "\n".join(par.text for par in doc.paragraphs)
