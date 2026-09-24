[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← SESION_04_RBAC_RUTAS_PRIVADAS.md](./SESION_04_RBAC_RUTAS_PRIVADAS.md) · [SESION_06_CART_ORDERS.md →](./SESION_06_CART_ORDERS.md)

# SESIÓN 5 — CATEGORIES + CATÁLOGO

## Objetivo

Agregar categorías y relacionarlas con Products.

---

# 1. Category Schema

Crear:

```text
apps/api/src/modules/categories/category.schema.js
```

```javascript
import {
  z
} from 'zod'

const empty =
  z.object({}).default({})

const params =
  z.object({
    id:
      z.string()
        .trim()
        .min(1)
  })

const categoryBody =
  z.object({
    name:
      z.string()
        .trim()
        .min(2)
        .max(100),

    slug:
      z.string()
        .trim()
        .min(2)
        .max(120)
        .regex(
          /^[a-z0-9-]+$/
        ),

    active:
      z.boolean()
        .default(true)
  })

export const listCategoriesSchema =
  z.object({
    body:
      empty,

    params:
      empty,

    query:
      empty
  })

export const getCategorySchema =
  z.object({
    body:
      empty,

    params,

    query:
      empty
  })

export const createCategorySchema =
  z.object({
    body:
      categoryBody,

    params:
      empty,

    query:
      empty
  })

export const updateCategorySchema =
  z.object({
    body:
      categoryBody
        .partial()
        .refine(
          value =>
            Object.keys(value)
              .length > 0,
          {
            message:
              'At least one field is required'
          }
        ),

    params,

    query:
      empty
  })

export const deleteCategorySchema =
  z.object({
    body:
      empty,

    params,

    query:
      empty
  })
```

---

# 2. Category Repository

Crear:

```text
apps/api/src/modules/categories/category.repository.js
```

```javascript
import {
  FieldValue
} from 'firebase-admin/firestore'

import {
  db
} from '../../config/firebase.js'

const categoriesCollection =
  db.collection('categories')

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

function mapCategory(
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

    ...data,

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

export async function listCategories() {
  const snapshot =
    await categoriesCollection
      .orderBy(
        'name'
      )
      .get()

  return snapshot.docs.map(
    mapCategory
  )
}

export async function findCategoryById(
  id
) {
  const document =
    await categoriesCollection
      .doc(id)
      .get()

  return mapCategory(
    document
  )
}

export async function findCategoryBySlug(
  slug
) {
  const snapshot =
    await categoriesCollection
      .where(
        'slug',
        '==',
        slug
      )
      .limit(1)
      .get()

  return snapshot.empty
    ? null
    : mapCategory(
        snapshot.docs[0]
      )
}

export async function createCategory(
  data
) {
  const categoryRef =
    categoriesCollection.doc()

  await categoryRef.set({
    ...data,

    createdAt:
      FieldValue.serverTimestamp(),

    updatedAt:
      FieldValue.serverTimestamp()
  })

  return mapCategory(
    await categoryRef.get()
  )
}

export async function updateCategory(
  id,
  data
) {
  const categoryRef =
    categoriesCollection.doc(id)

  await categoryRef.update({
    ...data,

    updatedAt:
      FieldValue.serverTimestamp()
  })

  return mapCategory(
    await categoryRef.get()
  )
}

export async function deleteCategory(
  id
) {
  await categoriesCollection
    .doc(id)
    .delete()
}
```

---

# 3. Category Service

Crear:

```text
apps/api/src/modules/categories/category.service.js
```

```javascript
import {
  AppError
} from '../../shared/errors/app-error.js'

import * as categoryRepository
  from './category.repository.js'

export async function listCategories() {
  return categoryRepository
    .listCategories()
}

export async function getCategory(
  id
) {
  const category =
    await categoryRepository
      .findCategoryById(
        id
      )

  if (!category) {
    throw new AppError({
      statusCode:
        404,

      code:
        'CATEGORY_NOT_FOUND',

      message:
        'Categoría no encontrada'
    })
  }

  return category
}

export async function createCategory(
  data
) {
  const existing =
    await categoryRepository
      .findCategoryBySlug(
        data.slug
      )

  if (existing) {
    throw new AppError({
      statusCode:
        409,

      code:
        'CATEGORY_SLUG_EXISTS',

      message:
        'El slug ya existe'
    })
  }

  return categoryRepository
    .createCategory(
      data
    )
}

export async function updateCategory(
  id,
  data
) {
  await getCategory(id)

  if (data.slug) {
    const existing =
      await categoryRepository
        .findCategoryBySlug(
          data.slug
        )

    if (
      existing &&
      existing.id !== id
    ) {
      throw new AppError({
        statusCode:
          409,

        code:
          'CATEGORY_SLUG_EXISTS',

        message:
          'El slug ya existe'
      })
    }
  }

  return categoryRepository
    .updateCategory(
      id,
      data
    )
}

export async function deleteCategory(
  id
) {
  await getCategory(id)

  await categoryRepository
    .deleteCategory(id)
}
```

---

# 4. Category Controller

Crear:

```text
apps/api/src/modules/categories/category.controller.js
```

```javascript
import * as categoryService
  from './category.service.js'

export async function listCategories(
  req,
  res
) {
  const data =
    await categoryService
      .listCategories()

  return res.status(200).json({
    success:
      true,

    data,

    meta: {
      count:
        data.length,

      requestId:
        req.id
    }
  })
}

export async function getCategory(
  req,
  res
) {
  const data =
    await categoryService
      .getCategory(
        req.validated.params.id
      )

  return res.status(200).json({
    success:
      true,

    data,

    meta: {
      requestId:
        req.id
    }
  })
}

export async function createCategory(
  req,
  res
) {
  const data =
    await categoryService
      .createCategory(
        req.validated.body
      )

  return res.status(201).json({
    success:
      true,

    data,

    meta: {
      requestId:
        req.id
    }
  })
}

export async function updateCategory(
  req,
  res
) {
  const data =
    await categoryService
      .updateCategory(
        req.validated.params.id,
        req.validated.body
      )

  return res.status(200).json({
    success:
      true,

    data,

    meta: {
      requestId:
        req.id
    }
  })
}

export async function deleteCategory(
  req,
  res
) {
  await categoryService
    .deleteCategory(
      req.validated.params.id
    )

  return res
    .status(204)
    .send()
}
```

---

# 5. Category Routes

Crear:

```text
apps/api/src/modules/categories/category.routes.js
```

```javascript
import {
  Router
} from 'express'

import * as controller
  from './category.controller.js'

import * as schema
  from './category.schema.js'

import {
  asyncHandler
} from '../../shared/http/async-handler.js'

import {
  authenticate
} from '../../shared/middleware/authenticate.middleware.js'

import {
  authorize
} from '../../shared/middleware/authorize.middleware.js'

import {
  validate
} from '../../shared/middleware/validate.middleware.js'

const router =
  Router()

router.get(
  '/',
  validate(
    schema.listCategoriesSchema
  ),
  asyncHandler(
    controller.listCategories
  )
)

router.get(
  '/:id',
  validate(
    schema.getCategorySchema
  ),
  asyncHandler(
    controller.getCategory
  )
)

router.post(
  '/',
  authenticate,
  authorize(
    'products:create'
  ),
  validate(
    schema.createCategorySchema
  ),
  asyncHandler(
    controller.createCategory
  )
)

router.patch(
  '/:id',
  authenticate,
  authorize(
    'products:update'
  ),
  validate(
    schema.updateCategorySchema
  ),
  asyncHandler(
    controller.updateCategory
  )
)

router.delete(
  '/:id',
  authenticate,
  authorize(
    'products:delete'
  ),
  validate(
    schema.deleteCategorySchema
  ),
  asyncHandler(
    controller.deleteCategory
  )
)

export default router
```

---

# 6. Actualizar routes/index.js

Agregar:

```javascript
import categoryRoutes
  from '../modules/categories/category.routes.js'
```

Y:

```javascript
router.use(
  '/categories',
  categoryRoutes
)
```

Archivo completo esperado:

```javascript
import {
  Router
} from 'express'

import authRoutes
  from '../modules/auth/auth.routes.js'

import categoryRoutes
  from '../modules/categories/category.routes.js'

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

router.use(
  '/categories',
  categoryRoutes
)

export default router
```

---

# 7. Agregar categoryId a Products

En:

```text
product.schema.js
```

agregar al producto:

```javascript
categoryId:
  z.string()
    .trim()
    .min(1)
```

También agregar al listado:

```javascript
categoryId:
  z.string()
    .trim()
    .min(1)
    .optional()
```

Y en repository añadir filtro:

```javascript
if (categoryId) {
  query =
    query.where(
      'categoryId',
      '==',
      categoryId
    )
}
```

---

# 8. Endpoints

```text
GET    /api/v1/categories
GET    /api/v1/categories/:id
POST   /api/v1/categories
PATCH  /api/v1/categories/:id
DELETE /api/v1/categories/:id
```

---

# 9. Commit

```bash
git switch develop
git switch -c feature/categories
git add .
git commit -m "feat(catalog): add categories module"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← SESION_04_RBAC_RUTAS_PRIVADAS.md](./SESION_04_RBAC_RUTAS_PRIVADAS.md) · [SESION_06_CART_ORDERS.md →](./SESION_06_CART_ORDERS.md)
