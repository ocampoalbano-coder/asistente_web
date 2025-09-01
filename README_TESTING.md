# 🧪 Guía de Testing – Mercury AI
Fecha: 2025-09-01 00:38

## Cómo correr los tests
### Rápido
pytest -q

### Con cobertura
pytest --cov=web_flask --cov=core

## Resultado actual
\\\
.....                                                                    [100%] =============================== tests coverage ================================ _______________ coverage: platform win32, python 3.13.3-final-0 _______________  Name                       Stmts   Miss  Cover ---------------------------------------------- core\__init__.py               0      0   100% core\docs_reader.py           20     20     0% core\excel_reports.py         19      3    84% core\extract_entities.py      42     42     0% core\pdf_reports.py           31      3    90% core\router.py                28     28     0% core\utils.py                 15      2    87% web_flask\__init__.py          0      0   100% web_flask\app.py              65      9    86% ---------------------------------------------- TOTAL                        220    107    51% 5 passed in 2.12s
\\\

## Próximos pasos sugeridos
1) Agregar tests a **core/docs_reader.py**, **core/extract_entities.py** y **core/router.py**.
2) Subir cobertura global a **≥ 70%**.
3) Tests de integración (subida CSV → genera Excel/PDF y descarga).
