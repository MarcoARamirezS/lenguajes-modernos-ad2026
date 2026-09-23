# Sesión 07 — Firebase Authentication y RBAC

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Autenticar usuarios con Firebase en Nuxt, verificar Firebase ID Tokens en FastAPI y aplicar roles en backend.

## Resultado esperado

Una ruta protegida devuelve 401 sin token, 403 sin permiso y 200 con usuario autorizado.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–15 | Flujo token |
| 15–30 | Firebase Auth cliente |
| 30–50 | Verify ID Token |
| 50–65 | Dependency current_user |
| 65–78 | RBAC |
| 78–90 | Pruebas 401/403/200 |

## Flujo

```text
Nuxt login
  ↓
Firebase Auth
  ↓
ID Token
  ↓
Authorization: Bearer ...
  ↓
FastAPI
  ↓
firebase_admin.auth.verify_id_token
```

## Roles

```text
ADMIN
COORDINATOR
VIEWER
```

## `app/core/security.py`

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth

security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    try:
        return auth.verify_id_token(credentials.credentials)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


def require_roles(*roles: str):
    def dependency(user: dict = Depends(get_current_user)) -> dict:
        role = user.get("role", "VIEWER")
        if role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user
    return dependency
```

## Claims

Para el ejercicio, el profesor puede asignar custom claims desde un script administrativo controlado. Nunca dar al cliente capacidad de asignarse su propio rol.

## Matriz

| Acción | ADMIN | COORDINATOR | VIEWER |
| --- | --- | --- | --- |
| Ver catálogos | Sí | Sí | Sí |
| Editar catálogos | Sí | Sí | No |
| Generar horario | Sí | Sí | No |
| Publicar horario | Sí | No | No |
| Administrar usuarios | Sí | No | No |

## Frontend

`useApi()` ya agrega el Firebase ID Token; ahora las pantallas pueden comenzar a consumir rutas protegidas.


## Cierre de sesión

```bash
git status
git add .
git commit -m "feat: implement Firebase auth and RBAC"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
