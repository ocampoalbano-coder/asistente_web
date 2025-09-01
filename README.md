[![CI](https://github.com/ocampoalbano-coder/asistente_web/actions/workflows/ci.yml/badge.svg)] ![Coverage](https://img.shields.io/badge/coverage-64%25-yellow)(https://github.com/ocampoalbano-coder/asistente_web/actions/workflows/ci.yml)

# Mercury AI — Avance hasta Nivel 3

## Estado
- ✅ **Nivel 1:** MVP funcional (Flask + generación de Excel/PDF).
- ✅ **Nivel 2:** Suite de tests en pytest (casos básicos cubiertos).
- ✅ **Nivel 3:** Calidad de código integrada:
  - ruff + black para lint/format
  - pre-commit hooks activos
  - CI en GitHub Actions (tests + lint en cada push)

**Cobertura actual:** ~51% (falta ampliar en módulos core auxiliares).

### Archivos claves añadidos
- pyproject.toml
- pytest.ini
- .pre-commit-config.yaml
- .github/workflows/ci.yml

## Próximos pasos (Nivel 4)
- Despliegue gratuito (Render/Railway/PythonAnywhere) usando Gunicorn.
- Ajustes de producción (Procfile listo, requirements verificados).
- Opcional: empaquetar CLI y subir cobertura de tests (router/extract_entities/docs_reader).


