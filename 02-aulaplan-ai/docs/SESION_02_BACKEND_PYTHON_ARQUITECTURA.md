[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 01](./SESION_01_FOUNDATION_MONOREPO_PYTHON.md) · [Sesión 03 →](./SESION_03_FIREBASE_FUNCTIONS_FIRESTORE.md)

# Sesión 02 — Arquitectura backend Python

**Duración:** 1 hora 30 minutos.

## Objetivo

Construir una API Python modular y probar `/health`.

## Distribución de tiempo

```text
00–20  Python aplicado a backend
20–40  Flask + Pydantic
40–65  Arquitectura por capas
65–80  Health endpoint
80–90  Prueba y commit
```


## Estructura

```text
apps/api/
├── main.py
├── requirements.txt
└── src/
    ├── core/
    ├── http/
    │   ├── app.py
    │   └── routes/
    ├── repositories/
    ├── schemas/
    └── services/
```

## Flask app

`src/http/app.py`:

```python
from flask import Flask, jsonify

def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify({
            "status": "ok",
            "service": "aulaplan-api",
            "runtime": "python",
        })

    return app
```

## Principio

```text
HTTP route
  ↓
Pydantic schema
  ↓
Service
  ↓
Repository
  ↓
Firestore
```

El route no contiene reglas de negocio.


## Cierre verificable

- [ ] Existe `create_app()`.
- [ ] `/health` devuelve JSON.
- [ ] Carpetas de arquitectura creadas.
- [ ] No hay acceso a Firestore dentro del route.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 01](./SESION_01_FOUNDATION_MONOREPO_PYTHON.md) · [Sesión 03 →](./SESION_03_FIREBASE_FUNCTIONS_FIRESTORE.md)
