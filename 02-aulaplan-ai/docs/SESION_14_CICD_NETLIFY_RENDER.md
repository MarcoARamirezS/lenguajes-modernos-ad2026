# Sesión 14 — CI/CD con GitHub, Netlify y Render

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Automatizar validación de frontend y backend y desplegar ambos componentes desde el mismo repositorio GitHub.

## Resultado esperado

Push a `main` ejecuta CI; Netlify publica Nuxt y Render publica FastAPI con variables de entorno separadas.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–15 | Arquitectura deploy |
| 15–30 | GitHub Actions API |
| 30–45 | GitHub Actions Web |
| 45–60 | Netlify |
| 60–75 | Render |
| 75–85 | Variables/CORS |
| 85–90 | Release v1.0.0 |

## GitHub Actions backend

`.github/workflows/api-ci.yml`:

```yaml
name: API CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: apps/api
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python -m pip install --upgrade pip
      - run: pip install -r requirements-dev.txt
      - run: ruff check app tests
      - run: pytest -q
```

## GitHub Actions frontend

`.github/workflows/web-ci.yml`:

```yaml
name: Web CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '24'
          cache: npm
      - run: npm ci
      - run: npm run generate:web
```

## `netlify.toml`

Desde raíz:

```toml
[build]
  command = "npm run generate:web"
  publish = "apps/web/.output/public"

[build.environment]
  NODE_VERSION = "24"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

Configurar en Netlify las variables `NUXT_PUBLIC_*`.

## Render

Crear Web Service apuntando al mismo repositorio:

```text
Root Directory: apps/api
Language: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Variables mínimas:

```text
APP_ENV=production
CORS_ORIGINS=https://TU-SITIO.netlify.app
FIREBASE_PROJECT_ID=...
GEMINI_API_KEY=...
GEMINI_MODEL=...
```

La credencial Firebase de producción debe configurarse como secreto del proveedor, nunca como archivo versionado.

## Conectar frontend

En Netlify:

```text
NUXT_PUBLIC_API_BASE_URL=https://TU-API.onrender.com/api/v1
```

## Validación final

```text
Netlify /login
  ↓
Firebase Auth
  ↓
Render /api/v1
  ↓
Firestore
  ↓
OR-Tools / Gemini
```

## Release

```bash
git switch main
git pull
git tag -a v1.0.0 -m "AulaPlan AI v1.0.0"
git push origin v1.0.0
```


## Cierre de sesión

```bash
git status
git add .
git commit -m "ci: deploy AulaPlan AI with Netlify and Render"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
