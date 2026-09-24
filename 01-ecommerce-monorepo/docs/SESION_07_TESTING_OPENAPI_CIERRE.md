# SESIÓN 7 — TESTING + OPENAPI + CIERRE

## Objetivo

Cerrar la primera versión del backend con:

```text
Vitest
Supertest
Swagger / OpenAPI
```

---

# 1. Instalar paquetes

```bash
npm install -D vitest supertest --workspace=@ecommerce/api
```

```bash
npm install swagger-ui-express --workspace=@ecommerce/api
```

---

# 2. Actualizar package.json del API

En:

```text
apps/api/package.json
```

agregar scripts:

```json
{
  "scripts": {
    "dev": "nodemon src/server.js",
    "start": "node src/server.js",
    "lint": "eslint src tests",
    "test": "vitest run",
    "test:watch": "vitest"
  }
}
```

---

# 3. OpenAPI

Crear:

```text
apps/api/src/docs/openapi.js
```

```javascript
export const openapi = {
  openapi:
    '3.0.3',

  info: {
    title:
      'E-Commerce API',

    version:
      '1.0.0',

    description:
      'API REST del proyecto evolutivo E-Commerce'
  },

  servers: [
    {
      url:
        'http://localhost:4050/api/v1'
    }
  ],

  paths: {
    '/health': {
      get: {
        summary:
          'Health check',

        responses: {
          200: {
            description:
              'API disponible'
          }
        }
      }
    },

    '/products': {
      get: {
        summary:
          'Listar productos',

        responses: {
          200: {
            description:
              'Listado de productos'
          }
        }
      },

      post: {
        summary:
          'Crear producto',

        security: [
          {
            bearerAuth: []
          }
        ],

        responses: {
          201: {
            description:
              'Producto creado'
          }
        }
      }
    },

    '/auth/register': {
      post: {
        summary:
          'Registrar usuario',

        responses: {
          201: {
            description:
              'Usuario creado'
          }
        }
      }
    },

    '/auth/login': {
      post: {
        summary:
          'Iniciar sesión',

        responses: {
          200: {
            description:
              'Login correcto'
          }
        }
      }
    },

    '/cart': {
      get: {
        summary:
          'Consultar carrito',

        security: [
          {
            bearerAuth: []
          }
        ],

        responses: {
          200: {
            description:
              'Carrito'
          }
        }
      }
    },

    '/orders': {
      get: {
        summary:
          'Consultar órdenes',

        security: [
          {
            bearerAuth: []
          }
        ],

        responses: {
          200: {
            description:
              'Órdenes'
          }
        }
      },

      post: {
        summary:
          'Crear orden',

        security: [
          {
            bearerAuth: []
          }
        ],

        responses: {
          201: {
            description:
              'Orden creada'
          }
        }
      }
    }
  },

  components: {
    securitySchemes: {
      bearerAuth: {
        type:
          'http',

        scheme:
          'bearer',

        bearerFormat:
          'JWT'
      }
    }
  }
}
```

---

# 4. Modificar app.js

Agregar:

```javascript
import swaggerUi
  from 'swagger-ui-express'

import {
  openapi
} from './docs/openapi.js'
```

Antes del router principal:

```javascript
app.use(
  '/api-docs',
  swaggerUi.serve,
  swaggerUi.setup(
    openapi
  )
)
```

La sección debe quedar:

```javascript
app.use(
  '/api-docs',
  swaggerUi.serve,
  swaggerUi.setup(
    openapi
  )
)

app.use(
  env.API_PREFIX,
  apiRouter
)
```

Swagger estará disponible en:

```text
http://localhost:4050/api-docs
```

---

# 5. Test de Health

Crear:

```text
apps/api/tests/health.test.js
```

```javascript
import {
  describe,
  expect,
  it
} from 'vitest'

process.env
  .FIRESTORE_EMULATOR_HOST =
    process.env
      .FIRESTORE_EMULATOR_HOST ??
    '127.0.0.1:8080'

process.env
  .FIREBASE_PROJECT_ID =
    process.env
      .FIREBASE_PROJECT_ID ??
    'demo-ecommerce'

process.env
  .JWT_ACCESS_SECRET =
    process.env
      .JWT_ACCESS_SECRET ??
    'test-access-secret'

process.env
  .JWT_REFRESH_SECRET =
    process.env
      .JWT_REFRESH_SECRET ??
    'test-refresh-secret'

const {
  default: request
} =
  await import(
    'supertest'
  )

const {
  app
} =
  await import(
    '../src/app.js'
  )

describe(
  'GET /api/v1/health',
  () => {
    it(
      'returns 200',
      async () => {
        const response =
          await request(app)
            .get(
              '/api/v1/health'
            )

        expect(
          response.status
        ).toBe(200)

        expect(
          response.body.success
        ).toBe(true)

        expect(
          response.body.data.status
        ).toBe('ok')
      }
    )
  }
)
```

---

# 6. Test 404

Crear:

```text
apps/api/tests/not-found.test.js
```

```javascript
import {
  describe,
  expect,
  it
} from 'vitest'

process.env
  .FIRESTORE_EMULATOR_HOST =
    '127.0.0.1:8080'

process.env
  .FIREBASE_PROJECT_ID =
    'demo-ecommerce'

process.env
  .JWT_ACCESS_SECRET =
    'test-access-secret'

process.env
  .JWT_REFRESH_SECRET =
    'test-refresh-secret'

const {
  default: request
} =
  await import(
    'supertest'
  )

const {
  app
} =
  await import(
    '../src/app.js'
  )

describe(
  '404 middleware',
  () => {
    it(
      'returns standard error',
      async () => {
        const response =
          await request(app)
            .get(
              '/api/v1/does-not-exist'
            )

        expect(
          response.status
        ).toBe(404)

        expect(
          response.body.error.code
        ).toBe(
          'ROUTE_NOT_FOUND'
        )
      }
    )
  }
)
```

---

# 7. Test Product Schema

Crear:

```text
apps/api/tests/product-schema.test.js
```

```javascript
import {
  describe,
  expect,
  it
} from 'vitest'

import {
  createProductSchema
} from '../src/modules/products/product.schema.js'

describe(
  'createProductSchema',
  () => {
    it(
      'accepts valid product',
      () => {
        const result =
          createProductSchema
            .parse({
              body: {
                sku:
                  'lap-001',

                name:
                  'Laptop',

                description:
                  'Demo',

                categoryId:
                  'computers',

                price:
                  1000,

                stock:
                  5,

                active:
                  true
              },

              params:
                {},

              query:
                {}
            })

        expect(
          result.body.sku
        ).toBe(
          'LAP-001'
        )
      }
    )

    it(
      'rejects negative price',
      () => {
        expect(
          () =>
            createProductSchema
              .parse({
                body: {
                  sku:
                    'lap-002',

                  name:
                    'Laptop',

                  categoryId:
                    'computers',

                  price:
                    -1,

                  stock:
                    1,

                  active:
                    true
                },

                params:
                  {},

                query:
                  {}
              })
        ).toThrow()
      }
    )
  }
)
```

---

# 8. Ejecutar pruebas

```bash
npm run test --workspace=@ecommerce/api
```

Después:

```bash
npm run lint
```

---

# 9. Validación final

Probar:

```bash
npm run dev
```

Después:

```text
http://localhost:4050/api-docs
```

Y:

```bash
curl -i http://localhost:4050/api/v1/health
```

---

# 10. Resultado final

```text
API
|
+-- health
|
+-- auth
|
+-- users
|
+-- products
|
+-- categories
|
+-- cart
|
`-- orders
```

Con:

```text
JWT
RBAC
Zod
Firestore
Vitest
Supertest
OpenAPI
```

---

# 11. Commit

```bash
git switch develop
git switch -c feature/testing-openapi
git add .
git commit -m "test(api): add API tests and OpenAPI documentation"
```

---

# 12. Cierre del proyecto

Después:

```bash
git switch develop
git merge feature/testing-openapi
```

Validar:

```bash
npm run lint
npm run test --workspace=@ecommerce/api
npm run dev
```
