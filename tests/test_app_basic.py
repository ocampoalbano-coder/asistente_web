import io
import re

import pandas as pd

from web_flask.app import app as flask_app


def _has_magic(data: bytes, magic: bytes) -> bool:
    return data.startswith(magic)


def test_home_ok():
    client = flask_app.test_client()
    r = client.get("/")
    assert r.status_code == 200
    assert b"Generar reporte" in r.data


def test_demo_excel_y_pdf():
    client = flask_app.test_client()
    r = client.post("/", data={"formato": "ambos", "demo": "1"})
    assert r.status_code == 200
    # Extraer links de descarga
    hrefs = re.findall(rb'href="(/download/[^"]+)"', r.data)
    assert len(hrefs) >= 2, "Debería ofrecer Excel y PDF"

    # Descargar y verificar firmas
    excel_path = hrefs[0].decode()
    pdf_path = hrefs[1].decode()

    rx = client.get(excel_path)
    assert rx.status_code == 200
    # XLSX es ZIP => empieza con 'PK'
    assert _has_magic(rx.data, b"PK"), "El XLSX no parece ZIP válido"

    rp = client.get(pdf_path)
    assert rp.status_code == 200
    assert _has_magic(rp.data, b"%PDF"), "El PDF no empieza con %PDF"


def test_upload_csv_valido_excel():
    client = flask_app.test_client()
    # CSV en memoria
    csv = "id,categoria,monto\n1,Software,100\n2,Servicios,50\n"
    data = {
        "formato": "excel",
        "file": (io.BytesIO(csv.encode("utf-8")), "ventas.csv"),
    }
    r = client.post("/", data=data, content_type="multipart/form-data")
    assert r.status_code == 200
    m = re.search(rb'href="(/download/[^"]+\.xlsx)"', r.data)
    assert m, "No se encontró link de Excel"
    rx = client.get(m.group(1).decode())
    assert rx.status_code == 200
    assert rx.data.startswith(b"PK")


def test_upload_xlsx_valido_pdf():
    client = flask_app.test_client()
    # Crear un XLSX en memoria con pandas
    buf = io.BytesIO()
    df = pd.DataFrame(
        [
            {"id": 1, "categoria": "Marketing", "monto": 200},
            {"id": 2, "categoria": "Software", "monto": 70},
        ]
    )
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    buf.seek(0)

    data = {
        "formato": "pdf",
        "file": (buf, "ventas.xlsx"),
    }
    r = client.post("/", data=data, content_type="multipart/form-data")
    assert r.status_code == 200
    m = re.search(rb'href="(/download/[^"]+\.pdf)"', r.data)
    assert m, "No se encontró link de PDF"
    rp = client.get(m.group(1).decode())
    assert rp.status_code == 200
    assert rp.data.startswith(b"%PDF")


def test_error_columnas_invalidas():
    client = flask_app.test_client()
    csv = "id,foo,bar\n1,a,2\n"
    data = {
        "formato": "excel",
        "file": (io.BytesIO(csv.encode("utf-8")), "mal.csv"),
    }
    r = client.post("/", data=data, content_type="multipart/form-data")
    assert r.status_code == 200
    assert b"debe tener columnas 'categoria' y 'monto'" in r.data
