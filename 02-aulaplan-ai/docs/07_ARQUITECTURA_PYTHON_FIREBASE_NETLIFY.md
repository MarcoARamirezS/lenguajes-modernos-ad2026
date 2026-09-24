[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Contrato API](./06_CONTRATO_API.md) · [Variables y seguridad →](./08_VARIABLES_ENTORNO_Y_SEGURIDAD.md)

# 07 — Arquitectura Python + Firebase + Netlify

## Decisión

El backend **sí es Python**.

## Restricción técnica

Netlify no ofrece runtime Python para Netlify Functions modernas. Python en Netlify está disponible para tareas del entorno de build, lo cual no equivale a ejecutar una API Python.

## Solución

```text
GitHub monorepo
       │
       ├── apps/web ──────────────► Netlify
       │                              │
       │                              └── /api/*
       │                                  │ proxy
       │                                  ▼
       └── apps/api ──────────────► Firebase Functions
                                      Python
                                        │
                                        ▼
                                  Firebase Admin
                                  Firestore/Auth
```

## Por qué Firebase Functions

Firebase soporta funciones escritas en Python y permite funciones HTTP con GET, POST, PUT, DELETE y OPTIONS.

## Función única de API

Se usa una HTTP Function llamada `api` que delega a Flask.

`apps/api/main.py`:

```python
from firebase_admin import initialize_app
from firebase_functions import https_fn
from src.http.app import create_app

initialize_app()
flask_app = create_app()

@https_fn.on_request(region="us-central1")
def api(req: https_fn.Request) -> https_fn.Response:
    with flask_app.request_context(req.environ):
        return flask_app.full_dispatch_request()
```

## Proxy de Netlify

`netlify.toml`:

```toml
[[redirects]]
  from = "/api/*"
  to = "https://us-central1-PROJECT_ID.cloudfunctions.net/api/:splat"
  status = 200
  force = true
```

Así el frontend usa `/api` sin conocer el dominio de Cloud Functions.

## Conclusión

No existe una variante técnicamente correcta que simultáneamente use:

```text
backend Python real
+
runtime de backend exclusivamente Netlify Functions
```

La guía prioriza Python y mantiene Netlify como front y gateway visible.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Contrato API](./06_CONTRATO_API.md) · [Variables y seguridad →](./08_VARIABLES_ENTORNO_Y_SEGURIDAD.md)
