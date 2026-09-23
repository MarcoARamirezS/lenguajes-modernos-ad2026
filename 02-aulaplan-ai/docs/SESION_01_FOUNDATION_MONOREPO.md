# Sesión 01 — Foundation del monorepo

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Crear desde cero el repositorio técnico `aulaplan-ai`, instalar Nuxt 4 y FastAPI, establecer la estructura común y dejar ambos procesos ejecutándose.

## Resultado esperado

`http://localhost:3000` responde con Nuxt y `http://127.0.0.1:8000/docs` muestra Swagger.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–15 | Arquitectura y objetivo |
| 15–35 | Prerrequisitos y monorepo |
| 35–55 | Nuxt 4 |
| 55–75 | Python, venv y FastAPI |
| 75–85 | Health endpoint |
| 85–90 | Git y verificación |

## 1. Crear el proyecto

Seguir primero [`01_INSTALACION_Y_EJECUCION.md`](./01_INSTALACION_Y_EJECUCION.md).

## 2. `package.json` raíz

Dejar una raíz enfocada en el frontend npm; Python mantiene su propio entorno:

```json
{
  "name": "aulaplan-ai",
  "version": "0.1.0",
  "private": true,
  "workspaces": ["apps/web"],
  "scripts": {
    "dev:web": "npm run dev --workspace apps/web",
    "build:web": "npm run build --workspace apps/web",
    "generate:web": "npm run generate --workspace apps/web"
  },
  "engines": {
    "node": ">=24"
  }
}
```

## 3. `.gitignore`

```gitignore
node_modules/
.nuxt/
.output/
.env
.env.*
!.env.example
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
coverage/
htmlcov/
playwright-report/
test-results/
.DS_Store
service-account*.json
firebase-adminsdk*.json
```

## 4. Primer FastAPI

Crear `apps/api/app/__init__.py` vacío.

Crear `apps/api/app/main.py`:

```python
from fastapi import FastAPI

app = FastAPI(title="AulaPlan AI API", version="0.1.0")


@app.get("/api/v1/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "aulaplan-api"}
```

## 5. Ejecutar API

### macOS / Linux

```bash
cd apps/api
source .venv/bin/activate
fastapi dev app/main.py
```

### Windows PowerShell

```powershell
cd apps/api
.\.venv\Scripts\Activate.ps1
fastapi dev app/main.py
```

## 6. Prueba

```bash
curl http://127.0.0.1:8000/api/v1/health
```

Esperado:

```json
{"status":"ok","service":"aulaplan-api"}
```

## 7. Frontend

Aplicar la entrega de [`02_FRONTEND_NUXT4_ENTREGA_UNICA.md`](./02_FRONTEND_NUXT4_ENTREGA_UNICA.md).

## Evidencia

- Nuxt visible.
- Swagger visible.
- Health 200.


## Cierre de sesión

```bash
git status
git add .
git commit -m "chore: initialize AulaPlan AI monorepo"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
