[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 01](./SESION_01_PYTHON_FOUNDATION.md) · [Sesión 03 →](./SESION_03_CORE_REPOSITORY_ARCHITECTURE.md)

# Sesión 02 — Firebase Functions + Firestore + Emulator Suite

**Duración:** 1 h 30 min  
**Objetivo:** convertir la aplicación Flask en una HTTP Function Python y ejecutar todo localmente con Firebase Emulator Suite.

## Distribución

```text
00–15  Cloud Functions y runtime Python
15–30  Firebase Admin
30–50  main.py
50–65  firebase.json
65–80  Emulator Suite
80–90  prueba y commit
```

## 1. Dependencias

```bash
pip install firebase-functions firebase-admin
pip freeze > requirements.txt
```

## 2. Configuración raíz

### `firebase.json`

```json
{
  "functions": [
    {
      "source": "apps/api",
      "codebase": "aulaplan-api",
      "runtime": "python311",
      "ignore": [".venv", "venv", "__pycache__", "*.pyc", ".git"]
    }
  ],
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


### `.firebaserc`

```text
{
  "projects": {
    "default": "YOUR_FIREBASE_PROJECT_ID"
  }
}
```


## 3. Firestore

### `firebase/firestore.rules`

```text
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```


### `firebase/firestore.indexes.json`

```json
{
  "indexes": [],
  "fieldOverrides": []
}
```


## 4. Función Python

### `apps/api/main.py`

```python
from firebase_admin import get_app, initialize_app
from firebase_functions import https_fn

from src.http.app import create_app

try:
    get_app()
except ValueError:
    initialize_app()

flask_app = create_app()


@https_fn.on_request(
    region="us-central1",
    cors=True,
)
def api(req: https_fn.Request) -> https_fn.Response:
    with flask_app.request_context(req.environ):
        return flask_app.full_dispatch_request()
```


## 5. Ejecutar emuladores

Desde la raíz:

```bash
firebase emulators:start
```

Puertos esperados: Auth `9099`, Functions `5001`, Firestore `8080`, UI `4000`.

## 6. Probar

```bash
curl http://127.0.0.1:5001/PROJECT_ID/us-central1/api/health
```

## Errores frecuentes

- `Failed to load function definition`: revisa `source: apps/api`.
- Error Java: `java --version`, curso estandarizado en Java 21.
- Proyecto incorrecto: `firebase use`.

## Checklist

- [ ] Function Python detectada.
- [ ] Firestore Emulator ejecutándose.
- [ ] Emulator UI disponible.
- [ ] `/health` responde por Functions.

## Commit

```bash
git add .
git commit -m "feat: run Python API on Firebase Functions emulator"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 01](./SESION_01_PYTHON_FOUNDATION.md) · [Sesión 03 →](./SESION_03_CORE_REPOSITORY_ARCHITECTURE.md)
