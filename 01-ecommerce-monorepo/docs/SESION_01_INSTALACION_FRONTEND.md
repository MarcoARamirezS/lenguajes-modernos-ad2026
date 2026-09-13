# Instalación del Frontend Nuxt 4 en el Monorepo

Esta guía explica cómo agregar el frontend al monorepo actual del proyecto e-commerce.

El backend ya se encuentra documentado en las sesiones previas. Ahora se agregará una aplicación frontend dentro de `apps/web`.

## Resultado esperado

Al finalizar, el monorepo debe quedar así:

```text
ecommerce-monorepo/
├── package.json
├── .gitignore
└── apps/
    ├── api/
    │   └── backend existente
    └── web/
        └── frontend Nuxt 4
```

## 1. Verificar estructura actual

Antes de instalar el frontend, confirma que tu backend esté dentro de:

```text
apps/api
```

La estructura mínima esperada es:

```text
ecommerce-monorepo/
├── package.json
└── apps/
    └── api/
        ├── package.json
        └── src/
```

## 2. Actualizar el `package.json` raíz

El archivo raíz debe manejar los workspaces:

```json
{
  "name": "ecommerce-monorepo",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "workspaces": [
    "apps/api",
    "apps/web"
  ],
  "scripts": {
    "dev:api": "npm run dev --workspace=@ecommerce/api",
    "dev:web": "npm run dev --workspace=@ecommerce/web",
    "build:web": "npm run build --workspace=@ecommerce/web",
    "generate:web": "npm run generate --workspace=@ecommerce/web",
    "typecheck:web": "npm run typecheck --workspace=@ecommerce/web",
    "lint:web": "npm run lint --workspace=@ecommerce/web",
    "test:e2e:web": "npm run test:e2e --workspace=@ecommerce/web"
  },
  "engines": {
    "node": ">=24.0.0"
  }
}
```

Si ya tienes scripts del backend, conserva los existentes y agrega solo los scripts del frontend.

## 3. Crear la carpeta del frontend

Desde la raíz del monorepo:

```bash
mkdir -p apps/web
```

Si ya tienes la carpeta `apps/web` del paquete entregado, cópiala directamente dentro de `apps`.

## 4. Crear el `package.json` del frontend

Archivo:

```text
apps/web/package.json
```

Contenido:

```json
{
  "name": "@ecommerce/web",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "nuxt dev --port 3000",
    "build": "nuxt build",
    "generate": "nuxt generate",
    "preview": "nuxt preview",
    "typecheck": "nuxt typecheck",
    "lint": "eslint .",
    "test:e2e": "playwright test"
  },
  "dependencies": {
    "@nuxt/eslint": "^1.9.0",
    "@nuxt/icon": "^2.0.0",
    "@pinia/nuxt": "^0.11.2",
    "@tailwindcss/vite": "^4.1.17",
    "nuxt": "^4.2.1",
    "pinia": "^3.0.4",
    "tailwindcss": "^4.1.17",
    "vue": "^3.5.24",
    "vue-router": "^4.6.3"
  },
  "devDependencies": {
    "@playwright/test": "^1.56.1",
    "typescript": "^5.9.3",
    "vitest": "^4.0.14",
    "vue-tsc": "^3.1.5"
  }
}
```

## 5. Crear configuración de Nuxt

Archivo:

```text
apps/web/nuxt.config.ts
```

Contenido:

```ts
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2026-09-13',
  css: ['~/assets/css/main.css'],
  devtools: { enabled: true },
  modules: [
    '@pinia/nuxt',
    '@nuxt/eslint',
    '@nuxt/icon'
  ],
  runtimeConfig: {
    public: {
      apiBaseUrl:
        process.env.NUXT_PUBLIC_API_BASE_URL ??
        'http://localhost:4050/api/v1'
    }
  },
  typescript: {
    strict: true,
    typeCheck: true
  },
  vite: {
    plugins: [
      tailwindcss()
    ]
  }
})
```

## 6. Crear variables de entorno

Archivo:

```text
apps/web/.env.example
```

Contenido:

```env
NUXT_PUBLIC_API_BASE_URL=http://localhost:4050/api/v1
```

Luego crear el archivo local:

```bash
cp apps/web/.env.example apps/web/.env
```

El archivo `.env` no debe subirse al repositorio.

## 7. Crear archivo de estilos

Archivo:

```text
apps/web/assets/css/main.css
```

Contenido:

```css
@import "tailwindcss";

:root {
  color-scheme: light;
  font-family:
    Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
}

body {
  margin: 0;
  background: #f8fafc;
  color: #0f172a;
}

button,
input,
select,
textarea {
  font: inherit;
}

.focus-ring {
  outline: 2px solid transparent;
  outline-offset: 2px;
}

.focus-ring:focus-visible {
  outline-color: #2563eb;
}
```

## 8. Instalar dependencias

Desde la raíz del monorepo:

```bash
npm install
```

Esto instalará las dependencias de:

```text
apps/api
apps/web
```

## 9. Ejecutar backend

En una terminal:

```bash
npm run dev:api
```

La API debe quedar disponible en:

```text
http://localhost:4050/api/v1
```

Verifica con:

```bash
curl http://localhost:4050/api/v1/health
```

## 10. Ejecutar frontend

En otra terminal:

```bash
npm run dev:web
```

El frontend debe abrir en:

```text
http://localhost:3000
```

## 11. Rutas del frontend

| Ruta | Uso |
| --- | --- |
| `/` | Catálogo de productos |
| `/login` | Inicio de sesión |
| `/register` | Registro |
| `/cart` | Carrito |
| `/orders` | Historial de órdenes |
| `/orders/:id` | Detalle de orden |
| `/admin/products` | Administración de productos |
| `/admin/categories` | Administración de categorías |

## 12. Archivos principales del frontend

```text
apps/web/
├── app.vue
├── nuxt.config.ts
├── package.json
├── assets/
│   └── css/
│       └── main.css
├── components/
│   ├── AdminProductForm.vue
│   ├── AppHeader.vue
│   ├── EmptyState.vue
│   └── ProductCard.vue
├── composables/
│   └── useApi.ts
├── middleware/
│   ├── admin.ts
│   └── auth.ts
├── pages/
│   ├── index.vue
│   ├── login.vue
│   ├── register.vue
│   ├── cart.vue
│   ├── orders/
│   │   ├── index.vue
│   │   └── [id].vue
│   └── admin/
│       ├── products.vue
│       └── categories.vue
├── stores/
│   ├── auth.ts
│   ├── cart.ts
│   ├── catalog.ts
│   └── orders.ts
└── types/
    └── api.ts
```

## 13. Flujo de prueba recomendado

1. Levantar backend.
2. Levantar frontend.
3. Entrar a `/register`.
4. Crear usuario.
5. Consultar catálogo en `/`.
6. Agregar productos al carrito.
7. Entrar a `/cart`.
8. Confirmar orden.
9. Consultar `/orders`.

## 14. Acceso administrador

El registro normal crea usuarios con rol:

```text
CUSTOMER
```

Para usar el panel admin, promover un usuario desde el backend:

```bash
node apps/api/scripts/promote-admin.js correo@dominio.com
```

Después iniciar sesión nuevamente.

## 15. Validaciones recomendadas

Ejecutar:

```bash
npm run typecheck:web
npm run lint:web
npm run build:web
```

Si se agregan pruebas E2E:

```bash
npm run test:e2e:web
```

## 16. Commit sugerido

```bash
git switch -c feature/ecommerce-frontend
git add .
git commit -m "feat(web): add Nuxt ecommerce frontend"
```

## Checklist final

- [ ] `apps/web` existe.
- [ ] `apps/web/package.json` existe.
- [ ] `nuxt.config.ts` apunta al backend correcto.
- [ ] `.env` del frontend está configurado.
- [ ] `npm install` se ejecutó desde la raíz.
- [ ] Backend levanta correctamente.
- [ ] Frontend levanta correctamente.
- [ ] Registro funciona.
- [ ] Login funciona.
- [ ] Catálogo consulta productos.
- [ ] Carrito agrega productos.
- [ ] Órdenes se generan correctamente.
- [ ] Admin puede crear productos y categorías.

