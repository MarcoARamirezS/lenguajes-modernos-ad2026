# 07 — Firebase Authentication y RBAC

**Duración:** 1 hora 30 minutos.

## Objetivo

Proteger la API verificando Firebase ID tokens y aplicando permisos en backend.

## Distribución de tiempo

- **00–20 min** — Firebase Auth client
- **20–40 min** — Bearer token
- **40–60 min** — verifyIdToken
- **60–75 min** — RBAC
- **75–90 min** — Security tests

## Conceptos

- ID token
- Authorization header
- token verification
- RBAC
- least privilege

## Desarrollo

### 1. Frontend login

El frontend autentica con Firebase Web SDK y obtiene un ID token. El API client lo agrega como `Authorization: Bearer <token>`.

### 2. Middleware funcional

Crear una función `requireAuth(req)` que valide encabezado, verifique el token con Firebase Admin y devuelva el principal autenticado.

### 3. Roles

Usar `ADMIN`, `COORDINATOR`, `VIEWER`. El rol puede almacenarse como custom claim o resolverse de la colección `users`; documentar una sola fuente de verdad.

### 4. Autorización

Crear `requireRole(user, allowedRoles)` y aplicarlo antes de mutaciones.

### 5. Casos

401 sin token, 401 token inválido, 403 rol insuficiente, 200 rol permitido.

## Endpoints al cierre

- `POST/PUT/DELETE de catálogos protegidos`
- `GET según política de lectura`

## Checklist de cierre

- [ ] Token inválido rechazado
- [ ] VIEWER no modifica
- [ ] COORDINATOR administra planificación
- [ ] ADMIN administra usuarios
- [ ] Permisos no dependen del frontend

## Commit sugerido

```bash
git add .
git commit -m "feat: implement Firebase authentication and RBAC"
```

## Código de autenticación

### `apps/api/src/auth/auth.ts`

```ts
import { auth, db } from '../firebase/admin'
import { AppError } from '../core/errors'

export type Role = 'ADMIN' | 'COORDINATOR' | 'VIEWER'

export type AuthenticatedUser = {
  uid: string
  email: string | null
  role: Role
}

export async function requireAuth(req: Request): Promise<AuthenticatedUser> {
  const header = req.headers.get('authorization')

  if (!header?.startsWith('Bearer ')) {
    throw new AppError(401, 'UNAUTHORIZED', 'Bearer token is required')
  }

  const token = header.slice('Bearer '.length)

  let decoded
  try {
    decoded = await auth.verifyIdToken(token)
  } catch {
    throw new AppError(401, 'UNAUTHORIZED', 'Invalid or expired token')
  }

  const profile = await db.collection('users').doc(decoded.uid).get()

  if (!profile.exists) {
    throw new AppError(403, 'USER_PROFILE_NOT_FOUND', 'User profile is not configured')
  }

  const role = profile.get('role') as Role

  if (!['ADMIN', 'COORDINATOR', 'VIEWER'].includes(role)) {
    throw new AppError(403, 'INVALID_ROLE', 'User role is invalid')
  }

  return {
    uid: decoded.uid,
    email: decoded.email ?? null,
    role
  }
}

export function requireRole(user: AuthenticatedUser, allowed: Role[]) {
  if (!allowed.includes(user.role)) {
    throw new AppError(403, 'FORBIDDEN', 'Insufficient permissions')
  }
}
```

## Uso en una ruta

```ts
router.post('/teachers', async req => {
  const user = await requireAuth(req)
  requireRole(user, ['ADMIN', 'COORDINATOR'])

  const input = createTeacherSchema.parse(await readJson(req))
  return json(await teacherService.create(input), 201)
})
```

## Política inicial

| Acción | ADMIN | COORDINATOR | VIEWER |
| --- | ---: | ---: | ---: |
| Leer catálogos | Sí | Sí | Sí |
| Modificar catálogos | Sí | Sí | No |
| Generar horario | Sí | Sí | No |
| Publicar | Sí | Sí | No |
| Administrar usuarios | Sí | No | No |

[Volver al índice](./README.md)
