[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 06](./SESION_06_AVAILABILITY_CONSTRAINTS.md) · [Sesión 08 →](./SESION_08_SCHEDULING_DOMAIN.md)

# Sesión 07 — Firebase Authentication + RBAC

**Duración:** 1 hora 30 minutos.

## Objetivo

Proteger la API Python mediante Firebase ID tokens y roles.

## Distribución de tiempo

```text
00–20  Auth flow
20–40  verify_id_token
40–60  RBAC
60–75  decorators/helpers
75–85  tests
85–90  commit
```


## Flujo

```text
Nuxt login
 ↓
Firebase Auth
 ↓
ID token
 ↓
Authorization: Bearer <token>
 ↓
Python
 ↓
firebase_admin.auth.verify_id_token()
```

## Roles

```text
ADMIN
COORDINATOR
VIEWER
```

## Helper

```python
from firebase_admin import auth

def verify_bearer_token(header: str | None) -> dict:
    if not header or not header.startswith("Bearer "):
        raise PermissionError("Missing token")

    token = header.removeprefix("Bearer ").strip()
    return auth.verify_id_token(token)
```

El rol debe obtenerse de claims confiables o de un documento de usuario administrado por backend.


## Cierre verificable

- [ ] endpoints públicos mínimos.
- [ ] token ausente → 401.
- [ ] token inválido → 401.
- [ ] rol insuficiente → 403.
- [ ] ADMIN/COORDINATOR pueden modificar catálogos.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 06](./SESION_06_AVAILABILITY_CONSTRAINTS.md) · [Sesión 08 →](./SESION_08_SCHEDULING_DOMAIN.md)
