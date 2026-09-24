[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← SESION_05_CATEGORIES_CATALOGO.md](./SESION_05_CATEGORIES_CATALOGO.md) · [SESION_07_TESTING_OPENAPI_CIERRE.md →](./SESION_07_TESTING_OPENAPI_CIERRE.md)

# SESIÓN 6 — CART + ORDERS

## Objetivo

Agregar el flujo de compra.

```text
Products
   |
   v
Cart
   |
   v
Checkout
   |
   v
Order
```

---

# 1. Cart Schema

Crear:

```text
apps/api/src/modules/cart/cart.schema.js
```

```javascript
import {
  z
} from 'zod'

const empty =
  z.object({}).default({})

export const getCartSchema =
  z.object({
    body:
      empty,

    params:
      empty,

    query:
      empty
  })

export const addItemSchema =
  z.object({
    body:
      z.object({
        productId:
          z.string()
            .trim()
            .min(1),

        quantity:
          z.coerce
            .number()
            .int()
            .positive()
            .max(99)
      }),

    params:
      empty,

    query:
      empty
  })

export const removeItemSchema =
  z.object({
    body:
      empty,

    params:
      z.object({
        productId:
          z.string()
            .trim()
            .min(1)
      }),

    query:
      empty
  })
```

---

# 2. Cart Repository

Crear:

```text
apps/api/src/modules/cart/cart.repository.js
```

```javascript
import {
  FieldValue
} from 'firebase-admin/firestore'

import {
  db
} from '../../config/firebase.js'

function cartRef(
  userId
) {
  return db
    .collection('carts')
    .doc(userId)
}

function itemsRef(
  userId
) {
  return cartRef(userId)
    .collection('items')
}

export async function listItems(
  userId
) {
  const snapshot =
    await itemsRef(userId)
      .get()

  return snapshot.docs.map(
    document => ({
      productId:
        document.id,

      ...document.data()
    })
  )
}

export async function upsertItem(
  userId,
  productId,
  quantity
) {
  await cartRef(userId)
    .set(
      {
        updatedAt:
          FieldValue.serverTimestamp()
      },
      {
        merge:
          true
      }
    )

  await itemsRef(userId)
    .doc(productId)
    .set(
      {
        quantity,

        updatedAt:
          FieldValue.serverTimestamp()
      },
      {
        merge:
          true
      }
    )
}

export async function removeItem(
  userId,
  productId
) {
  await itemsRef(userId)
    .doc(productId)
    .delete()
}

export async function clearCart(
  userId
) {
  const snapshot =
    await itemsRef(userId)
      .get()

  const batch =
    db.batch()

  snapshot.docs.forEach(
    document => {
      batch.delete(
        document.ref
      )
    }
  )

  await batch.commit()
}
```

---

# 3. Cart Service

Crear:

```text
apps/api/src/modules/cart/cart.service.js
```

```javascript
import {
  AppError
} from '../../shared/errors/app-error.js'

import * as productRepository
  from '../products/product.repository.js'

import * as cartRepository
  from './cart.repository.js'

export async function getCart(
  userId
) {
  const items =
    await cartRepository
      .listItems(
        userId
      )

  const detailedItems = []

  let total = 0

  for (
    const item of items
  ) {
    const product =
      await productRepository
        .findProductById(
          item.productId
        )

    if (!product) {
      continue
    }

    const subtotal =
      product.price *
      item.quantity

    total += subtotal

    detailedItems.push({
      productId:
        product.id,

      sku:
        product.sku,

      name:
        product.name,

      price:
        product.price,

      quantity:
        item.quantity,

      subtotal
    })
  }

  return {
    items:
      detailedItems,

    total
  }
}

export async function addItem(
  userId,
  {
    productId,
    quantity
  }
) {
  const product =
    await productRepository
      .findProductById(
        productId
      )

  if (
    !product ||
    !product.active
  ) {
    throw new AppError({
      statusCode:
        404,

      code:
        'PRODUCT_NOT_AVAILABLE',

      message:
        'Producto no disponible'
    })
  }

  if (
    quantity >
    product.stock
  ) {
    throw new AppError({
      statusCode:
        409,

      code:
        'INSUFFICIENT_STOCK',

      message:
        'Stock insuficiente'
    })
  }

  await cartRepository
    .upsertItem(
      userId,
      productId,
      quantity
    )

  return getCart(userId)
}

export async function removeItem(
  userId,
  productId
) {
  await cartRepository
    .removeItem(
      userId,
      productId
    )

  return getCart(userId)
}
```

---

# 4. Cart Controller

Crear:

```text
apps/api/src/modules/cart/cart.controller.js
```

```javascript
import * as cartService
  from './cart.service.js'

export async function getCart(
  req,
  res
) {
  const data =
    await cartService
      .getCart(
        req.auth.userId
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

export async function addItem(
  req,
  res
) {
  const data =
    await cartService
      .addItem(
        req.auth.userId,
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

export async function removeItem(
  req,
  res
) {
  const data =
    await cartService
      .removeItem(
        req.auth.userId,
        req.validated.params
          .productId
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

# 5. Cart Routes

Crear:

```text
apps/api/src/modules/cart/cart.routes.js
```

```javascript
import {
  Router
} from 'express'

import * as controller
  from './cart.controller.js'

import * as schema
  from './cart.schema.js'

import {
  asyncHandler
} from '../../shared/http/async-handler.js'

import {
  authenticate
} from '../../shared/middleware/authenticate.middleware.js'

import {
  validate
} from '../../shared/middleware/validate.middleware.js'

const router =
  Router()

router.use(
  authenticate
)

router.get(
  '/',
  validate(
    schema.getCartSchema
  ),
  asyncHandler(
    controller.getCart
  )
)

router.post(
  '/items',
  validate(
    schema.addItemSchema
  ),
  asyncHandler(
    controller.addItem
  )
)

router.delete(
  '/items/:productId',
  validate(
    schema.removeItemSchema
  ),
  asyncHandler(
    controller.removeItem
  )
)

export default router
```

---

# 6. Order Schema

Crear:

```text
apps/api/src/modules/orders/order.schema.js
```

```javascript
import {
  z
} from 'zod'

const empty =
  z.object({}).default({})

export const createOrderSchema =
  z.object({
    body:
      empty,

    params:
      empty,

    query:
      empty
  })

export const listOrdersSchema =
  z.object({
    body:
      empty,

    params:
      empty,

    query:
      empty
  })

export const getOrderSchema =
  z.object({
    body:
      empty,

    params:
      z.object({
        id:
          z.string()
            .trim()
            .min(1)
      }),

    query:
      empty
  })
```

---

# 7. Order Repository

Crear:

```text
apps/api/src/modules/orders/order.repository.js
```

```javascript
import {
  FieldValue
} from 'firebase-admin/firestore'

import {
  db
} from '../../config/firebase.js'

const ordersCollection =
  db.collection('orders')

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

function mapOrder(
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

export async function createOrder({
  userId,
  items
}) {
  return db.runTransaction(
    async transaction => {
      const productRefs =
        items.map(
          item =>
            db
              .collection('products')
              .doc(
                item.productId
              )
        )

      const productDocs =
        await Promise.all(
          productRefs.map(
            reference =>
              transaction.get(
                reference
              )
          )
        )

      const finalItems = []

      let serverTotal = 0

      for (
        let index = 0;
        index < productDocs.length;
        index++
      ) {
        const document =
          productDocs[index]

        const requestedItem =
          items[index]

        if (!document.exists) {
          throw new Error(
            `PRODUCT_NOT_FOUND:${requestedItem.productId}`
          )
        }

        const product =
          document.data()

        if (
          !product.active ||
          product.stock <
            requestedItem.quantity
        ) {
          throw new Error(
            `INSUFFICIENT_STOCK:${requestedItem.productId}`
          )
        }

        const subtotal =
          product.price *
          requestedItem.quantity

        serverTotal += subtotal

        finalItems.push({
          productId:
            document.id,

          sku:
            product.sku,

          name:
            product.name,

          unitPrice:
            product.price,

          quantity:
            requestedItem.quantity,

          subtotal
        })

        transaction.update(
          document.ref,
          {
            stock:
              product.stock -
              requestedItem.quantity,

            updatedAt:
              FieldValue
                .serverTimestamp()
          }
        )
      }

      const orderRef =
        ordersCollection.doc()

      transaction.set(
        orderRef,
        {
          userId,

          status:
            'CREATED',

          items:
            finalItems,

          total:
            serverTotal,

          createdAt:
            FieldValue
              .serverTimestamp(),

          updatedAt:
            FieldValue
              .serverTimestamp()
        }
      )

      return orderRef.id
    }
  )
}

export async function findOrderById(
  id
) {
  const document =
    await ordersCollection
      .doc(id)
      .get()

  return mapOrder(
    document
  )
}

export async function listOrdersByUser(
  userId
) {
  const snapshot =
    await ordersCollection
      .where(
        'userId',
        '==',
        userId
      )
      .orderBy(
        'createdAt',
        'desc'
      )
      .get()

  return snapshot.docs.map(
    mapOrder
  )
}
```

---

# 8. Order Service

Crear:

```text
apps/api/src/modules/orders/order.service.js
```

```javascript
import {
  AppError
} from '../../shared/errors/app-error.js'

import * as cartRepository
  from '../cart/cart.repository.js'

import * as orderRepository
  from './order.repository.js'

export async function createOrder(
  userId
) {
  const cartItems =
    await cartRepository
      .listItems(
        userId
      )

  if (
    cartItems.length === 0
  ) {
    throw new AppError({
      statusCode:
        409,

      code:
        'EMPTY_CART',

      message:
        'El carrito está vacío'
    })
  }

  let orderId

  try {
    orderId =
      await orderRepository
        .createOrder({
          userId,
          items:
            cartItems
        })
  } catch (error) {
    if (
      String(
        error.message
      ).startsWith(
        'PRODUCT_NOT_FOUND:'
      )
    ) {
      throw new AppError({
        statusCode:
          409,

        code:
          'PRODUCT_NOT_AVAILABLE',

        message:
          'Uno de los productos ya no existe'
      })
    }

    if (
      String(
        error.message
      ).startsWith(
        'INSUFFICIENT_STOCK:'
      )
    ) {
      throw new AppError({
        statusCode:
          409,

        code:
          'INSUFFICIENT_STOCK',

        message:
          'Stock insuficiente para completar la orden'
      })
    }

    throw error
  }

  await cartRepository
    .clearCart(
      userId
    )

  return orderRepository
    .findOrderById(
      orderId
    )
}

export async function listOrders(
  userId
) {
  return orderRepository
    .listOrdersByUser(
      userId
    )
}

export async function getOrder(
  userId,
  id
) {
  const order =
    await orderRepository
      .findOrderById(
        id
      )

  if (
    !order ||
    order.userId !== userId
  ) {
    throw new AppError({
      statusCode:
        404,

      code:
        'ORDER_NOT_FOUND',

      message:
        'Orden no encontrada'
    })
  }

  return order
}
```

---

# 9. Order Controller

Crear:

```text
apps/api/src/modules/orders/order.controller.js
```

```javascript
import * as orderService
  from './order.service.js'

export async function createOrder(
  req,
  res
) {
  const data =
    await orderService
      .createOrder(
        req.auth.userId
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

export async function listOrders(
  req,
  res
) {
  const data =
    await orderService
      .listOrders(
        req.auth.userId
      )

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

export async function getOrder(
  req,
  res
) {
  const data =
    await orderService
      .getOrder(
        req.auth.userId,
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
```

---

# 10. Order Routes

Crear:

```text
apps/api/src/modules/orders/order.routes.js
```

```javascript
import {
  Router
} from 'express'

import * as controller
  from './order.controller.js'

import * as schema
  from './order.schema.js'

import {
  asyncHandler
} from '../../shared/http/async-handler.js'

import {
  authenticate
} from '../../shared/middleware/authenticate.middleware.js'

import {
  validate
} from '../../shared/middleware/validate.middleware.js'

const router =
  Router()

router.use(
  authenticate
)

router.post(
  '/',
  validate(
    schema.createOrderSchema
  ),
  asyncHandler(
    controller.createOrder
  )
)

router.get(
  '/',
  validate(
    schema.listOrdersSchema
  ),
  asyncHandler(
    controller.listOrders
  )
)

router.get(
  '/:id',
  validate(
    schema.getOrderSchema
  ),
  asyncHandler(
    controller.getOrder
  )
)

export default router
```

---

# 11. Actualizar routes/index.js

Agregar:

```javascript
import cartRoutes
  from '../modules/cart/cart.routes.js'

import orderRoutes
  from '../modules/orders/order.routes.js'
```

Registrar:

```javascript
router.use(
  '/cart',
  cartRoutes
)

router.use(
  '/orders',
  orderRoutes
)
```

---

# 12. Endpoints

```text
GET    /api/v1/cart
POST   /api/v1/cart/items
DELETE /api/v1/cart/items/:productId

POST   /api/v1/orders
GET    /api/v1/orders
GET    /api/v1/orders/:id
```

Todos requieren:

```http
Authorization: Bearer ACCESS_TOKEN
```

---

# 13. Commit

```bash
git switch develop
git switch -c feature/cart-orders
git add .
git commit -m "feat(orders): add cart and order flow"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← SESION_05_CATEGORIES_CATALOGO.md](./SESION_05_CATEGORIES_CATALOGO.md) · [SESION_07_TESTING_OPENAPI_CIERRE.md →](./SESION_07_TESTING_OPENAPI_CIERRE.md)
