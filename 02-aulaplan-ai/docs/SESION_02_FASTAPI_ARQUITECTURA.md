# Sesión 02 — FastAPI profesional y arquitectura modular

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Reorganizar el backend por capas, agregar configuración tipada, CORS, router versionado y manejo consistente de errores.

## Resultado esperado

La API inicia desde `app/main.py`, expone `/api/v1/health`, `/api/v1/info` y carga configuración desde `.env`.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–15 | Repaso y arquitectura |
| 15–30 | Settings con Pydantic |
| 30–50 | Routers v1 |
| 50–65 | CORS y app factory |
| 65–80 | Errores y respuestas |
| 80–90 | Swagger y prueba |

## Dependencias

```bash
pip install pydantic-settings
```

## Estructura

```text
apps/api/app/
├── api/v1/
│   ├── __init__.py
│   ├── router.py
│   └── routes/
│       ├── __init__.py
│       └── health.py
├── core/
│   ├── __init__.py
│   └── config.py
└── main.py
```

## `core/config.py`

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AulaPlan AI API"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    cors_origins: str = "http://localhost:3000"
    firebase_project_id: str = ""
    gemini_api_key: str = ""
    gemini_model: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

## `api/v1/routes/health.py`

```python
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "aulaplan-api"}


@router.get("/info")
def info() -> dict[str, str]:
    return {"name": "AulaPlan AI", "api": "v1"}
```

## `api/v1/router.py`

```python
from fastapi import APIRouter
from app.api.v1.routes import health

api_router = APIRouter()
api_router.include_router(health.router)
```

## `main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=settings.api_prefix)
```

## Verificación

```bash
curl http://127.0.0.1:8000/api/v1/info
```

Swagger debe agrupar `health` correctamente.


## Cierre de sesión

```bash
git status
git add .
git commit -m "feat: implement FastAPI modular foundation"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
