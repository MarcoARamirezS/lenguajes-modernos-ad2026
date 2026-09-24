[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 02](./SESION_02_BACKEND_PYTHON_ARQUITECTURA.md) · [Sesión 04 →](./SESION_04_ACADEMIC_CORE.md)

# Sesión 03 — Firebase Functions + Firestore + Emulators

**Duración:** 1 hora 30 minutos.

## Objetivo

Ejecutar la API Python como función HTTP y conectarla a Firestore.

## Distribución de tiempo

```text
00–20  Firebase project
20–40  firebase.json
40–60  HTTP Function
60–75  Firestore
75–85  Emulators
85–90  commit
```


## Inicialización

```bash
firebase init functions firestore emulators
```

Seleccionar Python para Functions y usar `apps/api` como source si la CLI lo permite directamente; de lo contrario ajustar `firebase.json`.

## `firebase.json`

```json
{
  "functions": {
    "source": "apps/api",
    "runtime": "python311"
  },
  "firestore": {
    "rules": "firebase/firestore.rules",
    "indexes": "firebase/firestore.indexes.json"
  },
  "emulators": {
    "auth": { "port": 9099 },
    "functions": { "port": 5001 },
    "firestore": { "port": 8080 },
    "ui": { "enabled": true, "port": 4000 }
  }
}
```

## `main.py`

```python
from firebase_admin import initialize_app
from firebase_functions import https_fn
from src.http.app import create_app

initialize_app()
app = create_app()

@https_fn.on_request(region="us-central1")
def api(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()
```

## Ejecutar

```bash
firebase emulators:start
```

Probar:

```text
http://127.0.0.1:5001/PROJECT_ID/us-central1/api/health
```


## Cierre verificable

- [ ] Emulator UI abre en `:4000`.
- [ ] Firestore Emulator abre en `:8080`.
- [ ] Function `api` responde.
- [ ] `/health` funciona a través de Firebase Functions.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 02](./SESION_02_BACKEND_PYTHON_ARQUITECTURA.md) · [Sesión 04 →](./SESION_04_ACADEMIC_CORE.md)
