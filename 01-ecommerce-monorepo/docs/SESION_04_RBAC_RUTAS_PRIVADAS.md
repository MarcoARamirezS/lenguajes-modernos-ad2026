# Sesión 04 — RBAC y rutas privadas

[← Proyecto](../README.md) · [Índice](./README.md)

> Este documento fue restaurado porque el README del repositorio original hacía referencia a la Sesión 04, pero el archivo no estaba incluido en el ZIP recibido.

## Objetivo

Extender la autenticación JWT de la Sesión 03 para diferenciar permisos por rol y proteger operaciones sensibles.

## Roles sugeridos

```text
admin
customer
```

## Flujo

```text
Login
  ↓
JWT
  ↓
auth middleware
  ↓
req.user
  ↓
requireRole(...)
  ↓
controller
```

## Ejemplo conceptual de middleware

```js
export function requireRole(...roles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        error: 'Authentication required',
      })
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        error: 'Insufficient permissions',
      })
    }

    next()
  }
}
```

## Aplicación

```js
router.post(
  '/products',
  authenticate,
  requireRole('admin'),
  createProduct,
)
```

## Validaciones

- Sin JWT → `401`.
- JWT válido sin permiso → `403`.
- Admin → acceso a operación protegida.
- El rol se obtiene del usuario autenticado; no debe confiarse en un rol enviado por el cliente.

## Commit sugerido

```bash
git add .
git commit -m "feat: add RBAC and private routes"
```

## Continuar

[Sesión 05 — Categories](./SESION_05_CATEGORIES_CATALOGO.md)
