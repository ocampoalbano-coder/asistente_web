# Mercury AI — Estado General del Proyecto

## 🎯 Objetivo
Construir un **asistente web** que:
- Procese archivos CSV/XLSX con ventas/gastos.
- Valide y limpie datos (columnas requeridas: categoria, monto).
- Genere reportes en **Excel** y **PDF** automáticamente.
- Se ejecute vía **interfaz web Flask**, CLI y futuro despliegue en la nube.

---

## ✅ Avances realizados

### Nivel 1 — MVP funcional
- Flask app con subida de CSV/XLSX.
- Validación de columnas obligatorias.
- Botón **"Usar demo"** con dataset precargado.
- Generación de Excel (OpenPyXL) y PDF (ReportLab).
- Descarga de archivos lista (enlace directo en UI).
- Soporte básico a UTF-8 y favicon agregado.

**Estado:** 100% operativo en local.

---

### Nivel 2 — Testing
- Suite de pruebas con **pytest**:
  - Demo Excel y PDF generados sin errores.
  - Validación de columnas inválidas (categoria, monto).
  - Manejo de uploads corruptos / inválidos.
- Se configuró pytest.ini para rutas y ejecución simplificada.
- Todos los tests **pasan**.

**Cobertura:** ~51% (falta ampliar en módulos core).

---

### Nivel 3 — Calidad de código
- **Ruff + Black** configurados en pyproject.toml.
- **Pre-commit hooks** (.pre-commit-config.yaml) activos → evitan subir código mal formateado.
- **CI en GitHub Actions** (.github/workflows/ci.yml):
  - Corre linting, formateo y tests en cada push/PR.
- Repositorio limpio: uff check . --fix y lack . aplicados.
- Warnings de CRLF ↔ LF documentados (normal en Windows).

**Estado:** 100% implementado.

---

## 📊 Estado técnico actual
- **Cobertura:** 51% (core auxiliar sin testear).
- **Directorio /salida:** genera reportes válidos.
- **CLI auxiliar:** ya testeado (eporte-demo en PowerShell).
- **Repo Git:** commits atómicos con mensajes claros.

---

## ⏭️ Próximos niveles

### Nivel 4 — Despliegue
- Hosting gratuito (Render / Railway / PythonAnywhere).
- Crear Procfile con gunicorn o waitress.
- Revisar equirements.txt para producción.
- Variable de entorno PORT soportada (listo en Flask).

### Nivel 5 — Extras
- Empaquetado CLI con pyinstaller.
- Kill-switch/licencias para SaaS.
- Módulos avanzados de core/:
  - outer.py: enrutar comandos.
  - extract_entities.py: NER + reglas YAML.
  - docs_reader.py: leer PDF/DOCX.
- Ampliar tests a estos módulos.
- Mejorar cobertura al **80%+**.

---

## 📂 Estructura del proyecto (simplificada)



---

## 📌 Hitos alcanzados
- [x] MVP con generación de reportes.
- [x] Interfaz web con modo demo.
- [x] Suite de tests con validaciones.
- [x] Integración continua (CI).
- [x] Lint + formato automatizados.
- [ ] Despliegue en hosting.
- [ ] Cobertura 80%+.
- [ ] Kill-switch/licencias.
- [ ] CLI empaquetado.

---

## 🚀 Conclusión
Mercury AI ya es **usable en local**, tiene **tests confiables**, y el código está bajo estándares de calidad con CI automático.  
Lo inmediato es **Nivel 4: despliegue en la nube** → ahí empieza a ser accesible para terceros sin instalar nada.

## Calidad & Tests
Ver [README_TESTING.md](README_TESTING.md) para estado de tests y cobertura.

