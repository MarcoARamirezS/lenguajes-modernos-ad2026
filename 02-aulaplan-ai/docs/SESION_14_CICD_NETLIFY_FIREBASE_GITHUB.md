[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 13](./SESION_13_TESTING_QA.md) · [Referencias →](./99_REFERENCIAS_OFICIALES.md)

# Sesión 14 — CI/CD: GitHub + Netlify + Firebase

**Duración:** 1 hora 30 minutos.

## Objetivo

Desplegar el frontend y el backend Python desde el mismo repositorio con pipelines separados y rutas unificadas.

## Distribución de tiempo

```text
00–15  deployment architecture
15–35  Netlify
35–55  Firebase Functions
55–70  proxy /api
70–85  GitHub Actions
85–90  smoke test
```


## Frontend Netlify

`netlify.toml`:

```toml
[build]
  command = "npm run generate --workspace apps/web"
  publish = "apps/web/.output/public"

[[redirects]]
  from = "/api/*"
  to = "https://us-central1-PROJECT_ID.cloudfunctions.net/api/:splat"
  status = 200
  force = true

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## Backend Firebase

```bash
firebase deploy --only functions
```

## Firestore

```bash
firebase deploy --only firestore
```

## GitHub Actions backend

Ejemplo conceptual:

```yaml
name: backend-ci

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r apps/api/requirements.txt
      - run: pytest apps/api/tests -q
```

## Producción

Validar:

```text
https://TU-SITIO.netlify.app/
https://TU-SITIO.netlify.app/api/health
```

El segundo endpoint entra por Netlify y termina en la función Python.


## Cierre verificable

- [ ] web desplegada en Netlify.
- [ ] function Python desplegada en Firebase.
- [ ] `/api/health` funciona desde dominio Netlify.
- [ ] CI backend verde.
- [ ] secrets fuera de GitHub repo.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 13](./SESION_13_TESTING_QA.md) · [Referencias →](./99_REFERENCIAS_OFICIALES.md)
