[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Mapa backend](./12_MAPA_SESIONES_BACKEND.md) · [Sesión 02 →](./SESION_02_FIREBASE_FUNCTIONS_FIRESTORE.md)

# Sesión 01 — Python Foundation

**Duración:** 1 h 30 min  
**Objetivo:** crear la base Python del backend, una aplicación Flask mínima y su primera prueba automatizada.

## Distribución

```text
00–15  Repaso de Python aplicado a backend
15–30  Entorno virtual y dependencias
30–50  Estructura src/
50–70  Flask + health
70–82  pytest
82–90  commit y cierre
```

## 1. Entrar al backend

### macOS/Linux

```bash
cd apps/api
source .venv/bin/activate
python --version
```

### Windows PowerShell

```powershell
cd apps/api
.\.venv\Scripts\Activate.ps1
python --version
```

Debe mostrar `Python 3.11.x`.

## 2. Crear carpetas

### macOS/Linux

```bash
mkdir -p src/core src/http tests
touch src/__init__.py src/core/__init__.py src/http/__init__.py
```

### Windows

```powershell
New-Item -ItemType Directory -Force src/core
New-Item -ItemType Directory -Force src/http
New-Item -ItemType Directory -Force tests
New-Item -ItemType File -Force src/__init__.py
New-Item -ItemType File -Force src/core/__init__.py
New-Item -ItemType File -Force src/http/__init__.py
```

## 3. Dependencias

```bash
pip install Flask pydantic pytest
pip freeze > requirements.txt
```

## 4. Crear health endpoint

### `apps/api/src/http/routes_health.py`

```python
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return jsonify({"status": "ok", "service": "aulaplan-api", "runtime": "python"})
```


## 5. Crear aplicación Flask

En esta primera sesión usa esta versión mínima de `app.py`:

```python
from flask import Flask

from src.http.routes_health import health_bp


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    app.config["TESTING"] = testing
    app.register_blueprint(health_bp)
    return app
```

## 6. Crear prueba

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


## 7. Ejecutar prueba

```bash
PYTHONPATH=. pytest tests -q
```

En Windows PowerShell:

```powershell
$env:PYTHONPATH="."
pytest tests -q
```

Resultado esperado:

```text
1 passed
```

## 8. Probar Flask directamente

Crea temporalmente `dev.py`:

```python
from src.http.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8000)
```

Ejecuta:

```bash
python dev.py
```

Abre `http://127.0.0.1:8000/health`.

## Checklist

- [ ] `.venv` usa Python 3.11.
- [ ] Flask instalado.
- [ ] `/health` responde.
- [ ] pytest verde.
- [ ] No hay Firebase todavía.

## Commit

```bash
git add .
git commit -m "feat: create Python backend foundation"
```

## Árbol al cierre

```text
apps/api/
├── .venv/
├── requirements.txt
├── dev.py
├── src/
│   ├── __init__.py
│   └── http/
│       ├── __init__.py
│       ├── app.py
│       └── routes_health.py
└── tests/
    └── test_app.py
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Mapa backend](./12_MAPA_SESIONES_BACKEND.md) · [Sesión 02 →](./SESION_02_FIREBASE_FUNCTIONS_FIRESTORE.md)
