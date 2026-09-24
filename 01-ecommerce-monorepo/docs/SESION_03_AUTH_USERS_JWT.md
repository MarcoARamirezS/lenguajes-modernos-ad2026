[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← SESION_02_PRODUCTS_COMPLETO.md](./SESION_02_PRODUCTS_COMPLETO.md) · [SESION_04_RBAC_RUTAS_PRIVADAS.md →](./SESION_04_RBAC_RUTAS_PRIVADAS.md)

# SESIÓN 3 — AUTH + USERS + JWT

## Objetivo

Agregar autenticación al backend existente.

Al terminar tendremos:

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
GET  /api/v1/users/me
```

El flujo será:

```text
Register/Login
    |
    v
Controller
    |
    v
Service
    |
    +--> Password Hash
    |
    +--> User Repository
    |
    +--> JWT Access Token
    |
    `--> JWT Refresh Token
```

---

# 1. Instalar paquetes

Desde la raíz del monorepo:

```bash
npm install bcryptjs jsonwebtoken --workspace=@ecommerce/api
```

## Paquetes

### bcryptjs

Se utiliza para:

```text
Password
   |
   v
Hash
   |
   v
Firestore
```

Nunca se debe guardar la contraseña original.

### jsonwebtoken

Se utiliza para generar:

```text
Access Token
Refresh Token
```

---

# 2. Variables de entorno

Modificar:

```text
apps/api/.env
```

Agregar:

```env
JWT_ACCESS_SECRET=change-this-access-secret
JWT_REFRESH_SECRET=change-this-refresh-secret
JWT_ACCESS_EXPIRES_IN=15m
JWT_REFRESH_EXPIRES_IN=7d
```

Agregar también en:

```text
apps/api/.env.example
```

```env
JWT_ACCESS_SECRET=
JWT_REFRESH_SECRET=
JWT_ACCESS_EXPIRES_IN=15m
JWT_REFRESH_EXPIRES_IN=7d
```

---

# 3. Configuración JWT

Crear:

```text
apps/api/src/config/auth.js
```

```javascript
export const authConfig = Object.freeze({
  accessSecret:
    process.env.JWT_ACCESS_SECRET,

  refreshSecret:
    process.env.JWT_REFRESH_SECRET,

  accessExpiresIn:
    process.env.JWT_ACCESS_EXPIRES_IN ?? '15m',

  refreshExpiresIn:
    process.env.JWT_REFRESH_EXPIRES_IN ?? '7d'
})

if (
  !authConfig.accessSecret ||
  !authConfig.refreshSecret
) {
  throw new Error(
    'JWT secrets are required'
  )
}
```

---

# 4. Password utility

Crear:

```text
apps/api/src/shared/security/password.js
```

```javascript
import bcrypt from 'bcryptjs'

const SALT_ROUNDS = 12

export function hashPassword(
  password
) {
  return bcrypt.hash(
    password,
    SALT_ROUNDS
  )
}

export function verifyPassword(
  password,
  passwordHash
) {
  return bcrypt.compare(
    password,
    passwordHash
  )
}
```

---

# 5. Tokens utility

Crear:

```text
apps/api/src/shared/security/tokens.js
```

```javascript
import {
  createHash
} from 'node:crypto'

import jwt
  from 'jsonwebtoken'

import {
  authConfig
} from '../../config/auth.js'

export function signAccessToken(
  payload
) {
  return jwt.sign(
    payload,
    authConfig.accessSecret,
    {
      expiresIn:
        authConfig.accessExpiresIn
    }
  )
}

export function signRefreshToken(
  payload
) {
  return jwt.sign(
    payload,
    authConfig.refreshSecret,
    {
      expiresIn:
        authConfig.refreshExpiresIn
    }
  )
}

export function verifyAccessToken(
  token
) {
  return jwt.verify(
    token,
    authConfig.accessSecret
  )
}

export function verifyRefreshToken(
  token
) {
  return jwt.verify(
    token,
    authConfig.refreshSecret
  )
}

export function hashToken(
  token
) {
  return createHash('sha256')
    .update(token)
    .digest('hex')
}
```

---

# 6. User Repository

Crear:

```text
apps/api/src/modules/users/user.repository.js
```

```javascript
import {
  FieldValue
} from 'firebase-admin/firestore'

import {
  db
} from '../../config/firebase.js'

const usersCollection =
  db.collection('users')

function mapTimestamp(
  value
) {
  return (
    value
      ?.toDate?.()
      ?.toISOString() ??
    null
  )
}

function mapUser(
  document
) {
  if (!document.exists) {
    return null
  }

  const data =
    document.data()

  return {
    id:
      document.id,

    email:
      data.email,

    name:
      data.name,

    role:
      data.role,

    active:
      data.active,

    createdAt:
      mapTimestamp(
        data.createdAt
      ),

    updatedAt:
      mapTimestamp(
        data.updatedAt
      )
  }
}

export async function findByEmail(
  email
) {
  const snapshot =
    await usersCollection
      .where(
        'email',
        '==',
        email
      )
      .limit(1)
      .get()

  if (snapshot.empty) {
    return null
  }

  const document =
    snapshot.docs[0]

  return {
    ...mapUser(document),

    passwordHash:
      document.data().passwordHash
  }
}

export async function findById(
  id
) {
  const document =
    await usersCollection
      .doc(id)
      .get()

  return mapUser(document)
}

export async function createUser(
  data
) {
  const userRef =
    usersCollection.doc()

  await userRef.set({
    ...data,

    createdAt:
      FieldValue.serverTimestamp(),

    updatedAt:
      FieldValue.serverTimestamp()
  })

  const created =
    await userRef.get()

  return mapUser(created)
}
```

---

# 7. Auth Schema

Crear:

```text
apps/api/src/modules/auth/auth.schema.js
```

```javascript
import {
  z
} from 'zod'

const empty =
  z.object({}).default({})

const email =
  z.string()
    .trim()
    .toLowerCase()
    .email()

const password =
  z.string()
    .min(8)
    .max(100)

export const registerSchema =
  z.object({
    body:
      z.object({
        name:
          z.string()
            .trim()
            .min(2)
            .max(120),

        email,

        password
      }),

    params:
      empty,

    query:
      empty
  })

export const loginSchema =
  z.object({
    body:
      z.object({
        email,
        password
      }),

    params:
      empty,

    query:
      empty
  })

export const refreshSchema =
  z.object({
    body:
      z.object({
        refreshToken:
          z.string()
            .min(1)
      }),

    params:
      empty,

    query:
      empty
  })
```

---

# 8. Auth Repository

Crear:

```text
apps/api/src/modules/auth/auth.repository.js
```

```javascript
import {
  FieldValue
} from 'firebase-admin/firestore'

import {
  db
} from '../../config/firebase.js'

const refreshTokensCollection =
  db.collection('refreshTokens')

export async function saveRefreshToken({
  userId,
  tokenHash
}) {
  await refreshTokensCollection
    .doc(tokenHash)
    .set({
      userId,

      revoked:
        false,

      createdAt:
        FieldValue.serverTimestamp()
    })
}

export async function findRefreshToken(
  tokenHash
) {
  const document =
    await refreshTokensCollection
      .doc(tokenHash)
      .get()

  if (!document.exists) {
    return null
  }

  return {
    id:
      document.id,

    ...document.data()
  }
}

export async function revokeRefreshToken(
  tokenHash
) {
  await refreshTokensCollection
    .doc(tokenHash)
    .set(
      {
        revoked:
          true,

        revokedAt:
          FieldValue.serverTimestamp()
      },
      {
        merge:
          true
      }
    )
}
```

---

# 9. Auth Service

Crear:

```text
apps/api/src/modules/auth/auth.service.js
```

```javascript
import {
  AppError
} from '../../shared/errors/app-error.js'

import {
  hashPassword,
  verifyPassword
} from '../../shared/security/password.js'

import {
  hashToken,
  signAccessToken,
  signRefreshToken,
  verifyRefreshToken
} from '../../shared/security/tokens.js'

import * as userRepository
  from '../users/user.repository.js'

import * as authRepository
  from './auth.repository.js'

function issueTokens(
  user
) {
  const payload = {
    sub:
      user.id,

    role:
      user.role
  }

  return {
    accessToken:
      signAccessToken(payload),

    refreshToken:
      signRefreshToken(payload)
  }
}

export async function register(
  data
) {
  const existingUser =
    await userRepository
      .findByEmail(
        data.email
      )

  if (existingUser) {
    throw new AppError({
      statusCode:
        409,

      code:
        'EMAIL_EXISTS',

      message:
        'El correo ya está registrado'
    })
  }

  const user =
    await userRepository
      .createUser({
        name:
          data.name,

        email:
          data.email,

        passwordHash:
          await hashPassword(
            data.password
          ),

        role:
          'CUSTOMER',

        active:
          true
      })

  const tokens =
    issueTokens(user)

  await authRepository
    .saveRefreshToken({
      userId:
        user.id,

      tokenHash:
        hashToken(
          tokens.refreshToken
        )
    })

  return {
    user,

    ...tokens
  }
}

export async function login(
  data
) {
  const user =
    await userRepository
      .findByEmail(
        data.email
      )

  if (!user) {
    throw new AppError({
      statusCode:
        401,

      code:
        'INVALID_CREDENTIALS',

      message:
        'Credenciales inválidas'
    })
  }

  const validPassword =
    await verifyPassword(
      data.password,
      user.passwordHash
    )

  if (
    !validPassword ||
    !user.active
  ) {
    throw new AppError({
      statusCode:
        401,

      code:
        'INVALID_CREDENTIALS',

      message:
        'Credenciales inválidas'
    })
  }

  const safeUser =
    await userRepository
      .findById(
        user.id
      )

  const tokens =
    issueTokens(
      safeUser
    )

  await authRepository
    .saveRefreshToken({
      userId:
        safeUser.id,

      tokenHash:
        hashToken(
          tokens.refreshToken
        )
    })

  return {
    user:
      safeUser,

    ...tokens
  }
}

export async function refresh(
  refreshToken
) {
  let payload

  try {
    payload =
      verifyRefreshToken(
        refreshToken
      )
  } catch {
    throw new AppError({
      statusCode:
        401,

      code:
        'INVALID_REFRESH_TOKEN',

      message:
        'Refresh token inválido'
    })
  }

  const tokenHash =
    hashToken(
      refreshToken
    )

  const storedToken =
    await authRepository
      .findRefreshToken(
        tokenHash
      )

  if (
    !storedToken ||
    storedToken.revoked ||
    storedToken.userId !== payload.sub
  ) {
    throw new AppError({
      statusCode:
        401,

      code:
        'INVALID_REFRESH_TOKEN',

      message:
        'Refresh token inválido'
    })
  }

  await authRepository
    .revokeRefreshToken(
      tokenHash
    )

  const user =
    await userRepository
      .findById(
        payload.sub
      )

  if (
    !user ||
    !user.active
  ) {
    throw new AppError({
      statusCode:
        401,

      code:
        'USER_DISABLED',

      message:
        'Usuario no disponible'
    })
  }

  const tokens =
    issueTokens(user)

  await authRepository
    .saveRefreshToken({
      userId:
        user.id,

      tokenHash:
        hashToken(
          tokens.refreshToken
        )
    })

  return tokens
}
```

---

# 10. Auth Controller

Crear:

```text
apps/api/src/modules/auth/auth.controller.js
```

```javascript
import * as authService
  from './auth.service.js'

export async function register(
  req,
  res
) {
  const data =
    await authService
      .register(
        req.validated.body
      )

  return res
    .status(201)
    .json({
      success:
        true,

      data,

      meta: {
        requestId:
          req.id
      }
    })
}

export async function login(
  req,
  res
) {
  const data =
    await authService
      .login(
        req.validated.body
      )

  return res
    .status(200)
    .json({
      success:
        true,

      data,

      meta: {
        requestId:
          req.id
      }
    })
}

export async function refresh(
  req,
  res
) {
  const data =
    await authService
      .refresh(
        req.validated
          .body
          .refreshToken
      )

  return res
    .status(200)
    .json({
      success:
        true,

      data,

      meta: {
        requestId:
          req.id
      }
    })
}
```

---

# 11. Auth Routes

Crear:

```text
apps/api/src/modules/auth/auth.routes.js
```

```javascript
import {
  Router
} from 'express'

import {
  login,
  refresh,
  register
} from './auth.controller.js'

import {
  loginSchema,
  refreshSchema,
  registerSchema
} from './auth.schema.js'

import {
  asyncHandler
} from '../../shared/http/async-handler.js'

import {
  validate
} from '../../shared/middleware/validate.middleware.js'

const router =
  Router()

router.post(
  '/register',
  validate(
    registerSchema
  ),
  asyncHandler(
    register
  )
)

router.post(
  '/login',
  validate(
    loginSchema
  ),
  asyncHandler(
    login
  )
)

router.post(
  '/refresh',
  validate(
    refreshSchema
  ),
  asyncHandler(
    refresh
  )
)

export default router
```

---

# 12. Middleware authenticate

Crear:

```text
apps/api/src/shared/middleware/authenticate.middleware.js
```

```javascript
import {
  AppError
} from '../errors/app-error.js'

import {
  verifyAccessToken
} from '../security/tokens.js'

export function authenticate(
  req,
  _res,
  next
) {
  const authorization =
    req.headers.authorization

  if (
    !authorization ||
    !authorization
      .startsWith('Bearer ')
  ) {
    return next(
      new AppError({
        statusCode:
          401,

        code:
          'AUTH_REQUIRED',

        message:
          'Autenticación requerida'
      })
    )
  }

  const token =
    authorization.slice(7)

  try {
    const payload =
      verifyAccessToken(
        token
      )

    req.auth = {
      userId:
        payload.sub,

      role:
        payload.role
    }

    return next()
  } catch {
    return next(
      new AppError({
        statusCode:
          401,

        code:
          'INVALID_ACCESS_TOKEN',

        message:
          'Access token inválido'
      })
    )
  }
}
```

---

# 13. User Controller

Crear:

```text
apps/api/src/modules/users/user.controller.js
```

```javascript
import {
  AppError
} from '../../shared/errors/app-error.js'

import * as userRepository
  from './user.repository.js'

export async function me(
  req,
  res
) {
  const user =
    await userRepository
      .findById(
        req.auth.userId
      )

  if (!user) {
    throw new AppError({
      statusCode:
        404,

      code:
        'USER_NOT_FOUND',

      message:
        'Usuario no encontrado'
    })
  }

  return res
    .status(200)
    .json({
      success:
        true,

      data:
        user,

      meta: {
        requestId:
          req.id
      }
    })
}
```

---

# 14. User Routes

Crear:

```text
apps/api/src/modules/users/user.routes.js
```

```javascript
import {
  Router
} from 'express'

import {
  me
} from './user.controller.js'

import {
  asyncHandler
} from '../../shared/http/async-handler.js'

import {
  authenticate
} from '../../shared/middleware/authenticate.middleware.js'

const router =
  Router()

router.get(
  '/me',
  authenticate,
  asyncHandler(me)
)

export default router
```

---

# 15. Actualizar routes/index.js

Modificar:

```text
apps/api/src/routes/index.js
```

```javascript
import {
  Router
} from 'express'

import authRoutes
  from '../modules/auth/auth.routes.js'

import healthRoutes
  from '../modules/health/health.routes.js'

import productRoutes
  from '../modules/products/product.routes.js'

import userRoutes
  from '../modules/users/user.routes.js'

const router =
  Router()

router.use(
  '/health',
  healthRoutes
)

router.use(
  '/auth',
  authRoutes
)

router.use(
  '/users',
  userRoutes
)

router.use(
  '/products',
  productRoutes
)

export default router
```

---

# 16. Pruebas

## Register

```bash
curl -i \
  -X POST \
  http://localhost:4050/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alumno Demo",
    "email": "alumno@example.com",
    "password": "Password123"
  }'
```

## Login

```bash
curl -i \
  -X POST \
  http://localhost:4050/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alumno@example.com",
    "password": "Password123"
  }'
```

## Me

```bash
curl -i \
  http://localhost:4050/api/v1/users/me \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

---

# 17. Commit

```bash
git switch develop
git switch -c feature/auth-users
git add .
git commit -m "feat(auth): add users and JWT authentication"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← SESION_02_PRODUCTS_COMPLETO.md](./SESION_02_PRODUCTS_COMPLETO.md) · [SESION_04_RBAC_RUTAS_PRIVADAS.md →](./SESION_04_RBAC_RUTAS_PRIVADAS.md)
