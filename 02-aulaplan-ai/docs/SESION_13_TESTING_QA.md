# Sesión 13 — Testing y QA

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Crear una pirámide de pruebas para schemas, servicios, API y solver; utilizar emuladores para evitar depender de Firebase productivo.

## Resultado esperado

La suite cubre reglas críticas de conflicto y los endpoints principales pueden ejecutarse automáticamente.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–15 | Estrategia |
| 15–30 | Pytest |
| 30–50 | Solver unit tests |
| 50–65 | API tests |
| 65–78 | Firebase Emulator |
| 78–90 | Playwright smoke |

## Instalar

```bash
pip install pytest pytest-asyncio httpx ruff
```

## Estructura

```text
apps/api/tests/
├── conftest.py
├── unit/
│   ├── test_constraints.py
│   └── test_solver.py
├── integration/
│   └── test_teacher_repository.py
└── api/
    ├── test_health.py
    └── test_schedules.py
```

## Health

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

## Casos obligatorios del solver

- mismo profesor en dos clases;
- mismo grupo en dos clases;
- mismo salón en dos clases;
- capacidad insuficiente;
- tipo de salón incompatible;
- profesor no disponible;
- dataset factible;
- dataset inviable;
- soft constraints no rompen hard constraints.

## Ejecutar

```bash
cd apps/api
pytest -q
ruff check app tests
```

## E2E frontend

Mantener un smoke corto:

```text
login
→ dashboard
→ teachers
→ generator
→ schedules
```

No convertir E2E en sustituto de las pruebas del solver.


## Cierre de sesión

```bash
git status
git add .
git commit -m "test: add backend and scheduling test suite"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
