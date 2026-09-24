[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 14](./SESION_14_SCHEDULE_WORKFLOW_VERSIONING.md) · [Contrato API →](./90_CONTRATO_API.md)

# Sesión 15 — Testing, CI/CD, Firebase y Netlify

**Duración:** 1 h 30 min  
**Objetivo:** validar el proyecto completo y desplegar frontend/backend desde el mismo monorepo.

## Distribución

```text
00–20  suite backend
20–35  frontend typecheck/generate
35–50  GitHub Actions
50–65  Firebase deploy
65–78  Netlify
78–88  smoke tests
88–90  versión v1.0.0
```

## 1. Requirements final

### `apps/api/requirements.txt`

```text
firebase-functions>=0.4.0
firebase-admin>=7.0.0
Flask>=3.1.0
pydantic[email]>=2.11.0
google-genai>=1.0.0
pytest>=8.4.0
```


## 2. Pruebas

### `apps/api/tests/test_app.py`

```python
from src.http.app import create_app


def test_health():
    app = create_app(testing=True)
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["runtime"] == "python"
```


### `apps/api/tests/test_scheduler.py`

```python
from src.scheduler.domain import Group, Offering, Room, SchedulerContext, Subject, Teacher, TimeBlock
from src.scheduler.solver import solve_schedule


def build_context() -> SchedulerContext:
    return SchedulerContext(
        teachers={"t1": Teacher("t1", "Ana", 4, 10)},
        subjects={"s1": Subject("s1", "Programación", 2, "CLASSROOM")},
        groups={"g1": Group("g1", "A", 20)},
        rooms={"r1": Room("r1", "Aula 1", 30, "CLASSROOM")},
        time_blocks={
            "b1": TimeBlock("b1", "MONDAY", "08:00", "09:30", 1),
            "b2": TimeBlock("b2", "TUESDAY", "08:00", "09:30", 1),
        },
        offerings={"o1": Offering("o1", "s1", "g1", "t1", "p1")},
        availability=[],
        constraints=[],
    )


def test_solver_finds_valid_solution():
    result = solve_schedule(build_context(), max_nodes=1000)
    assert result.status == "SOLVED"
    assert len(result.assignments) == 2
    days = {build_context().time_blocks[x.time_block_id].day for x in result.assignments}
    assert len(days) == 2
```


### Ejecutar

macOS/Linux:

```bash
cd apps/api
source .venv/bin/activate
PYTHONPATH=. pytest tests -q
```

Windows:

```powershell
cd apps/api
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH="."
pytest tests -q
```

## 3. Frontend

Desde raíz:

```bash
npm run typecheck:web
npm run generate:web
```

## 4. GitHub Actions

### `.github/workflows/ci.yml`

```yaml
name: ci

on:
  pull_request:
  push:
    branches: [main]

jobs:
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: npm
      - run: npm ci
      - run: npm run typecheck:web
      - run: npm run generate:web

  backend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: apps/api
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip
          cache-dependency-path: apps/api/requirements.txt
      - run: python -m pip install --upgrade pip
      - run: pip install -r requirements.txt
      - run: PYTHONPATH=. pytest tests -q
```


## 5. Netlify

### `netlify.toml`

```toml
[build]
  command = "npm run generate:web"
  publish = "apps/web/.output/public"

[[redirects]]
  from = "/api/*"
  to = "https://us-central1-YOUR_FIREBASE_PROJECT_ID.cloudfunctions.net/api/:splat"
  status = 200
  force = true

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```


Reemplaza `YOUR_FIREBASE_PROJECT_ID`.

Este rewrite mantiene visible:

```text
https://TU-SITIO.netlify.app/api/health
```

pero la petición se ejecuta realmente en Firebase Functions Python.

## 6. Desplegar backend

Firebase Functions requiere que el proyecto tenga la facturación/plan requerido para despliegue de Functions.

```bash
firebase deploy --only functions
firebase deploy --only firestore
```

## 7. Conectar Netlify

1. Importa el repositorio de GitHub.
2. Netlify leerá `netlify.toml`.
3. Agrega las variables `NUXT_PUBLIC_FIREBASE_*`.
4. En producción:

```text
NUXT_PUBLIC_API_BASE_URL=/api
NUXT_PUBLIC_USE_FIREBASE_EMULATORS=false
```

5. Deploy.

## 8. Smoke tests

```text
GET https://TU-SITIO.netlify.app/
GET https://TU-SITIO.netlify.app/api/health
```

Después:

- login;
- abrir profesores;
- crear datos;
- generar horario;
- publicar.

## 9. Tag

```bash
git switch main
git pull
git tag -a v1.0.0 -m "AulaPlan AI v1.0.0"
git push origin v1.0.0
```

## Checklist final

- [ ] backend pytest verde.
- [ ] frontend typecheck verde.
- [ ] frontend generate verde.
- [ ] CI verde.
- [ ] Functions Python desplegadas.
- [ ] Firestore rules desplegadas.
- [ ] Netlify desplegado.
- [ ] `/api/health` responde a través de Netlify.
- [ ] secretos fuera del repo.
- [ ] tag v1.0.0.

## Commit

```bash
git add .
git commit -m "ci: complete AulaPlan production pipeline"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 14](./SESION_14_SCHEDULE_WORKFLOW_VERSIONING.md) · [Contrato API →](./90_CONTRATO_API.md)
