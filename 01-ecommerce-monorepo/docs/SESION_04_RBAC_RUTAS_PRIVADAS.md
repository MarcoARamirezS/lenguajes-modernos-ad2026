# SESIÓN 4 — ROLES + PERMISOS + RBAC + RUTAS PRIVADAS

## Objetivo

Extender la autenticación creada en la Sesión 3 para agregar autorización basada en roles y permisos.

Al terminar tendremos:

```text
JWT válido
   |
   v
authenticate
   |
   v
req.auth
   |
   v
authorize(permission)
   |
   +--> permiso permitido -> controller
   |
   `--> permiso denegado -> 403
```

Esta sesión prepara el middleware `authorize()` que utilizará la Sesión 5 para proteger operaciones de categorías y catálogo.

---

# 1. Diferencia entre autenticación y autorización

## Autenticación

Responde:

```text
¿Quién es el usuario?
```

Se resuelve con:

```text
authenticate.middleware.js
```

## Autorización

Responde:

```text
¿Puede este usuario ejecutar esta operación?
```

Se resolverá con:

```text
authorize.middleware.js
```

---

# 2. Roles iniciales

Trabajaremos con:

```text
CUSTOMER
ADMIN
```

`CUSTOMER` será el rol asignado durante el registro público.

`ADMIN` tendrá permisos administrativos sobre el catálogo.

---

# 3. Catálogo de permisos

Crear:

```text
apps/api/src/config/permissions.js
```

```javascript
export const rolePermissions =
  Object.freeze({
    CUSTOMER: [
      'products:read',
      'categories:read',
      'cart:read',
      'cart:write',
      'orders:create',
      'orders:read-own'
    ],

    ADMIN: [
      'products:read',
      'products:create',
      'products:update',
      'products:delete',
      'categories:read',
      'categories:create',
      'categories:update',
      'categories:delete',
      'orders:read',
      'users:read'
    ]
  })

export function hasPermission(
  role,
  permission
) {
  return Boolean(
    rolePermissions[role]
      ?.includes(permission)
  )
}
```

Para mantener compatibilidad con las siguientes sesiones, las rutas de categorías podrán reutilizar temporalmente los permisos `products:create`, `products:update` y `products:delete`, o evolucionar después hacia permisos específicos de categorías.

---

# 4. Middleware authorize

Crear:

```text
apps/api/src/shared/middleware/authorize.middleware.js
```

```javascript
import {
  AppError
} from '../errors/app-error.js'

import {
  hasPermission
} from '../../config/permissions.js'

export function authorize(
  permission
) {
  return function authorizationMiddleware(
    req,
    _res,
    next
  ) {
    if (!req.auth) {
      return next(
        new AppError({
          statusCode: 401,
          code: 'AUTH_REQUIRED',
          message: 'Autenticación requerida'
        })
      )
    }

    if (
      !hasPermission(
        req.auth.role,
        permission
      )
    ) {
      return next(
        new AppError({
          statusCode: 403,
          code: 'FORBIDDEN',
          message: 'No tienes permisos para realizar esta operación'
        })
      )
    }

    return next()
  }
}
```

---

# 5. Orden correcto de middlewares

Una ruta privada debe mantener este orden:

```text
authenticate
    |
    v
authorize
    |
    v
validate
    |
    v
controller
```

Ejemplo:

```javascript
router.post(
  '/',
  authenticate,
  authorize(
    'products:create'
  ),
  validate(
    createProductSchema
  ),
  asyncHandler(
    createProduct
  )
)
```

Nunca ejecutar `authorize()` antes de `authenticate`, porque `req.auth` todavía no existiría.

---

# 6. Proteger Products

Modificar las rutas de escritura del módulo Products.

Ejemplo esperado:

```javascript
router.post(
  '/',
  authenticate,
  authorize(
    'products:create'
  ),
  validate(
    createProductSchema
  ),
  asyncHandler(
    createProduct
  )
)

router.patch(
  '/:id',
  authenticate,
  authorize(
    'products:update'
  ),
  validate(
    updateProductSchema
  ),
  asyncHandler(
    updateProduct
  )
)

router.delete(
  '/:id',
  authenticate,
  authorize(
    'products:delete'
  ),
  validate(
    deleteProductSchema
  ),
  asyncHandler(
    deleteProduct
  )
)
```

Las consultas públicas del catálogo pueden permanecer sin autenticación si ésa es la regla del proyecto.

---

# 7. Matriz inicial de acceso

| Operación | CUSTOMER | ADMIN |
| --- | --- | --- |
| Ver productos | Sí | Sí |
| Crear producto | No | Sí |
| Modificar producto | No | Sí |
| Eliminar producto | No | Sí |
| Consultar perfil propio | Sí | Sí |
| Crear carrito | Sí | Sí |
| Crear orden | Sí | Sí |
| Consultar todas las órdenes | No | Sí |

---

# 8. Preparar un usuario ADMIN

El registro público mantiene:

```text
role = CUSTOMER
```

No se debe permitir:

```json
{
  "role": "ADMIN"
}
```

desde el endpoint público de registro.

Para desarrollo, promover manualmente un usuario de prueba en Firestore cambiando:

```text
role: "ADMIN"
```

Después iniciar sesión nuevamente para emitir un access token con el rol actualizado.

---

# 9. Pruebas manuales

## Caso 1 — sin token

Intentar crear producto sin header `Authorization`.

Esperado:

```text
401 AUTH_REQUIRED
```

## Caso 2 — CUSTOMER

Iniciar sesión como `CUSTOMER` e intentar:

```text
POST /api/v1/products
```

Esperado:

```text
403 FORBIDDEN
```

## Caso 3 — ADMIN

Iniciar sesión como `ADMIN` y ejecutar la misma operación.

Esperado:

```text
201 Created
```

---

# 10. Qué prepara esta sesión

La siguiente sesión utilizará:

```javascript
authenticate,
authorize('products:create')
```

para proteger la administración de categorías y catálogo.

---

# Checklist

- [ ] Existe catálogo de roles y permisos.
- [ ] Existe `authorize.middleware.js`.
- [ ] `authenticate` se ejecuta antes de `authorize`.
- [ ] CUSTOMER obtiene 403 en operaciones administrativas.
- [ ] ADMIN puede crear, actualizar y eliminar productos.
- [ ] El registro público no permite elegir rol ADMIN.
- [ ] Las rutas públicas siguen funcionando.

---

# Commit sugerido

```bash
git switch -c feature/rbac-private-routes
git add .
git commit -m "feat: add RBAC and private routes"
```

## Navegación

- [Volver a documentación](./README.md)
- [Sesión 03 — Auth + Users + JWT](./SESION_03_AUTH_USERS_JWT.md)
- [Sesión 05 — Categories + Catálogo](./SESION_05_CATEGORIES_CATALOGO.md)
